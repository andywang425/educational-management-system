from flask import Blueprint
from flask import request
from flask import session
from db.api import Db
from utils import md5, dict_includes_keys, check_session, pack_rows, pack_row, dict_fuzzy_search_pre

Api = Blueprint('Api', __name__)

db = Db()


@Api.route("/check")
def check():
    if session.get('role') is None:
        return {'code': 302, 'msg': '登录信息过期，请重新登录'}
    return {'code': 0, 'msg': 'ok'}


@Api.route("/login", methods=["POST"])
def login():
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'username', 'password'):
        login_result = db.login(json_data['username'], json_data['password'])
        if login_result >= 0:
            session.permanent = True
            session['username'] = json_data['username']
            session['role'] = login_result
            return {"code": 0, "role": login_result, "msg": "登录成功"}
        else:
            return {"code": 1, "msg": "登录失败，用户名或密码错误"}
    else:
        return {"code": -1, "msg": "缺少username或password"}


@Api.route('/logout', methods=["POST"])
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return {"code": 0, "msg": "Bye"}


@Api.route('/mod_password', methods=["POST"])
def modPassword():
    if session.get('role') is None:
        return {'code': 302, 'msg': '登录信息过期，请重新登录'}
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'old_password', 'new_password'):
        if db.checkPassowrdHash(session.get('username'), md5(json_data['old_password'])) > -1:
            if db.modifyPassword(session.get('username'), session.get('role'), json_data['new_password']):
                session.pop('username', None)
                session.pop('role', None)
                return {"code": 0, "msg": "修改密码成功"}
            else:
                return {"code": 2, "msg": "修改密码失败"}
        else:
            return {"code": 1, "msg": "修改密码失败，原密码错误"}
    else:
        return {"code": -1, "msg": "缺少old_password或new_password"}


@Api.route('/college/all')
def getAllCollegeInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    result = db.getAllCollegeInfo()
    ret = pack_rows(result, 'no', 'name', 'intro')
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/college/names/all')
def getAllCollegeName():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    result = db.getAllCollegeName()
    ret = []
    for i in result:
        ret.append(i[0])
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/college/create', methods=["POST"])
def createCollege():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'no', 'name', 'intro'):
        if db.createCollege(json_data['no'], json_data['name'], json_data['intro']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '插入学院信息失败'}
    else:
        return {"code": -1, "msg": "缺少no或name或intro"}


@Api.route('/college/delete', methods=["POST"])
def deleteCollege():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'no'):
        if db.deleteCollege(json_data['no']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '删除学院信息失败'}
    else:
        return {"code": -1, "msg": "缺少no"}


@Api.route('/college/modify', methods=["POST"])
def modifyCollege():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'no', 'name', 'intro'):
        if db.modifyCollege(json_data['no'], json_data['name'], json_data['intro']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '修改学院信息失败'}
    else:
        return {"code": -1, "msg": "缺少no或name或intro"}


@Api.route('/major/all')
def getAllMajorInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    result = db.getAllMajorInfo()
    ret = pack_rows(result, 'cno', 'mno', 'cname', 'mname', 'intro')
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/college/major/name/all')
def getOneCollegeAllMajorName():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    if dict_includes_keys(request.args, 'cname'):
        result = db.getOneCollegeAllMajorName(request.args.get('cname', type=str))
        ret = []
        for i in result:
            ret.append(i[0])
        return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/major/create', methods=["POST"])
def createMajor():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'cno', 'mno', 'mname', 'intro'):
        if db.createMajor(json_data['cno'], json_data['mno'], json_data['mname'], json_data['intro']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '插入专业信息失败'}
    else:
        return {"code": -1, "msg": "缺少cno或mno或mname或intro"}


@Api.route('/major/delete', methods=["POST"])
def deleteMajor():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if 'no' in json_data:
        if db.deleteMajor(json_data['no']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '删除专业信息失败'}
    else:
        return {"code": -1, "msg": "缺少no"}


@Api.route('/major/modify', methods=["POST"])
def modifyMajor():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'cno', 'mno', 'name', 'intro'):
        if db.modifyMajor(json_data['cno'], json_data['mno'], json_data['name'], json_data['intro']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '修改专业信息失败'}
    else:
        return {"code": -1, "msg": "缺少cno或mno或mname或intro"}


