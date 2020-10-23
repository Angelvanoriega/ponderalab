import psycopg2
import traceback

def execute_select(query):
	connection = None
	cursor = None
	try:
		connection = get_connection_object()
		cursor = connection.cursor()
		cursor.execute(query)
		desc = cursor.description
		column_names = [col[0] for col in desc]
		data = [dict(zip(column_names, row))
				for row in cursor.fetchall()]
		return data
	except (Exception, psycopg2.Error) as error:
		print("Error while connecting to PostgreSQL", error)
	finally:
		if connection:
			cursor.close()
			connection.close()

def execute_query(query):
	connection = None
	cursor = None
	try:
		connection = get_connection_object()
		cursor = connection.cursor()
		cursor.execute(query)
		connection.commit()
		count = cursor.rowcount
		print(count, "affected rows by query")
		return True
	except (Exception, psycopg2.Error) as error:
		print("Error while connecting to PostgreSQL", error)
	finally:
		if connection:
			cursor.close()
			connection.close()

def execute_insert(table_name, data):
	connection = None
	cursor = None
	try:
		connection = get_connection_object()
		cursor = connection.cursor()
		column_list = []
		row_count = 1
		value_list = []
		for row in data:
			values = []
			for column in row:
				if row_count == 1:
					column_list.append('"' + column + '"')
				values.append("'" + row[column] + "'")
			str_values_row = '(' + ','.join(values) + ')'
			value_list.append(str_values_row)
			row_count = row_count + 1

		str_columns = ','.join(column_list)
		str_values = ','.join(value_list)

		insert_query = f"INSERT INTO {table_name} ({str_columns}) VALUES {str_values}"
		# Print PostgreSQL version
		cursor.execute(insert_query)
		connection.commit()
		count = cursor.rowcount
		print(count, "Record inserted successfully")

	except (Exception, psycopg2.Error) as error:
		print("Error while inserting into PostgreSQL:", error)
		traceback.print_exc()
	finally:
		if connection:
			cursor.close()
			connection.close()


def get_connection_object():
	connection = psycopg2.connect(
		user="ponderausr",
		password="ponderapwd",
		host="pondera.clsjvgvvhooq.us-east-1.rds.amazonaws.com",
		port="5432",
		database="pondera"
	)
	return connection
