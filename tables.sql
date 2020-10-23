drop table if exists ageb;
create table ageb (
	entidad text,
	nom_ent text,
	mun text,
	nom_mun text,
	loc text,
	nom_loc text,
	ageb text,
	mza text,
	pobtot decimal,
	pobmas decimal,
	pobfem decimal
);

CREATE INDEX idx_ageb_iter_join
ON ageb(entidad,mun,loc);

drop table if exists iter;
create table iter(
    entidad text,
    nom_ent text,
    mun text,
    nom_mun text,
    loc text,
    nom_loc text,
    longitud text,
    latitud text,
    cp text
);

CREATE INDEX idx_iter_ageb_join
ON iter(entidad,mun,loc);

drop table if exists cp_coords;
create table cp_coords(
    cp text,
    coords text,
    file_name text
);
CREATE INDEX idx_cp_2
ON cp_coords(cp);

drop table if exists cp_coords_detail;
create table cp_coords_detail(
    cp text,
    lat decimal,
    lon decimal,
    file_name text
);

CREATE INDEX idx_cp
ON cp_coords_detail (cp);

CREATE INDEX idx_cp_lat
ON cp_coords_detail USING btree (lat);

CREATE INDEX idx_cp_lon
ON cp_coords_detail USING btree (lon);


CREATE INDEX idx_cp_lat_lon_ab_xyz
ON cp_coords_detail USING btree (cp,lat,lon);

drop table if exists entidades;
create table entidades(
    entidad text,
    nom_ent text,
    file_name text
);
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('01', 'Colima', 'CP_01Ags_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('02', 'Colima', 'CP_02BC_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('03', 'Colima', 'CP_03BCS_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('04', 'Colima', 'CP_04Camp_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('05', 'Colima', 'CP_05Coah_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('06', 'Colima', 'CP_06Col_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('07', 'Colima', 'CP_07Chs_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('08', 'Colima', 'CP_08Chih_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('09', 'Colima', 'CP_09CdMx_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('10', 'Colima', 'CP_10Dur_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('11', 'Colima', 'CP_11Gto_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('12', 'Colima', 'CP_12Gro_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('13', 'Colima', 'CP_13Hgo_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('14', 'Colima', 'CP_14Jal_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('15', 'Colima', 'CP_15EdoMex_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('16', 'Colima', 'CP_16Mich_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('17', 'Colima', 'CP_17Mor_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('18', 'Colima', 'CP_18Nay_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('19', 'Colima', 'CP_19NL_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('20', 'Colima', 'CP_20Oax_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('21', 'Colima', 'CP_21Pue_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('22', 'Colima', 'CP_22Qro_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('23', 'Colima', 'CP_23QRoo_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('24', 'Colima', 'CP_24SLP_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('25', 'Colima', 'CP_25Sin_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('26', 'Colima', 'CP_26Son_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('27', 'Colima', 'CP_27Tab_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('28', 'Colima', 'CP_28Tamps_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('29', 'Colima', 'CP_29Tlax_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('30', 'Colima', 'CP_30Ver_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('31', 'Colima', 'CP_31Yuc_v2.kml');
INSERT INTO entidades(entidad, nom_ent, file_name) VALUES ('32', 'Colima', 'CP_32Zac_v2.kml');