@Api.route('/college/name')
def getCollegeName():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    data = request.args
    if dict_includes_keys(data, 'no'):
        result = db.getCollegeName(request.args.get('no', type=str))
        ret = {'name': result[0][0]}
        return {'code': 0, 'data': ret, 'msg': 'success'}
    else:
        return {"code": -1, "msg": "缺少no"}


@Api.route('/class/all')
def getAllClassInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    result = db.getAllClassInfo()
    ret = pack_rows(result, 'mno', 'cno', 'mname', 'entrance_year', 'student_num')
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/class/create', methods=["POST"])
def createClass():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'mno', 'cno',  'entrance_year', 'student_num'):
        if db.createClass(json_data['mno'], json_data['cno'], json_data['entrance_year'], json_data['student_num']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '插入班级信息失败'}
    else:
        return {"code": -1, "msg": "缺少mno或cno或entrance_year或student_num"}


@Api.route('/major/name')
def getMajorName():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    if dict_includes_keys(request.args, 'no'):
        result = db.getMajorName(request.args.get('no', type=str))
        ret = {'name': result[0][0]}
        return {'code': 0, 'data': ret, 'msg': 'success'}
    else:
        return {"code": -1, "msg": "缺少no"}


@Api.route('/class/modify', methods=["POST"])
def modifyClass():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'mno', 'cno', 'entrance_year', 'student_num'):
        if db.modifyClass(json_data['mno'], json_data['cno'],  json_data['entrance_year'], json_data['student_num']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '修改班级信息失败'}
    else:
        return {"code": -1, "msg": "缺少mno或cno或entrance_year或student_num"}


@Api.route('/class/delete', methods=["POST"])
def deleteClass():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if 'no' in json_data:
        if db.deleteClass(json_data['no']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '删除班级信息失败'}
    else:
        return {"code": -1, "msg": "缺少no"}


@Api.route('/student_current/all')
def getAllCurrentStudentInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    result = db.getAllCurrentStudentInfo()
    ret = pack_rows(result, 'sno', 'cno', 'entrance_year', 'sname', 'gender', 'cname', 'mname', 'status')
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/student_current/create', methods=["POST"])
def createStudent():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'sno', 'cno',  'sname', 'gender', 'status'):
        if db.createStudent(json_data['sno'], json_data['cno'], json_data['sname'], json_data['gender'], json_data['status']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '插入学生信息失败'}
    else:
        return {"code": -1, "msg": "缺少sno或cno或sname或gender或status"}


@Api.route('/student_current/one')
def getOneStudentInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    if dict_includes_keys(request.args, 'no'):
        result = db.getOneStudentInfo(request.args.get('no', type=str))
        row = result[0]
        ret = pack_row(row, 'sno', 'sname', 'gender', 'status', 'entrance_year', 'cno', 'mname', 'cname')
        return {'code': 0, 'data': ret, 'msg': 'success'}
    else:
        return {"code": -1, "msg": "缺少no"}


@Api.route('/student_current/modify', methods=["POST"])
def modifyStudent():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'sno', 'cno',  'sname', 'gender', 'status'):
        if db.modifyStudent(json_data['sno'], json_data['cno'],  json_data['sname'], json_data['gender'], json_data['status']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '修改学生信息失败'}
    else:
        return {"code": -1, "msg": "缺少sno或cno或sname或gender或status"}


@Api.route('/student_current/delete', methods=["POST"])
def deleteStudent():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if 'no' in json_data:
        if db.deleteStudent(json_data['no']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '删除学生信息失败'}
    else:
        return {"code": -1, "msg": "缺少no"}


@Api.route('/teacher/all')
def getAllTeacherInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    result = db.getAllTeacherInfo()
    ret = pack_rows(result, 'tno', 'mno', 'mname', 'tname', 'gender', 'title')
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/teacher/create', methods=["POST"])
def createTeacher():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'tno', 'mno',  'tname', 'gender', 'title'):
        if db.createTeacher(json_data['tno'], json_data['mno'], json_data['tname'], json_data['gender'], json_data['title']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '插入教师信息失败'}
    else:
        return {"code": -1, "msg": "缺少tno或mno或tname或gender或title"}


