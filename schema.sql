drop table if exists patients;
create table patients (
  id integer primary key autoincrement,
  patient_id text not null,
  sex text not null,
  date_created integer not null,
  xray integer not null,
  double_density integer,
  oblique_diameter real,
  appendage_shape integer,
  interbronchial_angle real,
  subcarinal_angle real,
  post_bronchus integer,
  sup_bronchus integer,
  post_esophagus integer,
  ct_mri integer not null,
  atrial_diameter real,
  area_4chamber real,
  area_2chamber real,
  atrial_length real,
  atrial_volume real,
  outcome text
);
