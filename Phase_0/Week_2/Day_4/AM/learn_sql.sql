CREATE TABLE teachers (
  id int NOT null PRIMARY key AUTO_INCREMENT,
  first_name varchar(25) not null,
  last_name varchar(50),
  school varchar(50) not null,
  hire_date date,
  salary numeric 
);

-- Menambah column age 
ALTER table teachers add age int;

-- menghapus column age 
alter table teachers drop column age;

-- mengubah column salary 
ALTER TABLE teachers MODIFy COLUMN salary int ;

-- mengubah nama table teacher jadi guru 
ALTER TABLE teachers rename to guru;
-- mengubah table guru menjadi teachers 
alter table guru rename to teachers;

-- mengisi table teachers 
INSERT INTO teachers (id,first_name, last_name, school, hire_date, salary)
    VALUES (1,'Janet', 'Smith', 'MIT', '2011-10-30', 36200),
           (2,'Lee', 'Reynolds', 'MIT', '1993-05-22', 65000),
           (3,'Samuel', 'Cole', 'Cambridge University', '2005-08-01', 43500),
           (4,'Samantha', 'Bush', 'Cambridge University', '2011-10-30', 36200),
           (5,'Betty', 'Diaz', 'Cambridge University', '2005-08-30', 43500),
           (6,'Kathleen', 'Roush', 'MIT', '2010-10-22', 38500),
           (7,'James', 'Diaz', 'Harvard University', '2003-07-18', 61000),
           (8,'Zack', 'Smith', 'Harvard University', '2000-12-29', 55500),
           (9,'Luis', 'Gonzales', 'Standford University', '2002-12-01', 50000),
           (10,'Frank', 'Abbers', 'Standford University', '1999-01-30', 66000);

-- melihat semua isi data table teachers 
SELECT * from teachers;

-- menghapus semua data dari table teachers 
truncate table teachers;
SELECT * from teachers;

-- mengubah salary dari id == 3
UPDATE teachers
set salary = 60000
where id = 3;
SELECT * from teachers;

-- delete value dari table teachers where id = 6 
DELETE from teachers
where id = 6;
SELECT * from teachers;

-- menambah data baru ke table teachers 
INSERT INTO teachers (first_name, last_name, school, hire_date, salary)
    VALUES ('Samuel', 'Abbers', 'Standford University', '2006-01-30', 32000),
           ('Jessica', 'Abbers', 'Standford University', '2005-01-30', 33000),
           ('Tom', 'Massi', 'Harvard University', '1999-09-09', 39500),
           ('Esteban', 'Brown', 'MIT', '2007-01-30', 36000),
           ('Carlos', 'Alonso', 'Standford University', '2001-01-30', 44000);
select *  FROM teachers;

-- melihat panjang baris 
select count(*) as jumlah_data from teachers;

-- melihat first name lastname dan school 
SELECT first_name,last_name,school
from teachers;

-- conditional ,menampilkan semua dosen yang mengajar di MIT 
select * 
from teachers
where school = 'MIT' ;

-- mencari dosen yang last name adalah 'smith' atau 'abbers'

-- cara 1
select * 
from teachers 

-- menghitung total baris city dan jumlah baris unique value dari city dari table station
select  count(city) - count(distinct(city))
from station