@Api.route('/teacher/modify', methods=["POST"])
def modifyTeacher():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'tno', 'mno', 'tname', 'gender', 'title'):
        if db.modifyTeacher(json_data['tno'], json_data['mno'],  json_data['tname'], json_data['gender'], json_data['title']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '修改教师信息失败'}
    else:
        return {"code": -1, "msg": "缺少tno或mno或tname或gender或title"}


@Api.route('/teacher/delete', methods=["POST"])
def deleteTeacher():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if 'no' in json_data:
        if db.deleteTeacher(json_data['no']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '删除教师信息失败'}
    else:
        return {"code": -1, "msg": "缺少no"}


@Api.route('/course/all')
def getAllCourseInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    result = db.getAllCourseInfo()
    ret = pack_rows(result, 'cno', 'cname', 'credit', 'chour', 'pre_cno', 'pre_cname', 'college_no', 'college_name')
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/course/create', methods=["POST"])
def createCourse():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'cno', 'college_no', 'cname', 'credit', 'chour', 'pre_cno'):
        if db.createCourse(json_data['cno'], json_data['college_no'], json_data['cname'], json_data['credit'], json_data['chour'], json_data['pre_cno']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '插入课程信息失败'}
    else:
        return {"code": -1, "msg": "缺少cno或credit或chour或pre_cno或college_no"}


@Api.route('/course/name')
def getOneCourseInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    if dict_includes_keys(request.args, 'no'):
        result = db.getOneCourseInfo(request.args.get('no', type=str))
        row = result[0]
        print(row)
        ret = pack_row(row, 'cno', 'cname', 'credit', 'chour', 'pre_cno', 'pre_cname', 'college_no', 'college_name')
        return {'code': 0, 'data': ret, 'msg': 'success'}
    else:
        return {"code": -1, "msg": "缺少no"}


@Api.route('/course/modify', methods=["POST"])
def modifyCourse():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'cno', 'college_no', 'cname', 'credit', 'chour', 'pre_cno'):
        if db.modifyCourse(json_data['cno'], json_data['college_no'], json_data['cname'],  json_data['credit'], json_data['chour'], json_data['pre_cno']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '修改课程信息失败'}
    else:
        return {"code": -1, "msg": "缺少cno或cname或credit或chour或pre_cno"}


@Api.route('/course/delete', methods=["POST"])
def deleteCourse():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if 'no' in json_data:
        if db.deleteCourse(json_data['no']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '删除课程信息失败'}
    else:
        return {"code": -1, "msg": "缺少no"}


@Api.route('/class/upload', methods=["POST"])
def uploadClass():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'classes'):
        for c in json_data['classes']:
            if not dict_includes_keys(c, 'cno', 'mno', 'entrance_year', 'student_num'):
                return {"code": -1, "msg": "缺少mno或cno或entrance_year或student_num"}
        if db.createClasses(json_data['classes']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '批量插入班级信息失败'}
    else:
        return {"code": -1, "msg": "缺少classes"}


@Api.route('/student_current/upload', methods=["POST"])
def uploadStudent():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'students'):
        for c in json_data['students']:
            if not dict_includes_keys(c, 'sno', 'cno', 'sname', 'gender', 'status'):
                return {"code": -1, "msg": "缺少sno或cno或sname或gender或status"}
        if db.createStudents(json_data['students']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '批量插入学生信息失败'}
    else:
        return {"code": -1, "msg": "缺少students"}


@Api.route('/course_plan/all')
def getAllCoursePlanInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    result = db.getAllCoursePlanInfo()
    ret = pack_rows(result, 'cid', 'mno', 'mname', 'cno', 'cname', 'entrance_year', 'year', 'semester')
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/course_plan/create', methods=["POST"])
def createCoursePlan():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'cid', 'mno', 'cno', 'entrance_year', 'year', 'semester'):
        if db.createCoursePlan(json_data['cid'], json_data['mno'], json_data['cno'], json_data['entrance_year'], json_data['year'], json_data['semester']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '插入课程计划信息失败'}
    else:
        return {"code": -1, "msg": "缺少cid或mno或cno或entrance_year或year或semester"}


