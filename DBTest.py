# coding=utf-8
import MySQLdb
import CourseInfo

hostName = '39.106.138.103'
user = 'root'
password = "123456"
database = "cource_db"

if __name__ == '__main__':
    # 打开数据库连接
    db = MySQLdb.connect(hostName, user, password, database)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # 使用execute方法执行SQL语句
    cursor.execute("SELECT VERSION()")

    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()

    print "Database version : %s " % data

    # 关闭数据库连接
    db.close()


def create_table(cursor):
    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

    # 创建数据表SQL语句
    sql = """CREATE TABLE EMPLOYEE (
             FIRST_NAME  CHAR(20) NOT NULL,
             LAST_NAME  CHAR(20),
             AGE INT,  
             SEX CHAR(1),
             INCOME FLOAT )"""
    cursor.execute(sql)


def insert_or_update_course(courses):
    """
    插入一条课程信息(存在则不插入，不存在则插入)
    :param courses:    课程信息数组
    :return:
    """
    db = MySQLdb.connect(hostName, user, password, database, charset='utf8')
    cursor = db.cursor()
    try:
        for course in courses:
            # print type(course.course_english_name)
            sql = """INSERT INTO course(
                          study_id, course_order, course_chinese_name, course_english_name, credit, type, score, course_number)
                           VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s") 
                           ON DUPLICATE KEY UPDATE score = score""" % \
                  (course.study_id.encode('utf-8')
                   , course.course_order.encode('utf-8')
                   , course.course_chinese_name.encode('utf-8')
                   , course.course_english_name.encode('utf-8')
                   , course.course_credit.encode('utf-8')
                   , course.course_type.encode('utf-8')
                   , course.course_score.encode('utf-8')
                   , course.course_number.encode('utf-8'))
            print sql
            cursor.execute(sql)
            db.commit()
        db.close()
        return True
    except Exception, e:  # 插入出错则回滚
        db.rollback()
        db.close()
        print e
        return False


def query_course(study_id):
    """
    根据学号查询课程信息，并吧课程信息放到一个数组里面
    :param study_id:
    :return:
    """
    db = MySQLdb.connect(hostName, user, password, database, charset='utf8')
    cursor = db.cursor()
    sql = """select * from course WHERE study_id = %s""" % study_id
    courses = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            course = CourseInfo.CourseInfo(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            courses.append(course)
    except Exception, e:
        print e
        return []
    return courses

def query_user(study_id):
    db = MySQLdb.connect(hostName, user, password, database, charset='utf8')
    cursor = db.cursor()
    sql = """select * from user WHERE study_id = %s""" % study_id
    JSESSIONID = u""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 获取所有记录
        results = cursor.fetchall()
        for row in results:
            JSESSIONID = row[1]
    except Exception, e:
        JSESSIONID = u""
        print e
    return JSESSIONID


def insert_or_update_user(study_id, JSESSIONID):
    """
    插入或更新用户
    :param study_id:
    :param JSESSIONID:
    :return:
    """
    db = MySQLdb.connect(hostName, user, password, database, charset='utf8')
    cursor = db.cursor()
    sql = """insert into user(study_id, JSESSIONID) VALUES('%s', '%s') ON DUPLICATE KEY UPDATE JSESSIONID='%s'""" \
          % (study_id.encode('utf-8'), JSESSIONID.encode('utf-8'), JSESSIONID.encode('utf-8'))
    try:
        cursor.execute(sql)
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    db.close()
