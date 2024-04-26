USE MASTER
go
DROP DATABASE IF EXISTS SUEP
go
CREATE DATABASE SUEP
go
USE SUEP
go
/*==============================================================*/
/* Table: 班级                                                  */
/*==============================================================*/
create table Class (
   class_no             char(7)              not null,         -- 班号
   major_no             char(3)              not null,         -- 专业编号
   entrance_year        smallint             not null,         -- 入学年份
   student_num          smallint             not null,         -- 班级人数
   constraint PK_CLASS primary key (class_no)
)
go

/*==============================================================*/
/* Index: 班级-专业编号                                          */
/*==============================================================*/
create index CLASS_MAJOR_NO on Class (
   major_no ASC   -- 专业编号
)
go

/*==============================================================*/
/* Table: 学院                                                  */
/*==============================================================*/
create table College (
   college_no           char(2)              not null,        -- 学院编号
   college_name         varchar(30)          not null,        -- 学院名称
   college_intro        varchar(200)         null,            -- 学院简介
   constraint PK_COLLEGE primary key (college_no)
)
go

/*==============================================================*/
/* Table: 课程                                                */
/*==============================================================*/
create table Course (
   course_no            varchar(10)          not null,       -- 课号
   course_name          varchar(20)          not null,       -- 课名
   credit               smallint             not null,       -- 学分
   course_hour          smallint             not null,       -- 学时
   pre_course_no        varchar(10)          null,           -- 先行课课号
   college_no           char(2)              not null,       -- 开设该课程的学院编号
   constraint PK_COURSE primary key (course_no)
)
go

/*==============================================================*/
/* Table: 专业                                                  */
/*==============================================================*/
create table Major (
   major_no             char(3)              not null,      -- 专业编号
   college_no           char(2)              not null,      -- 学院编号
   major_name           varchar(30)          not null,      -- 专业名称
   major_intro          varchar(200)         null,          -- 专业简介
   constraint PK_MAJOR primary key (major_no)
)
go

/*==============================================================*/
/* Index: 专业-学院编号                                          */
/*==============================================================*/
create index MAJOR_COLLEGE_NO on Major (
   college_no ASC   -- 学院编号
)
go

/*==============================================================*/
/* Table: 在籍学生                                              */
/*==============================================================*/
create table Student_current (
   student_no           char(8)              not null,      -- 在籍学生学号
   class_no             char(7)              not null,      -- 班号
   student_name         varchar(20)          not null,      -- 学生姓名
   student_gender       nchar(1)             not null,      -- 学生性别
   student_status       varchar(10)          not null,      -- 学生政治面貌
   constraint PK_STUDENT_CURRENT primary key (student_no)
)
go

/*==============================================================*/
/* Index: 在籍学生-班号                                          */
/*==============================================================*/
create index STUDENT_CURRENT_CLASS_NO on Student_current (
   class_no ASC   -- 班号
)
go

/*==============================================================*/
/* Table: 毕业学生                                              */
/*==============================================================*/
create table Student_graduated (
   graduated_student_no char(8)              not null,      -- 毕业学生学号
   class_no             char(7)              not null,      -- 班号
   student_name         varchar(20)          not null,      -- 学生姓名
   student_gender       nchar(1)             not null,      -- 学生性别
   student_status       varchar(10)          not null,      -- 学生政治面貌
   constraint PK_STUDENT_GRADUATED primary key (graduated_student_no)
)
go

/*==============================================================*/
/* Index: 毕业学生-班号                                          */
/*==============================================================*/
create index STUDENT_GRADUATED_CLASS_NO on Student_graduated (
   class_no ASC   -- 班号
)
go

/*==============================================================*/
/* Table: 课程计划                                              */
/*==============================================================*/
create table course_plan (
   course_id            varchar(15)          not null,   -- 课程 id
   major_no             char(3)              not null,   -- 专业编号
   course_no            varchar(10)          not null,   -- 课号
   entrance_year        smallint             not null,   -- 入学年份（年级）
   year                 smallint             not null,   -- 年份
   semester             smallint             not null,   -- 学期
   constraint PK_COURSE_PLAN primary key (course_id)
)
go