@Api.route('/course_plan/one')
def getOneCoursePlanInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    if dict_includes_keys(request.args, 'id'):
        result = db.getOneCoursePlanInfo(request.args.get('id', type=str))
        row = result[0]
        ret = pack_row(row, 'cid', 'mno', 'mname', 'cno', 'cname', 'entrance_year', 'year', 'semester')
        return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/course_plan/modify', methods=["POST"])
def modifyCoursePlan():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'cid', 'mno', 'cno', 'entrance_year', 'year', 'semester'):
        if db.modifyCoursePlan(json_data['cid'], json_data['mno'], json_data['cno'], json_data['entrance_year'], json_data['year'], json_data['semester']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '修改课程计划信息失败'}
    else:
        return {"code": -1, "msg": "缺少cid或mno或cno或entrance_year或year或semester"}


@Api.route('/course_plan/delete', methods=["POST"])
def deleteCoursePlan():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if 'id' in json_data:
        if db.deleteCoursePlan(json_data['id']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '删除课程计划失败'}
    else:
        return {"code": -1, "msg": "缺少id"}


@Api.route('/teach/all')
def getAllTeachInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    result = db.getAllTeachInfo()
    ret = pack_rows(result, 'cid', 'tno', 'cno', 'cname', 'tname', 'year', 'semester')
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/teach/one')
def getOneTeachInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    if dict_includes_keys(request.args, 'cid', 'tno'):
        result = db.getOneTeachInfo(request.args.get('cid', type=str), request.args.get('tno', type=str))
        row = result[0]
        ret = pack_row(row, 'cid', 'tno', 'cno', 'cname', 'tname', 'year', 'semester')
        return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/teach/create', methods=["POST"])
def createTeachinfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'cid', 'tno'):
        if db.createTeachInfo(json_data['cid'], json_data['tno']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '插入授课信息失败'}
    else:
        return {"code": -1, "msg": "缺少cid或tno"}


@Api.route('/teach/modify', methods=["POST"])
def modifyTeachinfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'old_cid', 'new_cid', 'old_tno', 'new_tno'):
        if db.modifyTeachInfo(json_data['old_cid'], json_data['new_cid'], json_data['old_tno'], json_data['new_tno']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '修改授课信息失败'}
    else:
        return {"code": -1, "msg": "缺少old_cid或new_cid或old_tno或new_tno"}


@Api.route('/teach/delete', methods=["POST"])
def deleteTeachInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'cid', 'tno'):
        if db.deleteTeachInfo(json_data['cid'], json_data['tno']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '删除授课信息失败'}
    else:
        return {"code": -1, "msg": "缺少cid或tno"}


@Api.route('/student_current/graduate', methods=["POST"])
def graduateStudent():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'sno_list'):
        if db.graduateStudents(json_data['sno_list']):
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': '批量毕业学生失败'}
    else:
        return {"code": -1, "msg": "缺少sno_list"}


