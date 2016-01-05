drop table if exists patients;
create table patients (
  id integer primary key autoincrement,
  patient_id text not null,
  sex text not null
);
