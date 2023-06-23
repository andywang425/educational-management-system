from datetime import datetime
import hashlib
import secrets


def md5(str, salt='SUEP'):
    return hashlib.md5(f'{salt}{str}'.encode()).hexdigest()


def generate_secret_key():
    return '49865fe7a5efc33dbd4bed465f441c7dcaf85ffc420e234ca6c9a6239c319c0a'
    # 可以改为随机密钥，如下：
    # return secrets.token_hex(32)


def dict_includes_keys(dict, *keys):
    for k in keys:
        if k not in dict:
            return False
    return True


def check_session(session, expire, roles):
    if expire and not session.get('role'):
        return (False, {'code': 302, 'msg': '登录信息过期，请重新登录'})
    if roles and session['role'] not in roles:
        return (False, {"code": 403, "msg": "非法访问"})
    return (True, None)


def pack_row(resultRow, *keys):
    ret = {}
    for i in range(len(resultRow)):
        ret[keys[i]] = resultRow[i]
    return ret


def pack_rows(resultRows, *keys):
    ret = []
    for row in resultRows:
        obj = {}
        for i in range(len(row)):
            obj[keys[i]] = row[i]
        ret.append(obj)
    return ret


def dict_fuzzy_search_pre(dict, *keys):
    for k in keys:
        if k not in dict or not dict[k] or dict[k] == 'any':
            dict[k] = '%'


def get_elective_semester():
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month

    if 3 <= month <= 8:
        return [year, 1]
    else:
        if month > 8:
            return [year, 2]
        else:
            return [year - 1, 2]
