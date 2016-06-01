DROP TABLE if exists patients;
CREATE TABLE patients (
  id SERIAL PRIMARY KEY,
  patient_id varchar(80) UNIQUE NOT NULL,
  gender varchar(8) NOT NULL,
  date_created integer NOT NULL,
  xray smallint NOT NULL,
  double_density smallint,
  oblique_diameter real,
  appendage_shape smallint,
  xray_outcome varchar(80),
  ctmri smallint NOT NULL,
  interbronchial_angle real,
  subcarinal_angle real,
  post_bronchus integer,
  sup_bronchus integer,
  post_esophagus integer,
  atrial_diameter real,
  area_4chamber real,
  area_2chamber real,
  atrial_length real,
  atrial_volume real,
  ctmri_outcome varchar(80)
);
