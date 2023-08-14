CREATE DATABASE 'nbaplayers';
USE 'nbaplayers';

CREATE TABLE 'players' (
  'id' varchar(255) NOT NULL,
  'name' varchar(255) NOT NULL,
  PRIMARY KEY ('id');

CREATE TABLE 'teams' (
  'team_id' int NOT NULL AUTO_INCREMENT,
  'team' varchar(255) DEFAULT NULL,
  PRIMARY KEY ('team_id');

CREATE TABLE 'careerstats' (
  'id' varchar(255) NOT NULL,
  'career_g' int DEFAULT NULL,
  'career_per' double DEFAULT NULL,
  'career_ws' double DEFAULT NULL,
  'numseasons' int DEFAULT NULL,
  PRIMARY KEY ('id'),
  CONSTRAINT 'csid' FOREIGN KEY ('id') REFERENCES 'players' ('id');

CREATE TABLE 'draftinfo' (
  'id' varchar(255) NOT NULL,
  'draft_pick' varchar(255) DEFAULT NULL,
  'draft_round' varchar(255) DEFAULT NULL,
  'draft_team' varchar(255) DEFAULT NULL,
  'draft_year' int DEFAULT NULL,
  PRIMARY KEY ('id'),
  CONSTRAINT 'diid' FOREIGN KEY ('id') REFERENCES 'players' ('id');

CREATE TABLE 'education' (
  'id' varchar(255) NOT NULL,
  'highschool' varchar(255) DEFAULT NULL,
  'hscity' varchar(255) DEFAULT NULL,
  'hsloc' varchar(255) DEFAULT NULL,
  'college' varchar(255) DEFAULT NULL,
  PRIMARY KEY ('id'),
  CONSTRAINT 'eid' FOREIGN KEY ('id') REFERENCES 'players' ('id');

CREATE TABLE 'medinfo' (
  'id' varchar(255) NOT NULL,
  'birthdate' date DEFAULT NULL,
  'height' varchar(255) DEFAULT NULL,
  'weight' int DEFAULT NULL,
  PRIMARY KEY ('id'),
  CONSTRAINT 'miid' FOREIGN KEY ('id') REFERENCES 'players' ('id');

CREATE TABLE 'origin' (
  'id' varchar(255) NOT NULL,
  'birthcity' varchar(255) DEFAULT NULL,
  'birthloc' varchar(255) DEFAULT NULL,
  PRIMARY KEY ('id'),
  CONSTRAINT 'hid' FOREIGN KEY ('id') REFERENCES 'players' ('id');

CREATE TABLE 'pergame' (
  'id' varchar(255) NOT NULL,
  'career_ast' double DEFAULT NULL,
  'career_pts' double DEFAULT NULL,
  'career_trb' double DEFAULT NULL,
  PRIMARY KEY ('id'),
  CONSTRAINT 'pgid' FOREIGN KEY ('id') REFERENCES 'players' ('id');

CREATE TABLE 'playstyle' (
  'id' varchar(255) NOT NULL,
  'position' varchar(255) DEFAULT NULL,
  'shoots' varchar(255) DEFAULT NULL,
  PRIMARY KEY ('id'),
  KEY 'psid_idx' ('id'),
  CONSTRAINT 'psid' FOREIGN KEY ('id') REFERENCES 'players' ('id');

CREATE TABLE 'salaries' (
  'id' varchar(255) NOT NULL,
  'salseq' int NOT NULL,
  'salary' int DEFAULT NULL,
  'season' varchar(255) DEFAULT NULL,
  'team_id' int NOT NULL,
  PRIMARY KEY ('id','salseq'),
  KEY 'teamid_idx' ('team_id'),
  CONSTRAINT 'salid' FOREIGN KEY ('id') REFERENCES 'players' ('id'),
  CONSTRAINT 'teamid' FOREIGN KEY ('team_id') REFERENCES 'teams' ('team_id');

CREATE TABLE 'splits' (
  'id' varchar(255) NOT NULL,
  'career_fg' double DEFAULT NULL,
  'career_fg3' double DEFAULT NULL,
  'career_ft' double DEFAULT NULL,
  'career_efg' double DEFAULT NULL,
  PRIMARY KEY ('id'),
  CONSTRAINT 'sid' FOREIGN KEY ('id') REFERENCES 'players' ('id');

CREATE TABLE 'years' (
  'id' varchar(255) NOT NULL,
  'yrstart' int DEFAULT NULL,
  'yrend' int DEFAULT NULL,
  'totalyrs' int DEFAULT NULL,
  PRIMARY KEY ('id'),
  CONSTRAINT 'yrid' FOREIGN KEY ('id') REFERENCES 'players' ('id');
