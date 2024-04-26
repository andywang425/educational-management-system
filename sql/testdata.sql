--1. College

INSERT INTO College (college_no, college_name, college_intro)
VALUES
('01', '经济与管理学院', '学习经济与管理'),
('02', '数理学院', '学好数理化'),
('03', '外国语学院', '学外语'),
('04', '马克思主义学院', '马克思主义'),
('05', '能源与机械工程学院', '能源与机械'),
('06', '电气工程学院', '电工'),
('07', '自动化工程学院', '自动'),
('08', '计算机科学与技术学院', '计算机'),
('09', '电子信息与工程学院', '电子信息');

GO
--2. Major

INSERT INTO Major (major_no, college_no, major_name, major_intro)
VALUES
('001', '08', '计算机科学与技术', '计算机科学'),
('002', '08', '软件工程', '写软件'),
('003', '08', '信息安全', '信安'),
('004', '09', '电子信息工程', '电子信息工程'),
('005', '09', '通信工程', '通信工程');
GO
--3. Class

INSERT INTO Class (class_no, major_no, entrance_year, student_num)
VALUES
('2021051', '001', 2021, 31),
('2021052', '001', 2021, 32),
('2021053', '001', 2021, 30);
GO
--4. Student_current

INSERT INTO Student_current (student_no, class_no, student_name, student_gender, student_status)
VALUES
('20211455', '2021051', 'name1', '男', '团员'),
('20211458', '2021051', 'name2', '男', '群众'),
('20211461', '2021052', 'name3', '男', '群众'),
('20211462', '2021052', 'name4', '女', '团员'),
('20211463', '2021052', 'name5', '男', '团员'),
('20211464', '2021052', 'name6', '男', '党员'),
('20211503', '2021053', 'name7', '女', '团员'),
('20211508', '2021053', 'name8', '女', '团员');
GO
--5. Teacher

INSERT INTO Teacher (teacher_no, major_no, teacher_name, teacher_gender, teacher_title)
VALUES
('20210000', '001', '杜海周', '男', '副教授'),
('20210001', '001', '王小雨', '男', '助教'),
('20210002', '002', '刘福涛', '女', '副教授'),
('20210003', '002', '俞天天', '女', '讲师'),
('20210004', '003', '陈严冰', '女', '教授'),
('20210005', '003', '胡雨凡', '男', '讲师'),
('20210006', '004', '河西陪', '男', '讲师'),
('20210007', '005', '周董梅', '女', '副教授');
GO
--6. Course

INSERT INTO Course (course_no, course_name, credit, course_hour, pre_course_no, college_no)
VALUES
('200031600', '计算机科学导论', 2, 10, NULL, '08'),
('200031601', '数据库原理', 4, 20, '200031600', '08'),
('200031602', 'JAVA高级语言程序设计', 3, 20, NULL, '08'),
('200031603', '数据结构', 4, 25, '200031602', '08'),
('200030451', '编译原理', 4, 20, NULL, '08'),
('200032110', '通信原理', 3, 24, NULL, '09');
GO
--7. Course_plan

INSERT INTO Course_plan (course_id, major_no, course_no, entrance_year, year, semester)
VALUES
('200031602.2003', '001', '200031602', 2021, 2021, 2),
('200031600.1200', '001', '200031600', 2021, 2021, 1),
('200031602.1001', '001', '200031602', 2021, 2022, 1),
('200031601.1401', '001', '200031601', 2021, 2022, 1),
('200031601.1402', '001', '200031601', 2021, 2022, 1),
('200030451.1822', '001', '200030451', 2021, 2022, 1),

('200031602.2004', '001', '200031602', 2021, 2023, 1),
('200031600.1201', '001', '200031600', 2021, 2023, 1),
('200031602.1002', '001', '200031602', 2021, 2023, 1),
('200031601.1403', '001', '200031601', 2021, 2023, 1),
('200031601.1404', '001', '200031601', 2021, 2023, 1),
('200030451.1824', '001', '200030451', 2021, 2023, 1);
GO
--8. Teach

INSERT INTO Teach (course_id, teacher_no)
VALUES
('200031600.1200', '20210000'),
('200031602.2003', '20210002'),
('200031602.1001', '20210001'),
('200031601.1401', '20210003'),
('200031601.1402', '20210004'),
('200030451.1822', '20210005'),

('200031602.2004', '20210000'),
('200031600.1201', '20210002'),
('200031602.1002', '20210001'),
('200031601.1403', '20210003'),
('200031601.1404', '20210004'),
('200030451.1824', '20210005');
GO
--9. Student_current_elective_course

INSERT INTO Student_current_elective_course (student_no, course_id, score) VALUES
('20211462', '200031600.1200', 81);
INSERT INTO Student_current_elective_course (student_no, course_id, score) VALUES
('20211463', '200031602.2003', 86);
INSERT INTO Student_current_elective_course (student_no, course_id) VALUES
('20211463', '200031602.2004');
INSERT INTO Student_current_elective_course (student_no, course_id, score) VALUES
('20211464', '200031600.1200', 90);
INSERT INTO Student_current_elective_course (student_no, course_id, score) VALUES
('20211464', '200031602.2003', 67);
INSERT INTO Student_current_elective_course (student_no, course_id) VALUES
('20211464', '200031602.2004');
GO

--10. Student_current_account
--INSERT INTO Student_current_account (student_no, student_current_password_hash)
--VALUES
--('20211463', substring(sys.fn_sqlvarbasetostr(HashBytes('MD5',concat('SUEP', '20211463'))),3,32)),
--('20211464', substring(sys.fn_sqlvarbasetostr(HashBytes('MD5',concat('SUEP', '20211464'))),3,32));

--11. Teacher_account
--INSERT INTO Teacher_account (teacher_no, teacher_password_hash)
--VALUES
--('20210000', substring(sys.fn_sqlvarbasetostr(HashBytes('MD5',concat('SUEP', '20211463'))),3,32)),
--('20210001', substring(sys.fn_sqlvarbasetostr(HashBytes('MD5',concat('SUEP', '20211464'))),3,32));

--12. admin_account
INSERT INTO Admin_account (admin_no, admin_password_hash)
VALUES
('admin123', substring(sys.fn_sqlvarbasetostr(HashBytes('MD5',concat('SUEP', 'suep123'))),3,32));