@Api.route('/student/all', methods=["POST"])
def getAllStudentInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    dict_fuzzy_search_pre(json_data,  'sno', 'sname', 'gender', 'status',
                          'entrance_year', 'cno', 'mname', 'cname', 'type')
    result = db.getAllStudentInfo(json_data)
    ret = pack_rows(result, 'sno', 'sname', 'gender', 'status', 'entrance_year', 'cno', 'mname', 'cname', 'type')
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/teacher/v2/all', methods=["POST"])
def getAllTeacherInfoV2():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    dict_fuzzy_search_pre(json_data, 'tno', 'tname', 'mname', 'cname', 'gender', 'title')
    result = db.getAllTeacherInfoV2(json_data)
    ret = pack_rows(result, 'tno', 'tname', 'mname', 'cname', 'gender', 'title')
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/course/v2/all', methods=["POST"])
def getAllCourseInfoV2():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    dict_fuzzy_search_pre(json_data, 'cno', 'cname', 'credit', 'chour', 'pre_cno', 'pre_cname')
    result = db.getAllCourseInfoV2(json_data)
    ret = pack_rows(result, 'cno', 'cname', 'credit', 'chour', 'pre_cno', 'pre_cname')
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/teach/v2/all', methods=["POST"])
def getAllTeachInfoV2():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    dict_fuzzy_search_pre(json_data, 'cid', 'course_name', 'college_name', 'mname', 'tname', 'year', 'semester')
    result = db.getAllTeachInfoV2(json_data)
    ret = pack_rows(result, 'cid', 'course_name', 'college_name', 'mname', 'tname', 'year', 'semester')
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/elective/all', methods=["POST"])
def getAllElectiveInfo():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    json_data = request.get_json()
    dict_fuzzy_search_pre(json_data, 'cid', 'sname', 'course_name', 'college_name',
                          'mname', 'year', 'semester', 'score', 'gp', 'type')
    result = db.getAllElectiveInfo(json_data)
    ret = pack_rows(result, 'cid', 'sname', 'course_name', 'college_name',
                    'mname', 'year', 'semester', 'score', 'gp', 'type')
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/statement/student_elective')
def studentElectiveStatement():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    if dict_includes_keys(request.args, 'sno', 'year', 'semester'):
        result = db.studentElectiveStatement(request.args.get(
            'sno', str), request.args.get('year', int), request.args.get('semester', int))
        ret = pack_rows(result, 'cid', 'cname', 'credit', 'chour', 'score')
        return {'code': 0, 'data': ret, 'msg': 'success'}
    else:
        return {"code": -1, "msg": "缺少sno或year或semester"}


@Api.route('/statement/teacher_teach')
def teacherTeachStatement():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    if dict_includes_keys(request.args, 'tno', 'year', 'semester'):
        result = db.teacherTeachStatement(request.args.get('tno', str), request.args.get(
            'year', int), request.args.get('semester', int))
        ret = pack_rows(result, 'cid', 'cname', 'mname', 'credit', 'chour', 'pre_cname')
        return {'code': 0, 'data': ret, 'msg': 'success'}
    else:
        return {"code": -1, "msg": "缺少tno或year或semester"}


@Api.route('/statement/class_gpa')
def classGPAStatement():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    if dict_includes_keys(request.args, 'cno', 'year', 'semester', 'order_row'):
        result = db.classGPAStatement(request.args.get('cno', str), request.args.get(
            'year', int), request.args.get('semester', int), request.args.get('order_row', str))
        ret = pack_rows(result, 'sno', 'sname', 'gpa')
        return {'code': 0, 'data': ret, 'msg': 'success'}
    else:
        return {"code": -1, "msg": "缺少cno或year或semester"}


@Api.route('/statement/teacher_title')
def teacherTitleStatement():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    result = db.teacherTitleStatement()
    ret = pack_rows(result, 'cname', 'assistant', 'lecturer', 'associate_professor', 'professor')
    return {'code': 0, 'data': ret, 'msg': 'success'}


@Api.route('/statement/college_course')
def collegeCourseStatement():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    if dict_includes_keys(request.args, 'college_name'):
        result = db.collegeCourseStatement(request.args.get('college_name', type=str))
        ret = pack_rows(result, 'cname', 'chour', 'pre_cname', 'pre_chour')
        return {'code': 0, 'data': ret, 'msg': 'success'}
    else:
        return {"code": -1, "msg": "缺少college_name"}


@Api.route('/statement/teacher_course')
def teacherCourseStatement():
    session_status, res = check_session(session, expire=True, roles=[3])
    if not session_status:
        return res
    if dict_includes_keys(request.args, 'year', 'semester'):
        result = db.teacherCourseStatement(request.args.get('year', int), request.args.get('semester', int))
        ret = pack_rows(result, 'tno', 'tname', 'cnum', 'chour')
        return {'code': 0, 'data': ret, 'msg': 'success'}
    else:
        return {"code": -1, "msg": "缺少year或semester"}