/*==============================================================*/
/* Index: 课程计划-专业编号                                      */
/*==============================================================*/
create index COURSE_PLAN_MAJOR_NO on course_plan (
   major_no ASC   -- 专业编号
)
go

/*==============================================================*/
/* Index: 课程计划-课号                                          */
/*==============================================================*/
create index COURSE_PLAN_COURSE_NO on course_plan (
   course_no ASC  -- 课号
)
go

/*==============================================================*/
/* Table: 在籍学生账户信息                                       */
/*==============================================================*/
create table student_current_account (
   student_no                    char(8)              not null,   -- 在籍学生学号
   student_current_password_hash char(32)              not null,   -- 学生密码哈希
   constraint PK_STUDENT_CURRENT_ACCOUNT primary key (student_no)
)
go

/*==============================================================*/
/* Table: 在籍学生选课信息                                       */
/*==============================================================*/
create table student_current_elective_course (
   student_no           char(8)              not null,   -- 在籍学生学号
   course_id            varchar(15)          not null,   -- 课程 id
   score                smallint             null,       -- 学分
   grade_point          float(1)             null,       -- 绩点
   constraint PK_STUDENT_CURRENT_ELECTIVE_CO primary key (student_no, course_id)
)
go

/*==============================================================*/
/* Index: 在籍学生选课信息-在籍学生学号                           */
/*==============================================================*/
create index STUDENT_CURRENT_ELECTIVE_COURSE_STUDENT_NO on student_current_elective_course (
   student_no ASC    -- 在籍学生学号
)
go

/*==============================================================*/
/* Index: 在籍学生选课信息-课程id                                */
/*==============================================================*/
create index STUDENT_CURRENT_ELECTIVE_COURSE_COURSE_ID on student_current_elective_course (
   course_id ASC     -- 课程id
)
go

/*==============================================================*/
/* Table: 毕业学生账户信息                                       */
/*==============================================================*/
create table student_graduated_account (
   graduated_student_no            char(8)              not null, -- 毕业学生学号
   student_graduated_password_hash char(32)             not null  -- 学生密码哈希
)
go

/*==============================================================*/
/* Table: 毕业学生选课信息                                       */
/*==============================================================*/
create table student_graduated_elective_course (
   graduated_student_no char(8)              not null,   -- 毕业学生学号
   course_id            varchar(15)          not null,   -- 课程 id
   score                smallint             not null,   -- 分数
   grade_point          float(1)             null,       -- 绩点
   constraint PK_STUDENT_GRADUATED_ELECTIVE primary key (graduated_student_no, course_id)
)
go

/*==============================================================*/
/* Index: 毕业学生选课信息-毕业学生学号                           */
/*==============================================================*/
create index STUDENT_GRADUATED_ELECTIVE_COURSE_GRADUATED_STUDENT_NO on student_graduated_elective_course (
   graduated_student_no ASC -- 毕业学生学号
)
go

/*==============================================================*/
/* Index: 毕业学生选课信息-课程id                                 */
/*==============================================================*/
create index STUDENT_GRADUATED_ELECTIVE_COURSE_COURSE_ID on student_graduated_elective_course (
   course_id ASC  -- 课程id
)
go

/*==============================================================*/
/* Table: 教授课程                                               */
/*==============================================================*/
create table teach (
   course_id            varchar(15)          not null,    -- 课程 id
   teacher_no           char(8)              not null,    -- 工号
   constraint PK_TEACH primary key (course_id, teacher_no)
)
go

/*==============================================================*/
/* Index: 教授课程-课程id                                        */
/*==============================================================*/
create index TEACH_COURSE_ID on teach (
   course_id ASC  -- 课程id
)
go

/*==============================================================*/
/* Index: 教授课程-工号                                          */
/*==============================================================*/
create index TEACH_TEACHER_NO on teach (
   teacher_no ASC -- 工号
)
go

/*==============================================================*/
/* Table: 教师                                                  */
/*==============================================================*/
create table Teacher (
   teacher_no           char(8)              not null,   -- 工号
   major_no             char(3)              not null,   -- 专业编号
   teacher_name         varchar(20)          not null,   -- 姓名
   teacher_gender       nchar(1)             not null,   -- 性别
   teacher_title        varchar(20)          null,       -- 职称
   constraint PK_TEACHER primary key (teacher_no)
)
go

