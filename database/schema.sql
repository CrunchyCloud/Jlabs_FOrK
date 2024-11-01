
-- create database jlabs
--   with
--   owner = postgres
--   encoding = 'utf8'
--   lc_collate = 'english_canada.1252'
--   lc_ctype = 'english_canada.1252'
--   locale_provider = 'libc'
--   tablespace = pg_default
--   connection limit = -1
--   is_template = false;

-- drop if exists
drop database if exists jlabs;

-- create the database
create database jlabs with encoding 'utf8';

-- connect to the new database
\c jlabs;

-- create the workers table first since it is referenced in other tables
create table workers ( 
  workersid serial primary key,
  workersname varchar(50) not null,
  email varchar(50) not null,
  phonenumber varchar(10) not null, 
  image bytea,
  usertype varchar(13) not null,
  staffpassword varchar(50) not null
);

-- create the examtype table first since it is referenced in other tables
create table examtype (
  examtype varchar(50) primary key
);

-- create the users table
create table users (
  id serial primary key,
  username varchar(50) not null unique,
  email varchar(100) not null unique,
  password varchar(255) not null,
  created_at timestamp default current_timestamp
);

-- create the patient table
create table patient (
  healthid smallserial primary key,
  patientname varchar(50) not null,
  email varchar(50) not null,
  dob date not null,
  status boolean not null,
  doctorid int not null,
  patientpassword varchar(50) not null,
  phonenumber varchar(10),
  foreign key (doctorid) references workers(workersid)
);

-- create the posts table
create table posts (
  id serial primary key,
  user_id int,
  title varchar(255) not null,
  content varchar(355) not null,
  created_at timestamp default current_timestamp,
  foreign key (user_id) references users(id)
);

-- create the examtable
create table examtable (
  examid serial primary key,
  examdate date not null,
  healthid smallint not null,  -- ensure this matches the patient table
  workersid serial not null,
  examtype varchar(50) not null,
  foreign key (healthid) references patient(healthid),
  foreign key (workersid) references workers(workersid),
  foreign key (examtype) references examtype(examtype)
);

-- create the testtypes table
create table testtypes (
  testtype varchar(50) primary key,
  lowerbound numeric(4, 1) not null,
  upperbound numeric(4, 1) not null, 
  unit varchar(6) not null,
  examtype varchar(50),
  foreign key (examtype) references examtype(examtype)
);

-- create the testresults table
create table testresults (
  testtype varchar(50),
  foreign key (testtype) references testtypes(testtype),
  examid serial,
  foreign key (examid) references examtable(examid),
  results numeric(7, 4) not null,
  resultdate date not null
);

-- create the summaryreport table
create table summaryreport (
  sreportid numeric(4) primary key,
  workersid serial not null,
  foreign key (workersid) references workers(workersid),
  monthoryear varchar(5) check (monthoryear in ('month', 'year')) not null,
  summarydate date not null,
  timeperiod varchar(40)
);

-- create the summaryreportentries table
create table summaryreportentries (
  sreportid numeric(4),
  foreign key (sreportid) references summaryreport(sreportid),
  healthid smallserial,
  foreign key (healthid) references patient(healthid),
  noofexams numeric(2) not null,
  abnormalexams numeric(2) not null
);

-- create the predictreports table
create table predictreports (
  preportid numeric(4) primary key not null,
  workersid serial not null,
  foreign key (workersid) references workers(workersid),
  healthid smallserial not null,
  foreign key (healthid) references patient(healthid),
  pdate date not null
);

-- create the predictreportsentries table
create table predictreportsentries (
  preportid numeric(4) primary key,
  foreign key (preportid) references predictreports(preportid),
  examtype varchar(50) not null,
  foreign key (examtype) references examtype(examtype),
  concernvalue numeric(3) not null
);

-- create the smartmonitor table
create table smartmonitor (
  monitorid serial primary key not null,
  workersid serial not null,
  foreign key (workersid) references workers(workersid),
  examtype varchar(50) default 'on stand by' not null,
  foreign key (examtype) references examtype(examtype),
  smartstatus varchar(10) check (smartstatus in ('sent', 'not sent')) not null,
  healthid smallserial not null,
  foreign key (healthid) references patient(healthid)
);
