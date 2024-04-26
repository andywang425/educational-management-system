from .mssql import Base_db
from utils import md5, get_elective_semester


class Db:
    db = Base_db()

    def login(self, uname, pwd):
        pwd_hash = md5(pwd)
        return self.checkPassowrdHash(uname, pwd_hash)

    def checkPassowrdHash(self, uname, pwdHash):
        res = self.db.select(
            "select * from Student_current_account where student_no = ? and student_current_password_hash = ?", uname, pwdHash)
        if res:
            return 1
        res = self.db.select(
            "select * from teacher_account where teacher_no = ? and teacher_password_hash = ?", uname, pwdHash)
        if res:
            return 2
        res = self.db.select(
            "select * from admin_account where admin_no = ? and admin_password_hash = ?", uname, pwdHash)
        if res:
            return 3
        res = self.db.select(
            "select * from student_graduated_account where graduated_student_no = ? and student_graduated_password_hash = ?", uname, pwdHash)
        if res:
            return 4
        return -1

    def modifyPassword(self, username, role, new_password):
        pwd_hash = md5(new_password)
        try:
            if role == 1:
                self.db.update(
                    "update Student_current_account set student_current_password_hash = ? where student_no = ?", pwd_hash, username)
            elif role == 2:
                self.db.update(
                    "update teacher_account set teacher_password_hash = ? where teacher_no = ?", pwd_hash, username)
            elif role == 3:
                self.db.update(
                    "update admin_account set admin_password_hash = ? where admin_no = ?", pwd_hash, username)
            else:
                self.db.updatet(
                    "update student_graduated_account set student_graduated_password_hash = ? where graduated_student_no = ?", pwd_hash, username)
            return True
        except Exception as e:
            print(e)
            return False

    def getAllCollegeInfo(self):
        res = self.db.select(
            "select college_no, college_name, college_intro from College")
        if res:
            return res
        return []

    def getAllCollegeName(self):
        try:
            res = self.db.select("select college_name from College")
            if res:
                return res
            return []
        except Exception as e:
            print(e)

    def createCollege(self, no, name, intro):
        try:
            self.db.insert('insert into College (college_no, college_name, college_intro) values (?, ?, ?)', no, name, intro)
            return True
        except Exception as e:
            print(e)
            return False

    def deleteCollege(self, no):
        try:
            self.db.delete('delete College where college_no = ?', no)
            return True
        except Exception as e:
            print(e)
            return False

    def modifyCollege(self, no, name, intro):
        try:
            self.db.update(
                'update College set college_name = ?, college_intro = ? where college_no = ?', name, intro, no)
            return True
        except Exception as e:
            print(e)
            return False

    def getAllMajorInfo(self):
        res = self.db.select(
            "select College.college_no, major_no, college_name, major_name, major_intro from College join Major on College.college_no = Major.college_no")
        if res:
            return res
        return []

    def getOneCollegeAllMajorName(self, college_name):
        res = self.db.select(
            "select major_name from College join Major on College.college_no = Major.college_no where college_name = ?", college_name)
        if res:
            return res
        return []

    def createMajor(self, cno, mno, mname, intro):
        try:
            self.db.insert(
                'insert into Major (college_no, major_no, major_name, major_intro) values (?, ?, ?, ?)', cno, mno, mname, intro)
            return True
        except Exception as e:
            print(e)
            return False

    def deleteMajor(self, no):
        try:
            self.db.delete('delete Major where major_no = ?', no)
            return True
        except Exception as e:
            print(e)
            return False

    def modifyMajor(self, cno, mno, name, intro):
        try:
            self.db.update('update Major set college_no = ?, major_name = ?, major_intro = ? where major_no = ?',
                           cno, name, intro, mno)
            return True
        except Exception as e:
            print(e)
            return False

    def getCollegeName(self, no):
        res = self.db.select("select college_name from College where college_no = ?", no)
        if res:
            return res
        return []

    def getAllClassInfo(self):
        res = self.db.select(
            "select Class.major_no, class_no, major_name, entrance_year, student_num from Class join Major on Class.major_no = Major.major_no")
        if res:
            return res
        return []

    def createClass(self, mno, cno, entrance_year, student_num):
        try:
            self.db.insert('insert into Class (class_no, major_no, entrance_year, student_num) values (?, ?, ?, ?)',
                           cno, mno, entrance_year, student_num)
            return True
        except Exception as e:
            print(e)
            return False

    def getMajorName(self, no):
        res = self.db.select("select major_name from Major where major_no = ?", no)
        if res:
            return res
        return []

    def modifyClass(self, mno, cno, entrance_year, student_num):
        try:
            self.db.update('update Class set major_no = ?, entrance_year = ?, student_num = ? where class_no = ?',
                           mno, entrance_year, student_num, cno)
            return True
        except Exception as e:
            print(e)
            return False

    def deleteClass(self, no):
        try:
            self.db.delete('delete Class where class_no = ?', no)
            return True
        except Exception as e:
            print(e)
            return False

    def getAllCurrentStudentInfo(self):
        res = self.db.select(
            "select student_no, class_no, entrance_year, student_name, student_gender, college_name,  major_name, student_status from student_current_info")
        if res:
            return res
        return []

    def createStudent(self, sno, cno,  sname, gender, status):
        try:
            self.db.insert(
                'insert into Student_current (student_no, class_no, student_name, student_gender, student_status) values (?, ?, ?, ?, ?)', sno, cno, sname, gender, status)
            return True
        except Exception as e:
            print(e)
            return False

    def getOneStudentInfo(self, no):
        res = self.db.call('getCurrentStudentInfo', no)
        if res:
            return res
        return []

    def modifyStudent(self, sno, cno, sname, gender, status):
        try:
            self.db.update('update Student_current set class_no = ?, student_name = ?, student_gender = ?, student_status = ? where student_no = ?',
                           cno, sname, gender, status, sno)
            return True
        except Exception as e:
            print(e)
            return False

    def deleteStudent(self, no):
        try:
            self.db.delete('delete Student_current where student_no = ?', no)
            return True
        except Exception as e:
            print(e)
            return False

    def getAllTeacherInfo(self):
        res = self.db.select(
            "select teacher_no, Major.major_no, major_name, teacher_name, teacher_gender, teacher_title from Teacher join Major on Teacher.major_no = Major.major_no")
        if res:
            return res
        return []

    def createTeacher(self, tno, mno, tname, gender, title):
        try:
            self.db.insert(
                'insert into Teacher (teacher_no, major_no, teacher_name, teacher_gender, teacher_title) values (?, ?, ?, ?, ?)', tno, mno, tname, gender, title)
            return True
        except Exception as e:
            print(e)
            return False

    def modifyTeacher(self, tno, mno, tname, gender, title):
        try:
            self.db.update('update Teacher set major_no = ?, teacher_name = ?, teacher_gender = ?, teacher_title = ? where teacher_no = ?',
                           mno, tname, gender, title, tno)
            return True
        except Exception as e:
            print(e)
            return False

    def deleteTeacher(self, no):
        try:
            self.db.delete('delete Teacher where teacher_no = ?', no)
            return True
        except Exception as e:
            print(e)
            return False

    def getAllCourseInfo(self):
        res = self.db.select(
            "select c1.course_no, c1.course_name, c1.credit, c1.course_hour, c1.pre_course_no, c2.course_name as pre_course_name, c1.college_no, college_name from Course c1 left outer join Course c2 on c1.pre_course_no = c2.course_no join College on c1.college_no = College.college_no")
        if res:
            return res
        return []

    def createCourse(self, cno, college_no, cname, credit, chour, pre_cno):
        try:
            self.db.insert(
                'insert into Course (course_no, course_name, credit, course_hour, pre_course_no, college_no) values (?, ?, ?, ?, ?, ?)', cno, cname, credit, chour, pre_cno, college_no)
            return True
        except Exception as e:
            print(e)
            return False

    def getOneCourseInfo(self, no):
        try:
            res = self.db.select("select c1.course_no, c1.course_name, c1.credit, c1.course_hour, c1.pre_course_no, c2.course_name as pre_course_name, c1.college_no, college_name from Course c1 left outer join Course c2 on c1.pre_course_no = c2.course_no join College on c1.college_no = College.college_no where c1.course_no = ?", no)
            if res:
                return res
            return []
        except Exception as e:
            print(e)
            return []

    def modifyCourse(self, cno, college_no, cname, credit, chour, pre_cno):
        try:
            self.db.update('update Course set course_name = ?, credit = ?, course_hour = ?, pre_course_no = ?, college_no = ? where course_no = ?',
                           cname, credit, chour, pre_cno, college_no, cno)
            return True
        except Exception as e:
            print(e)
            return False

    def deleteCourse(self, no):
        try:
            self.db.delete('delete Course where course_no = ?', no)
            return True
        except Exception as e:
            print(e)
            return False

    def createClasses(self, classes):
        try:
            conn = self.db.connect(autocommit=False)
            cursor = conn.cursor()
            try:
                for c in classes:
                    cursor.execute('insert into Class (class_no, major_no, entrance_year, student_num) values (?, ?, ?, ?)',
                                   c['cno'], c['mno'], c['entrance_year'], c['student_num'])
            except Exception as e:
                print('Rollback', e)
                cursor.rollback()
                return False
            cursor.commit()
            return True
        except Exception as e:
            print('Other exception', e)
            return False

    def createStudents(self, students):
        try:
            conn = self.db.connect(autocommit=False)
            cursor = conn.cursor()
            try:
                for s in students:
                    cursor.execute('insert into Student_current (student_no, class_no, student_name, student_gender, student_status) values (?, ?, ?, ?, ?)',
                                   s['sno'], s['cno'], s['sname'], s['gender'], s['status'])
            except Exception as e:
                print('Rollback', e)
                cursor.rollback()
                return False
            cursor.commit()
            return True
        except Exception as e:
            print('Other exception', e)
            return False

    def getAllCoursePlanInfo(self):
        res = self.db.select(
            "select course_id, course_plan.major_no, major_name, course_plan.course_no, course_name, entrance_year, year, semester from course_plan join Course on course_plan.course_no = Course.course_no join Major on course_plan.major_no = Major.major_no")
        if res:
            return res
        return []

    def createCoursePlan(self, cid, mno, cno, entrance_year, year, semester):
        try:
            self.db.insert(
                'insert into course_plan (course_id, major_no, course_no, entrance_year, year, semester) values (?, ?, ?, ?, ?, ?)',
                cid, mno, cno, entrance_year, year, semester)
            return True
        except Exception as e:
            print(e)
            return False

    def getOneCoursePlanInfo(self, id):
        res = self.db.select(
            "select course_id, course_plan.major_no, major_name, course_plan.course_no, course_name, entrance_year, year, semester from course_plan join Course on course_plan.course_no = Course.course_no join Major on course_plan.major_no = Major.major_no where course_id = ?", id)
        if res:
            return res
        return []

    def modifyCoursePlan(self, cid, mno, cno, entrance_year, year, semester):
        try:
            self.db.update(
                'update course_plan set major_no = ?, course_no = ?, entrance_year = ?, year = ?, semester = ? where course_id = ?',
                mno, cno, entrance_year, year, semester, cid)
            return True
        except Exception as e:
            print(e)
            return False

    def deleteCoursePlan(self, id):
        try:
            self.db.delete(
                'delete course_plan where course_id = ?', id)
            return True
        except Exception as e:
            print(e)
            return False

    def getAllTeachInfo(self):
        res = self.db.select("select teach.course_id, teach.teacher_no, Course.course_no, course_name, teacher_name, year, semester from teach join course_plan on teach.course_id = course_plan.course_id join Course on course_plan.course_no = Course.course_no join Teacher on teach.teacher_no = Teacher.teacher_no")
        if res:
            return res
        return []

    def createTeachInfo(self, cid, tno):
        try:
            self.db.insert('insert into teach (course_id, teacher_no) values (?, ?)', cid, tno)
            return True
        except Exception as e:
            print(e)
            return False

    def getOneTeachInfo(self, cid, tno):
        res = self.db.select("select teach.course_id, teach.teacher_no, Course.course_no, course_name, teacher_name, year, semester from teach join course_plan on teach.course_id = course_plan.course_id join Course on course_plan.course_no = Course.course_no join Teacher on teach.teacher_no = Teacher.teacher_no where teach.course_id = ? and teach.teacher_no = ?",
                             cid, tno)
        if res:
            return res
        return []

    def modifyTeachInfo(self, old_cid, new_cid, old_tno, new_tno):
        try:
            self.db.update(
                'update teach set course_id = ?, teacher_no = ? where course_id = ? and teacher_no = ?',
                new_cid, new_tno, old_cid, old_tno)
            return True
        except Exception as e:
            print(e)
            return False

    def deleteTeachInfo(self, cid, tno):
        try:
            self.db.delete(
                'delete teach where course_id = ? and teacher_no = ?', cid, tno)
            return True
        except Exception as e:
            print(e)
            return False

    def graduateStudents(self, sno_list):
        try:
            conn = self.db.connect(autocommit=False)
            cursor = conn.cursor()
            try:
                for sno in sno_list:
                    cursor.execute('{CALL graduateStudent (?)}', sno)
            except Exception as e:
                print('Rollback', e)
                cursor.rollback()
                return False
            cursor.commit()
            return True
        except Exception as e:
            print('Other exception', e)
            return False

    def getAllStudentInfo(self, json):
        res = self.db.select("select student_no, student_name, student_gender, student_status, entrance_year, class_no, major_name, college_name, student_type from student_all_info where student_no like ? and student_name like ? and student_gender like ? and student_status like ? and entrance_year like ? and class_no like ? and major_name like ? and college_name like ? and student_type like ?",
                             json['sno'], json['sname'], json['gender'], json['status'], json['entrance_year'], json['cno'], json['mname'], json['cname'], json['type'])
        if res:
            return res
        return []

    def getAllTeacherInfoV2(self, json):
        res = self.db.select("select teacher_no, teacher_name, major_name, college_name, teacher_gender, teacher_title from Teacher join Major on Teacher.major_no = Major.major_no join College on Major.college_no = College.college_no where teacher_no like ? and teacher_name like ? and major_name like ? and college_name like ? and teacher_gender like ? and teacher_title like ?",
                             json['tno'], json['tname'], json['mname'], json['cname'], json['gender'], json['title'])
        if res:
            return res
        return []

    def getAllCourseInfoV2(self, json):
        param_list = [json['cno'], json['cname'], json['credit'], json['chour']]
        sql_stat = "select c1.course_no, c1.course_name, c1.credit, c1.course_hour, c1.pre_course_no, c2.course_name as pre_course_name from Course c1 left outer join Course c2 on c1.pre_course_no = c2.course_no where c1.course_no like ? and c1.course_name like ? and c1.credit like ? and c1.course_hour like ?"
        if json['pre_cno'] != '%':
            sql_stat += " and c1.pre_course_no like ?"
            param_list.append(json['pre_cno'])
        if json['pre_cname'] != '%':
            sql_stat += " and c2.course_name like ?"
            param_list.append(json['pre_cname'])
        res = self.db.select(sql_stat, *param_list)
        if res:
            return res
        return []

    def getAllTeachInfoV2(self, json):
        res = self.db.select("select teach.course_id, course_name, college_name, major_name, teacher_name, year, semester from teach join course_plan on teach.course_id = course_plan.course_id join Course on course_plan.course_no = Course.course_no join Teacher on teach.teacher_no = Teacher.teacher_no join Major on course_plan.major_no = Major.major_no join College on Major.college_no = College.college_no where teach.course_id like ? and course_name like ? and college_name like ? and major_name like ? and teacher_name like ? and year like ? and semester like ?",
                             json['cid'], json['course_name'], json['college_name'], json['mname'], json['tname'], json['year'], json['semester'])
        if res:
            return res
        return []

    def getAllElectiveInfo(self, json):
        res = self.db.select("SELECT course_id, student_name, course_name, college_name, major_name, year, semester, score, ROUND(grade_point, 1) as grade_point, student_type FROM student_all_elective_info where course_id like ? and student_name like ? and course_name like ? and college_name like ? and major_name like ? and year like ? and semester like ? and score like ? and grade_point like ? and student_type like ?",
                             json['cid'], json['sname'], json['course_name'], json['college_name'], json['mname'], json['year'], json['semester'], json['score'], json['gp'], json['type'])
        if res:
            return res
        return []

    def studentElectiveStatement(self, sno, year, semester):
        res = self.db.call('statStudentElective', sno, year, semester)
        if res:
            return res
        return []

    def teacherTeachStatement(self, tno, year, semester):
        res = self.db.call('statTeacherTeach', tno, year, semester)
        if res:
            return res
        return []

    def classGPAStatement(self, cno, year, semester, order_row):
        res = self.db.call('statClassGPA', cno, year, semester, order_row)
        if res:
            return res
        return []

    def teacherTitleStatement(self):
        res = self.db.call('statTeacherTitle')
        if res:
            return res
        return []

    def collegeCourseStatement(self, college_name):
        res = self.db.call('statCollegeCourse', college_name)
        if res:
            return res
        return []

    def teacherCourseStatement(self, year, semester):
        res = self.db.call('statTeacherCourse', year, semester)
        if res:
            return res
        return []

    def getStudentCoursePlan(self, year, semester, sno):
        res = self.db.select("select course_id, c1.course_name, c1.credit, c1.course_hour, c2.course_name as pre_course_name from course_plan cp join Course c1 on cp.course_no = c1.course_no left join Course c2 on c1.pre_course_no = c2.course_no where c1.college_no in (select College.college_no from College, Major, Class, Student_current where College.college_no = Major.college_no and Major.major_no = Class.major_no and Class.class_no = Student_current.class_no and student_no = ?) and year = ? and semester = ? and not exists (select course_id from student_current_elective_course sc where cp.course_id = sc.course_id)",
                             sno, year, semester)
        if res:
            return res
        return []

    def getPreCourseNoName(self, cid):
        res = self.db.select(
            "select c1.pre_course_no, c2.course_name as pre_course_name from Course c1 left outer join Course c2 on c1.pre_course_no = c2.course_no join course_plan cp on c1.course_no = cp.course_no where cp.course_id = ?", cid)
        if res and res[0] and res[0][0]:
            return res[0]
        return [None, None]

    def checkElective(self, cid, sno):
        no, name = self.getPreCourseNoName(cid)
        if no is None:
            return (True, None)
        res = self.db.select(
            "select * from student_current_elective_course sc join course_plan cp on cp.course_id = sc.course_id where course_no = ? and student_no = ?", no, sno)
        if res:
            return (True, None)
        else:
            return (False, name)

    def checkTime(self, cid):
        res = self.db.select(
            "select year, semester from course_plan where course_id = ?", cid)
        year, month = get_elective_semester()
        if res and res[0][0] == year and res[0][1] == month:
            return True
        else:
            return False

    def electiveCourse(self, cid, sno):
        try:
            self.db.insert('insert into student_current_elective_course (student_no, course_id) values (?, ?)', sno, cid)
            return True
        except Exception as e:
            print(e)
            return False

    def studentMyCourses(self, year, semester, sno):
        res = self.db.select("select year, semester, sc.course_id, course_name, CASE WHEN score >= 60 THEN credit ELSE 0 END AS credits, score, ROUND(grade_point, 1) from student_current_elective_course sc join course_plan cp on cp.course_id = sc.course_id join Course c on c.course_no = cp.course_no where year like ? and semester like ? and student_no = ?",
                             year, semester, sno)
        if res:
            return res
        return []

    def checkCourseTeacher(self, cid, tno):
        res = self.db.select("select * from teach where teacher_no = ? and course_id = ?",
                             tno, cid)
        if res:
            return True
        return False

    def updateStudentScores(self, course_id, students):
        try:
            conn = self.db.connect(autocommit=False)
            cursor = conn.cursor()
            try:
                for s in students:
                    cursor.execute('update student_current_elective_course set score = ? where course_id = ? and student_no = ?',
                                   s['score'], course_id, s['sno'])
            except Exception as e:
                print('Rollback', e)
                cursor.rollback()
                return False
            cursor.commit()
            return True
        except Exception as e:
            print('Other exception', e)
            return False

    def getStudentScore(self, json, tno):
        res = self.db.select("select course_id, student_name, course_name, year, semester, score, grade_point from student_all_score where year like ? and semester like ? and teacher_no like ? and course_id like ?",
                             json['year'], json['semester'], tno, json['cid'])
        if res:
            return res
        return []

    def getStudentElectiveInfo(self, sno):
        res = self.db.select("select course_id, course_name, year, semester, score, grade_point from student_all_score where student_no = ?",
                             sno)
        if res:
            return res
        return []
