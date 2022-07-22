select * 
from teachers;

-- melihat dosen yang salary lebih dari 50000
SELECT * 
from teachers 
where salary>50000;

-- melihat nama depan samuel 
SELECT * 
from teachers 
where first_name = "samuel";

-- melihat dosen nama depan berawal 'sam-' 
select *
from teachers
where first_name like 'sam%';

-- melihat nama depan berakhir "-sam"
SELECT * 
from teachers
where first_name like "%sam";

-- melihat nama depan mengandung "-sam-"
SELECT * 
from teachers 
where first_name NOT like '%sam%';

-- melihat gaji tertinggi 
select max(salary) 
from teachers;

-- melihat identitas gaji tertinggi (cara1 tidak valid)
select first_name, last_name,max(salary)
from teachers;

-- melihat identitas gaji tertinggi (cara 2 Error)
select first_name,last_name, salary
from teachers
where salary = max(salary);

-- melihat identitas gaji tertinggi (cara 3 subquery)

select first_name ,last_name,salary
from teachers
where salary=(
  select max(salary)
  from teachers
);

-- melihat gaji rata-rata 
select AVG(salary),floor(avg(salary)) ,ceil(avg(salary))
from teachers;


-- melihat gaji dosen tertinggi di setiap universitas 
SELECT first_name,last_name,school,salary
from teachers
where (school,salary) in (
   select school,max(salary)
   from teachers
   group by school);

-- join dengan teacher id dengan courses teacher_id 
select * 
from teachers
join courses on teachers.id = courses.teachers_id

-- melihat dosen yang mengajar kalkulus 
select * 
from teachers
join courses on teachers.id = courses.teachers_id
where courses.name = 'calculus';

-- melihat jumlah mata kuliah di setiap universitas 
select teachers.school, count(DISTINCT(courses.name)) as "Total Matkul"
from teachers
join courses on teachers.id = courses.teachers_id
group by teachers.school

-- melihat university yang memiliki total matkul > 4 cara 1
select teachers.school, count(DISTINCT(courses.name)) as total_matkul
from teachers
join courses on teachers.id = courses.teachers_id
group by teachers.school
having total_matkul > 4;

-- cara 2 tanpa having
select *
from (
  select teachers.school, count(DISTINCT(courses.name)) as total_matkul
  from teachers
  join courses on teachers.id = courses.teachers_id
  group by teachers.school) as hasil_join
where hasil_join.total_matkul > 4

-- melihat nama dosen (first name) beserta banyak mata kuliah yang diajarkan 
select teachers.first_name, count(DISTINCT(courses.name)) as total_matkul
from teachers
join courses on teachers.id = courses.teachers_id
group BY teachers.first_name
ORDER by total_matkul DESC