/*==============================================================*/
/* Index: 教师-专业编号                                          */
/*==============================================================*/
create index TEACHER_MAJOR_NO on teacher (
   major_no ASC -- 专业编号
)
go

/*==============================================================*/
/* Table: 教师账户信息                                           */
/*==============================================================*/
create table teacher_account (
   teacher_no            char(8)              not null,     -- 工号
   teacher_password_hash char(32)             not null,     -- 教师密码哈希
   constraint PK_TEACHER_ACCOUNT primary key (teacher_no)
)
go

/*==============================================================*/
/* Table: 教务管理人员账户信息                                           */
/*==============================================================*/
create table admin_account (
   admin_no            char(8)                not null,     -- 教务管理人员账号
   admin_password_hash char(32)             not null,     -- 教务管理人员密码哈希
   constraint PK_ADMIN_ACCOUNT primary key (admin_no)
)
go

/* 外键约束 */
alter table Class
   add constraint FK_CLASS_MAJOR_NO_MAJOR foreign key (major_no)
      references Major (major_no)
go

ALTER TABLE Course
	ADD CONSTRAINT FK_COURSE_PRE_COURSE_NO FOREIGN KEY (pre_course_no)
		REFERENCES Course(course_no)
go

ALTER TABLE Course
	ADD CONSTRAINT FK_COURSE_COLLEGE_NO_COLLEGE FOREIGN KEY (college_no)
		REFERENCES College(college_no)
go

alter table Major
   add constraint FK_MAJOR_COLLEGE_NO_COLLEGE foreign key (college_no)
      references College (college_no)
go

alter table Student_current
   add constraint FK_STUDENT_CURRENT_CLASS_NO_CLASS foreign key (class_no)
      references Class (class_no)
go

alter table Student_graduated
   add constraint FK_STUDENT_GRADUATED_CLASS_NO_CLASS foreign key (class_no)
      references Class (class_no)
go

alter table course_plan
   add constraint FK_COURSE_PLAN_MAJOR_NO_MAJOR foreign key (major_no)
      references Major (major_no)
go

alter table course_plan
   add constraint FK_COURSE_PLAN_COURSE_NO_COURSE foreign key (course_no)
      references Course (course_no)
go

alter table student_current_account
   add constraint FK_STUDENT_CURRENT_ACCOUNT_STUDENT_NO_STUDENT_CURRENT foreign key (student_no)
      references Student_current (student_no)
go

alter table student_current_elective_course
   add constraint FK_STUDENT_CURRENT_ELECTIVE_COURSE_STUDENT_NO_STUDENT_CURRENT foreign key (student_no)
      references Student_current (student_no)
go

alter table student_current_elective_course
   add constraint FK_STUDENT_CURRENT_ELECTIVE_COURSE_COURSE_ID_COURSE_PLAN foreign key (course_id)
      references course_plan (course_id)
go

alter table student_graduated_account
   add constraint FK_STUDENT_GRADUATED_ACCOUNT_GRADUATED_STUDENT_NO_STUDENT_GRADUATED foreign key (graduated_student_no)
      references Student_graduated (graduated_student_no)
go

alter table student_graduated_elective_course
   add constraint FK_STUDENT_GRADUATED_ELECTIVE_COURSE_COURSE_ID_COURSE_PLAN foreign key (course_id)
      references course_plan (course_id)
go

alter table student_graduated_elective_course
   add constraint FK_STUDENT_GRADUATED_ELECTIVE_COURSE_GRADUATED_STUDENT_NO_STUDENT_GRADUATED foreign key (graduated_student_no)
      references Student_graduated (graduated_student_no)
go

alter table teach
   add constraint FK_TEACH_COURSE_ID_COURSE_PLAN foreign key (course_id)
      references course_plan (course_id)
go

alter table teach
   add constraint FK_TEACH_TEACHER_NO_TEACHER foreign key (teacher_no)
      references teacher (teacher_no)
go

alter table teacher
   add constraint FK_TEACHER_MAJOR_NO_MAJOR foreign key (major_no)
      references Major (major_no)
