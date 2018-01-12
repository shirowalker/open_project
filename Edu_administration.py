# coding=gb2312
import codecs
import requests
import re
import CourseInfo
import DBTest

baseUrl = 'http://zhjw.dlut.edu.cn/'
url = 'http://zhjw.dlut.edu.cn/loginAction.do'
mainFrameUrl = 'http://zhjw.dlut.edu.cn/menu/mainFrame.jsp'
# baseScoreUrl = 'http://zhjw.dlut.edu.cn/gradeLnAllAction.do?type=ln&oper=fa'
baseScoreUrl = 'http://zhjw.dlut.edu.cn/gradeLnAllAction.do?type=ln&oper=qb'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
    'Host': 'zhjw.dlut.edu.cn',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
}


def login(usn, psd):
    """
    登录函数（本地cookie还有效则用本地cookie，无效则请求登录并获得cookie）
    :param usn: 用户名
    :param psd: 密码
    :return: 返回cookie
    """
    cookies = {}
    data = {}
    JSESSIONID = DBTest.query_user(usn)
    # 在数据库中有cookie的情况下，测试一下cookie通不通
    # 如果连接的通，说明本地的cookie还有效，直接返回就好了
    if JSESSIONID != u"" and test_connect(JSESSIONID=JSESSIONID):
        cookies["JSESSIONID"] = JSESSIONID
        return cookies

    # 如果本地无记录或者说本地cookie已经失效，则重新获取cookie
    data['zjh'] = usn
    data['mm'] = psd
    response = requests.post(url=url, data=data, headers=headers)
    cookies['JSESSIONID'] = response.cookies.values()[0]
    DBTest.insert_or_update_user(usn, cookies['JSESSIONID'])
    return cookies


def test_connect(JSESSIONID):
    """
    测试cookie是否还有效
    :param JSESSIONID:
    :return: 测试成功则返回True
    """
    c = {'JSESSIONID': JSESSIONID}
    response = requests.get(url=baseScoreUrl, headers=headers, cookies=c)
    print response.status_code
    if response.status_code != 200:
        return False
    title = re.findall('<title>(.*?)</title>', response.text, re.I | re.S)
    print type(title[0])
    if title[0] == u'登录超时':
        return False
    return True


def get_score(study_id, cookies):
    """
    通过学号和cookie获取成绩，并插入到数据库当中
    :param study_id:
    :param cookies:
    :return:
    """
    response = requests.get(url=baseScoreUrl, headers=headers, cookies=cookies)
    print response.text
    results = re.findall('name="lnqbIfra" src="(.*?)#', response.text, re.I | re.S)
    if len(results) == 0:
        print '未查询到成绩，请先完成教学评估'
        return False
    newUrl_back = results[0]

    newUrl = baseUrl + newUrl_back
    response = requests.get(url=newUrl, headers=headers, cookies=cookies)
    if response.status_code == 200:
        deal_data(study_id, response.text)
    else:
        print '获取成绩失败'


def deal_data(study_id, html_text):
    """
    处理爬到的成绩数据，并插入到数据库当中
    :param study_id:
    :param html_text:
    :return:
    """
    first = re.findall('<tr class="odd"(.*?)</tr>', html_text, re.S | re.I)
    if len(first) == 0:
        print '没有抓到数据'
        return
    first[0].encode('gb2312')
    # f = codecs.open('data.txt', 'w', 'gb2312')

    courses = []
    for course_item in first:
        second = re.findall('>(.*?)</td>', course_item, re.S | re.I)
        print second[0]
        course = CourseInfo.CourseInfo(study_id,
                                       "".join(second[1].split()),
                                       "".join(second[2].split()),
                                       "".join(second[3].split()),
                                       "".join(second[4].split()),
                                       "".join(second[5].split()),
                                       "".join(re.findall('"center">(.*?)&nbsp;', second[6])[0]),
                                       "".join(re.findall('"center">(.*)', second[0], re.S | re.I)[0].split()))
        courses.append(course)
        # f.write(course.get_info())
        # f.write('\n')
    if DBTest.insert_or_update_course(courses):
        print "插入到数据库成功"
    else:
        print "插入到数据库失败"

        # print total_score
        # print total_credit
        # print total_score * 1.0 / total_credit

        # f.close()


def calculate_avr_score(study_id, excepts):
    """
    计算加权均分
    :param study_id:        学号
    :param excepts:         要去除的科目的索引
    :return:
    """
    total_score = 0
    total_credit = 0
    courses = DBTest.query_course(study_id=study_id)
    total_num = 0
    for index, course in enumerate(courses):
        if course.course_type == u'必修' and index + 1 not in excepts:
            total_score = total_score + float(course.course_score) * float(course.course_credit)
            total_credit = total_credit + float(course.course_credit)
            print str(index + 1) + "." + str(course.get_info())
            total_num = total_num + 1
    print "总共计算的科目数为：" + str(total_num)
    if total_credit != 0:
        return total_score / total_credit
    return 0


def query_course(study_id):
    courses = DBTest.query_course(study_id)
    for course in courses:
        print course.get_info()


# username = "201592362"
# password = "19970825"
username = '201592038'
password = 'qq4538'


# username = '201592442'
# password = '19970408'

# print login(username, password)
# test_connect(cookie['JSESSIONID'])
# get_score(username, login(usn=username, psd=password))
# print "".join({'已选科目的加权均分为：', str(calculate_avr_score(username, [28, 44, 47, 48, 49, 40, 41, 42, 29, 31, 32, 19, 20, 21, 22, 9, 10, 13, 14, 15, 16, 45, 46]))})
# getScore(username, 'http://zhjw.dlut.edu.cn/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=6747', c)
# getMainFrame('JSESSIONID=uxzUQ2sZKNaL6b_icFZZv')

def show_operator():
    print "你可以执行以下操作:"
    print '1.查询所有科目信息\t\t' + '2.查询必修科目加权\t\t'
    print '3.计算加权去除科目\t\t' + '4.在线获取成绩信息\t\t'
    print "5.exit"


while True:
    usn = str(input("Please input your study id: "))
    psd = str(raw_input("Please input your psd:"))
    if login(usn=usn, psd=psd):
        print '登录成功'
        break
    else:
        print '请重新输入！！'

show_operator()
expects = []
operator = input("请输入操作：")
while operator != 5:
    if operator == 1:
        query_course(usn)
    elif operator == 2:
        print '加权均分：' + str(calculate_avr_score(usn, excepts=expects))
    elif operator == 3:
        expects = []
        while True:
            print '加权均分：' + str(calculate_avr_score(usn, excepts=expects))
            exps = input("请输入要去除科目的序号，逗号隔开（输入-1结束）：")
            if type(exps) == type(1):
                if exps == -1:
                    break
                expects.append(exps)
            else:
                for i in exps:
                    expects.append(int(i))

    elif operator == 4:
        get_score(usn, login(usn, psd))
    show_operator()
    operator = input("请输入操作：")

print '程序退出'
