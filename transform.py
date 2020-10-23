import csv
from db import execute_insert, execute_select, execute_query
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from os import listdir
from os.path import isfile, join
import xml.dom.minidom
import re

def read_ageb_files():
	all_files = [f for f in listdir('ageb/') if isfile(join('ageb/', f))]
	for file_name in all_files:
		print(file_name)
		with open('ageb/'+file_name) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			line_count = 0
			ageb_data = []
			for row in csv_reader:
				if line_count == 0:
					line_count += 1
				else:
					ageb_row = {
						'entidad': row[0],
						'nom_ent': row[1],
						'mun': row[2],
						'nom_mun': row[3],
						'loc': row[4],
						'nom_loc': row[5],
						'ageb': row[6],
						'mza': row[7],
						'pobtot': row[8].replace("*","0"),
						'pobmas': row[9].replace("*","0"),
						'pobfem': row[10].replace("*","0")
					}
					if ageb_row['mun'] == '000' or ageb_row['loc'] == '000' or ageb_row['ageb'] == '000' or ageb_row['mza'] == '000':
						pass
					else:
						ageb_data.append(ageb_row)
					line_count += 1
			execute_insert('ageb',ageb_data)
			print(f'Processed {line_count} lines.')

def read_iter_files():
	iter_data = []
	execute_query('TRUNCATE TABLE iter;')
	with open('iter/iter_00_cpv2010.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
			else:
				iter_row = {
					'entidad': row[0],
					'nom_ent': '',
					'mun': row[2],
					'nom_mun': '',
					'loc': row[4],
					'nom_loc': '',
					'longitud': str((int(row[6]) * -1) / 10000 if is_integer(row[6]) else ''),
					'latitud': str((int(row[7])) / 10000 if is_integer(row[7]) else '')
				}
				if iter_row['mun'] == '000' or iter_row['loc'] == '000' or iter_row['longitud'] == '' or iter_row['latitud'] == '':
					pass
				else:
					iter_data.append(iter_row)
					pass
				line_count += 1

	processed_rows = 0
	processed_rows_total = 1
	new_iter_data = []
	for row in iter_data:
		lat_rounded = float(row['latitud'][:4])
		lon_rounded = float(row['longitud'][:6])
		coords_data = execute_select(
			"select cp, coords from cp_coords where cp in ("
			"select  distinct cp from cp_coords_detail "
			"where (lat >= %s and lat < %s) "
			"and (lon >= %s and lon < %s))" % ((lat_rounded - .4),(lat_rounded + .4),(lon_rounded - .4),(lon_rounded + .4))
		)

		postal_code = find_postal_code(row['latitud'],row['longitud'], coords_data)
		row['cp'] = '' if postal_code is None else postal_code
		print("%s - %s left %s " % (postal_code, str(processed_rows_total), str(len(iter_data) - processed_rows_total)))
		processed_rows_total = processed_rows_total + 1
		processed_rows = processed_rows + 1
		new_iter_data.append(row)
		if processed_rows == 5000:
			execute_insert('iter', new_iter_data)
			processed_rows = 0
			new_iter_data = []

	print(f'Processed {line_count} lines.')

def find_postal_code(latx, lony, coords_data):
	point = Point(float(latx), float(lony)) # punto que queremos encontrar dentro de algun poligono

	for coords_list_cp in coords_data: # aqui se encuentran todos los codigos postales por estado y se procesan las coordenadas por CP
		pointList = []
		coords_list_separated = coords_list_cp['coords'].split(' ')
		"""
		Por codigo postal se procesa la lista de coordenadas separadas y se pretende hacer un poligono para verificar
		si la latitud y longitud de la localidad se encuentra dentro de alguno de estos poligonos
		"""
		for cls in coords_list_separated:
			if len(cls) > 1:
				lonlat = cls.split(',')
				longitudy = float(lonlat[0])
				latitudx = float(lonlat[1])
				pointList.append((latitudx,longitudy))


		polygon = Polygon((pointList))
		if polygon.contains(point):
			return coords_list_cp['cp']

def read_cps_files():
	all_files = [f for f in listdir('cps/') if isfile(join('cps/', f))]
	for file_name in all_files:
		print(file_name)
		doc = xml.dom.minidom.parse('cps/'+ file_name)
		cp_coords_data = []
		cp_coords_detail_data = []
		placemark_xml_list = doc.getElementsByTagName("Placemark")
		for placemark in placemark_xml_list:
			cp = ""
			cps_xml = placemark.getElementsByTagName("SimpleData")
			for cp_xml in cps_xml:
				cp = cp_xml.firstChild.data

			coords_xml_list = placemark.getElementsByTagName("coordinates")
			for coords_xml in coords_xml_list:
				formatted_coords = (str(coords_xml.firstChild.data).replace('\n',' '))
				formatted_coords = re.sub('\s+',' ',formatted_coords)

				coords_list_separated = formatted_coords.split(' ')

				for cls in coords_list_separated:
					if len(cls) > 1:
						lonlat = cls.split(',')
						longitudy = float(lonlat[0])
						latitudx = float(lonlat[1])

						cp_coords_detail = {
							'cp': cp,
							'lat': str(latitudx),
							'lon': str(longitudy),
							'file_name': file_name
						}
						cp_coords_detail_data.append(cp_coords_detail)

				cp_coords = {
					'cp' : cp,
					'coords' : formatted_coords,
					'file_name' : file_name
				}

				cp_coords_data.append(cp_coords)
		execute_query('DELETE FROM cp_coords where file_name = \'%s\'' % file_name)
		execute_insert('cp_coords', cp_coords_data)
		execute_query('DELETE FROM cp_coords_detail where file_name = \'%s\'' % file_name)
		execute_insert('cp_coords_detail', cp_coords_detail_data)

def is_integer(n):
	try:
		float(n)
	except ValueError:
		return False
	else:
		return float(n).is_integer()

if __name__ == '__main__':
	#read_cps_files()
	read_iter_files()
	#read_ageb_files()