go

alter table teacher_account
   add constraint FK_TEACHER_ACCOUNT_TEACHER_NO_TEACHER foreign key (teacher_no)
      references teacher (teacher_no)
go

/* 默认值约束 */
alter table Student_current
   add constraint DF_student_current_gender
      default '男' for student_gender
go

alter table Student_graduated
   add constraint DF_student_graduated_gender
      default '男' for student_gender
go

alter table Student_current
   add constraint DF_student_current_status
      default '群众' for student_status
go

alter table Student_graduated
   add constraint DF_student_graduated_status
      default '群众' for student_status
go

alter table teacher
   add constraint DF_teacher_gender
      default '男'  for teacher_gender
go

alter table teacher
   add constraint DF_teacher_title
      default '讲师' for teacher_title
go

/* CHECK约束 */
alter table Student_current
   add constraint CK_student_current_status
      check (
         student_status in ('群众', '团员', '党员')
      )
go

alter table Student_graduated
   add constraint CK_student_graduated_status
      check (
         student_status in ('群众', '团员', '党员')
      )
go

alter table teacher
   add constraint CK_teacher_title
      check (
         teacher_title in ('助教', '讲师', '副教授', '教授')
      )
go

alter table student_current_elective_course
   add constraint CK_student_current_elective_course_score
      check (
         score <= 100 and score >= 0
      )
go

alter table student_graduated_elective_course
   add constraint CK_student_graduated_elective_course_score
      check (
         score <= 100 and score >= 0
      )
go

alter table student_current_elective_course
   add constraint CK_student_current_elective_course_grade_point
      check (
         grade_point <= 4 and grade_point >= 0
      )
go

alter table student_graduated_elective_course
   add constraint CK_student_graduated_elective_course_grade_point
      check (
         grade_point <= 4 and grade_point >= 0
      )
go

/* 视图 */
create view student_current_info
   as
select student_no, student_name, student_gender, student_status, entrance_year, c.class_no, major_name, college_name
   from Student_current s
   join Class c on s.class_no = c.class_no
   join Major m on c.major_no = m.major_no
   join College co on m.college_no = co.college_no
go

create view student_graduated_info
   as
select graduated_student_no as student_no, student_name, student_gender, student_status, entrance_year, c.class_no, major_name, college_name
   from Student_graduated s
   join Class c on s.class_no = c.class_no
   join Major m on c.major_no = m.major_no
   join College co on m.college_no = co.college_no
go

create view student_all_info
	as
SELECT student_no, student_name, student_gender, student_status, entrance_year, class_no, major_name, college_name, '在籍' as student_type
FROM student_current_info
UNION ALL
SELECT student_no, student_name, student_gender, student_status, entrance_year, class_no, major_name, college_name, '毕业' as student_type
FROM Student_graduated_info
go

create view student_current_elective_info
	as
select s.course_id, student_name, course_name, college_name, major_name, year, semester, score, grade_point
from student_current_elective_course s
join course_plan cp on s.course_id = cp.course_id
join student_current sc on sc.student_no = s.student_no
join Course c on c.course_no = cp.course_no
join Major m on m.major_no = cp.major_no
join College co on co.college_no = m.college_no
go

create view student_graduated_elective_info
	as
select s.course_id, student_name, course_name, college_name, major_name, year, semester, score, grade_point
from student_graduated_elective_course s
join course_plan cp on s.course_id = cp.course_id
join student_current sc on sc.student_no = s.graduated_student_no
join Course c on c.course_no = cp.course_no
join Major m on m.major_no = cp.major_no
join College co on co.college_no = m.college_no
go

create view student_all_elective_info
	as
select course_id, student_name, course_name, college_name, major_name, year, semester, score, grade_point, '在籍' as student_type
from student_current_elective_info
UNION ALL
select course_id, student_name, course_name, college_name, major_name, year, semester, score, grade_point, '毕业' as student_type
from student_graduated_elective_info
go