@Api.route('/student/home/course_plan')
def getStudentCoursePlan():
    session_status, res = check_session(session, expire=True, roles=[1])
    if not session_status:
        return res
    if dict_includes_keys(request.args, 'year', 'semester'):
        result = db.getStudentCoursePlan(request.args.get('year', type=int), request.args.get(
            'semester', type=str), session.get('username'))
        ret = pack_rows(result, 'cid', 'cname', 'credit', 'chour', 'pre_cname')
        return {'code': 0, 'data': ret, 'msg': 'success'}
    else:
        return {"code": -1, "msg": "缺少year或semester"}


@Api.route('/student/home/elective_course', methods=["POST"])
def electiveCourse():
    session_status, res = check_session(session, expire=True, roles=[1])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'cid'):
        allow, pre_cname = db.checkElective(json_data['cid'], session.get('username'))
        if not allow:
            return {'code': 1, 'msg': '选课失败，请先选修先行课' + pre_cname}
        else:
            if db.checkTime(json_data['cid']):
                if db.electiveCourse(json_data['cid'], session.get('username')):
                    return {'code': 0, 'msg': '选课成功'}
                else:
                    return {'code': 3, 'msg': '选课失败'}
            return {'code': 2, 'msg': '选课失败，当前时间不可选修该课程'}

    else:
        return {"code": -1, "msg": "缺少cid"}


@Api.route('/student/home/my_courses')
def studentMyCourses():
    session_status, res = check_session(session, expire=True, roles=[1])
    if not session_status:
        return res
    if dict_includes_keys(request.args, 'year', 'semester'):
        search_args = request.args.to_dict()
        dict_fuzzy_search_pre(search_args, 'year', 'semester')
        # print(search_args)
        result = db.studentMyCourses(search_args.get('year'), search_args.get('semester'), session.get('username'))
        ret = pack_rows(result, 'year', 'semester', 'cid', 'cname', 'credit', 'score', 'gp')
        return {'code': 0, 'data': ret, 'msg': 'success'}
    else:
        return {"code": -1, "msg": "缺少sno或year或semester"}


@Api.route('/student_score/upload', methods=["POST"])
def uploadStudentScore():
    session_status, res = check_session(session, expire=True, roles=[2])
    if not session_status:
        return res
    json_data = request.get_json()
    if dict_includes_keys(json_data, 'course_id', 'student_scores'):
        for s in json_data['student_scores']:
            if not dict_includes_keys(s, 'sno', 'score'):
                return {"code": -1, "msg": "缺少sno或score"}
        if db.checkCourseTeacher(json_data['course_id'], session.get('username')):
            if db.updateStudentScores(json_data['course_id'], json_data['student_scores']):
                return {'code': 0, 'msg': 'success'}
            else:
                return {'code': 2, 'msg': '批量录入学生成绩失败'}
        else:
            return {'code': 1, 'msg': '批量录入学生成绩失败，无法录入非本人教授课程的学生成绩'}
    else:
        return {"code": -1, "msg": "缺少course_id或student_scores"}


@Api.route('/teacher/home/student_score')
def getStudentScore():
    session_status, res = check_session(session, expire=True, roles=[2])
    if not session_status:
        return res
    search_args = request.args.to_dict()
    dict_fuzzy_search_pre(search_args, 'cid', 'year', 'semester')
    if search_args['cid'] == '%' or db.checkCourseTeacher(search_args['cid'], session.get('username')):
        result = db.getStudentScore(search_args, session.get('username'))
        ret = pack_rows(result, 'cid', 'sname', 'course_name', 'year', 'semester', 'score', 'gp')
        return {'code': 0, 'data': ret, 'msg': 'success'}
    else:
        return {'code': 1, 'msg': '查询学生成绩失败，无法查询非本人教授课程的学生成绩'}


@Api.route('/teacher/home/student_elective_info')
def getStudentElectiveInfo():
    session_status, res = check_session(session, expire=True, roles=[2])
    if not session_status:
        return res
    if request.args.get('sno', False):
        result = db.getStudentElectiveInfo(request.args.get('sno'))
        ret = pack_rows(result, 'cid', 'course_name', 'year', 'semester', 'score', 'gp')
        return {'code': 0, 'data': ret, 'msg': 'success'}
    else:
        return {'code': 1, 'msg': '缺少sno'}