create view student_current_score
as
	SELECT teach.course_id, teacher_no, student_name, Student_current.student_no, course_name, year, semester, score, ROUND(grade_point, 1) as grade_point
	from teach
	join course_plan on teach.course_id = course_plan.course_id
	join Course on course_plan.course_no = Course.course_no
	join student_current_elective_course sc on sc.course_id = course_plan.course_id
	join Student_current on sc.student_no = Student_current.student_no
go

create view student_graduated_score
as
	SELECT teach.course_id, teacher_no, student_name, Student_graduated.graduated_student_no as student_no, course_name, year, semester, score, ROUND(grade_point, 1) as grade_point
	from teach
	join course_plan on teach.course_id = course_plan.course_id
	join Course on course_plan.course_no = Course.course_no
	join student_graduated_elective_course sc on sc.course_id = course_plan.course_id
	join Student_graduated on sc.graduated_student_no = Student_graduated.graduated_student_no
go

create view student_all_score
as
	SELECT course_id, teacher_no, student_name, student_no, course_name, year, semester, score, grade_point
	FROM student_current_score
	UNION ALL
	SELECT course_id, teacher_no, student_name, student_no, course_name, year, semester, score, grade_point
	FROM student_graduated_score
go

/* 存储过程 */
create procedure getCurrentStudentInfo
   @student_no char(8)
as
   select *
   from student_current_info
   where student_no = @student_no
go

create procedure getTeacherInfo
    @teacher_no char(8)
as
    SELECT teacher_name, teacher_gender, major_name, college_name, teacher_title
    FROM teacher, Major, College
    WHERE teacher_no = @teacher_no
    and teacher.major_no = Major.major_no
    and Major.college_no = College.college_no
GO

create procedure calcGradePointByScore
   @score smallint,
   @grade_point float(1) OUTPUT
as
   if @score >= 90
      set @grade_point = 4
   else if  @score >= 85 and @score < 90
		set @grade_point = 3.7
	else if @score>=82 and @score <85
		set @grade_point = 3.3
	else if @score>=78 and @score <82
		set @grade_point = 3
	else if @score>=75 and @score <78
		set @grade_point = 2.7
	else if @score>=72 and @score <75
		set @grade_point = 2.3
	else if @score>=68 and @score <72
		set @grade_point = 2
   else if @score>=66 and @score <68
		set @grade_point = 1.7
   else if @score>=64 and @score <66
		set @grade_point = 1.5
   else if @score>=60 and @score <64
		set @grade_point = 1
	else
		set @grade_point = 0
go

create procedure statTeacherCourse
   @year smallint, @semester smallint
as
   begin
      select
         t.teacher_no,
         t.teacher_name,
         COUNT(cp.course_id) as 授课数,
         SUM(c.course_hour) as 学时数
      from
         Teacher t
      join
         Teach te on t.teacher_no = te.teacher_no
      join
         course_plan cp on te.course_id = cp.course_id
      join
         Course c on cp.course_no = c.course_no
      where
         cp.year = @year
         and cp.semester = @semester
      group by
         t.teacher_no,
         t.teacher_name;
   end
go

CREATE PROCEDURE graduateStudent @student_no char(8)
AS
BEGIN
   DECLARE @student_name varchar(20), @class_no char(7), @student_gender char(2),
            @student_status varchar(10), @student_current_password_hash char(32)

   SELECT @student_name = student_name, @class_no = class_no, @student_gender = student_gender,
         @student_status = student_status
   FROM Student_current
   WHERE student_no = @student_no

   SELECT @student_current_password_hash = student_current_password_hash
   FROM student_current_account
   WHERE student_no = @student_no

   INSERT INTO Student_graduated(graduated_student_no, class_no, student_name, student_gender, student_status)
   VALUES (@student_no, @class_no, @student_name, @student_gender, @student_status)

   INSERT INTO student_graduated_account(graduated_student_no, student_graduated_password_hash)
   VALUES (@student_no, @student_current_password_hash)

   INSERT INTO student_graduated_elective_course(graduated_student_no, course_id, score, grade_point)
   SELECT student_no, course_id, score, grade_point
   FROM student_current_elective_course
   WHERE student_no = @student_no

   DELETE FROM student_current_elective_course WHERE student_no = @student_no
   DELETE FROM student_current_account WHERE student_no = @student_no
   DELETE FROM Student_current WHERE student_no = @student_no
END
GO

create procedure statStudentElective
   @student_no char(8), @year smallint, @semester smallint
as
begin
	select student_current_elective_course.course_id, course_name, credit, course_hour, score from
	student_current_elective_course
	join course_plan on student_current_elective_course.course_id = course_plan.course_id
	join Course on course_plan.course_no = Course.course_no
	where student_no = @student_no and year = @year and semester = @semester
end
go

create procedure statTeacherTeach
   @teacher_no char(8), @year smallint, @semester smallint
as
begin
	select teach.course_id, c1.course_name, major_name, c1.credit, c1.course_hour, c2.course_name as pre_course_name
	from teach
	join course_plan on teach.course_id = course_plan.course_id
	join Course c1 on c1.course_no = course_plan.course_no
	left outer join Course c2 on c1.pre_course_no = c2.course_no
	join Major on course_plan.major_no = Major.major_no
	where teacher_no = @teacher_no and year = @year and semester = @semester
end
go

create procedure statClassGPA
   @class_no char(8), @year smallint, @semester smallint, @order_row varchar(20) = 'student_no'
as
begin
if @order_row = 'student_no'
	select s.student_no, student_name, ROUND(AVG(grade_point), 1) as grade_point_avg
	from student_current_elective_course sc
	join Student_current s on s.student_no = sc.student_no
	join course_plan cp on sc.course_id = cp.course_id,
	Class
	where Class.class_no = @class_no and year = @year and semester = @semester
	group by s.student_no, s.student_name
	order by student_no
else
	select s.student_no, student_name, ROUND(AVG(grade_point), 1) as grade_point_avg
	from student_current_elective_course sc
	join Student_current s on s.student_no = sc.student_no
	join course_plan cp on sc.course_id = cp.course_id,
	Class
	where Class.class_no = @class_no and year = @year and semester = @semester
	group by s.student_no, s.student_name
	order by grade_point_avg DESC
end
go

create procedure statTeacherTitle
	as
SELECT 
        College.college_name,
        SUM(CASE WHEN Teacher.teacher_title = '助教' THEN 1 ELSE 0 END) AS 'assistant',
        SUM(CASE WHEN Teacher.teacher_title = '讲师' THEN 1 ELSE 0 END) AS 'lecturer',
        SUM(CASE WHEN Teacher.teacher_title = '副教授' THEN 1 ELSE 0 END) AS 'associate_professor',
        SUM(CASE WHEN Teacher.teacher_title = '教授' THEN 1 ELSE 0 END) AS 'professor'
    FROM 
        Teacher
    INNER JOIN Major
        ON Teacher.major_no = Major.major_no
    INNER JOIN College
        ON Major.college_no = College.college_no
    GROUP BY 
        College.college_name
go

CREATE PROCEDURE statCollegeCourse
    @college_name varchar(30)
AS
BEGIN
    SELECT 
        c1.course_name AS 'course_name', 
        c1.course_hour AS 'course_hour', 
        c2.course_name AS 'pre_course_name', 
        c2.course_hour AS 'pre_course_hour'
    FROM 
        Course AS c1
    LEFT OUTER JOIN 
        Course AS c2
        ON c1.course_no = c2.pre_course_no
	JOIN
        College
        ON c1.college_no = College.college_no
    WHERE 
        college_name = @college_name
END
GO

/* 触发器 */
CREATE TRIGGER mod_credit
   ON student_current_elective_course
   AFTER UPDATE, INSERT
AS
BEGIN
    IF UPDATE(score)
    BEGIN
        -- 建立一张临时表用于存放临时数据
        DECLARE @grade_points TABLE (
            student_no CHAR(8),
            course_id VARCHAR(15),
            grade_point FLOAT(1)
        )
        
        -- 利用游标遍历数据并计算绩点，将结果插入到临时表
        DECLARE cur CURSOR FOR SELECT student_no, course_id, score FROM inserted
        DECLARE @student_no char(8), @course_id varchar(15), @score smallint, @grade_point float(1)
        OPEN cur
        FETCH NEXT FROM cur INTO @student_no, @course_id, @score
        WHILE @@FETCH_STATUS = 0
        BEGIN
            EXEC calcGradePointByScore @score, @grade_point OUTPUT
            INSERT INTO @grade_points(student_no, course_id, grade_point) VALUES (@student_no, @course_id, @grade_point)
            FETCH NEXT FROM cur INTO @student_no, @course_id, @score
        END
        CLOSE cur
        DEALLOCATE cur

        -- 更新表
        UPDATE s
        SET s.grade_point = g.grade_point
        FROM student_current_elective_course AS s
        INNER JOIN @grade_points AS g ON s.student_no = g.student_no AND s.course_id = g.course_id
    END
END
GO


CREATE TRIGGER add_current_student_account
   ON student_current
   AFTER INSERT
AS
   INSERT INTO student_current_account (student_no, student_current_password_hash)
   SELECT i.student_no, substring(sys.fn_sqlvarbasetostr(HashBytes('MD5',concat('SUEP', i.student_no))),3,32)
   FROM inserted i
GO


create trigger add_teacher_account
   on Teacher
   after insert
as
   insert into teacher_account (teacher_no, teacher_password_hash)
   select i.teacher_no, substring(sys.fn_sqlvarbasetostr(HashBytes('MD5',concat('SUEP', i.teacher_no))),3,32)
   FROM inserted i
go

CREATE TRIGGER delete_current_student_account_and_elective_course
   ON student_current
   INSTEAD OF DELETE
AS
BEGIN
   DELETE FROM student_current_account
   WHERE student_no IN (SELECT student_no FROM deleted)
   
   DELETE FROM student_current_elective_course
   WHERE student_no IN (SELECT student_no FROM deleted)

   DELETE FROM student_current
   WHERE student_no IN (SELECT student_no FROM deleted)
END
GO

CREATE TRIGGER delete_graduated_student_account
   ON student_graduated
   INSTEAD OF DELETE
AS
BEGIN
   DELETE FROM student_graduated_account
   WHERE graduated_student_no IN (SELECT graduated_student_no FROM deleted)

   DELETE FROM student_graduated_account
   WHERE graduated_student_no IN (SELECT graduated_student_no FROM deleted)
END
GO

CREATE TRIGGER delete_teacher_account
   ON Teacher
   INSTEAD OF DELETE
AS
BEGIN
   DELETE FROM teacher_account
   WHERE teacher_no IN (SELECT teacher_no FROM deleted)

   DELETE FROM Teacher
   WHERE teacher_no IN (SELECT teacher_no FROM deleted)
END
GO

CREATE TRIGGER delete_student
   ON Class
   INSTEAD OF DELETE
AS
BEGIN
   DELETE FROM Student_current
   WHERE class_no IN (SELECT class_no FROM deleted)
   
   DELETE FROM Student_graduated
   WHERE class_no IN (SELECT class_no FROM deleted)

   DELETE FROM Class
   WHERE class_no IN (SELECT class_no FROM deleted)
END
GO

CREATE TRIGGER delete_teach
   ON course_plan
   INSTEAD OF DELETE
AS
BEGIN
   DELETE FROM teach
   WHERE course_id IN (SELECT course_id FROM deleted)

   DELETE FROM course_plan
   WHERE course_id IN (SELECT course_id FROM deleted)
END
GO

CREATE TRIGGER delete_class
   ON Major
   INSTEAD OF DELETE
AS
BEGIN
   DELETE FROM Class
   WHERE major_no IN (SELECT major_no FROM deleted)

   DELETE FROM course_plan
   WHERE major_no IN (SELECT major_no FROM deleted)

   DELETE FROM Teacher
   WHERE major_no IN (SELECT major_no FROM deleted)

   DELETE FROM Major
   WHERE major_no IN (SELECT major_no FROM deleted)
END
GO

CREATE TRIGGER delete_major_and_course
   ON College
   INSTEAD OF DELETE
AS
BEGIN
   DELETE FROM Major
   WHERE college_no IN (SELECT college_no FROM deleted)

   DELETE FROM Course
   WHERE college_no IN (SELECT college_no FROM deleted)

   DELETE FROM College
   WHERE college_no IN (SELECT college_no FROM deleted)
END
GO