# coding=utf-8
class CourseInfo:
    study_id = ""               # 学号
    course_score = 0.0          # 课程分数
    course_credit = 0.0         # 课程学分
    course_english_name = ""    # 课程英文名
    course_chinese_name = ""    # 课程中文名
    course_order = ""           # 课序号
    course_type = ""            # 课程类型
    course_number = ""          # 课程号
    semester = 0                # 学期

    def __init__(self, study_id, course_order, course_chinese_name, course_english_name, course_credit, course_type,
                 course_score, course_number):
        self.study_id = study_id
        self.course_order = course_order
        self.course_chinese_name = course_chinese_name
        self.course_english_name = course_english_name
        self.course_credit = course_credit
        self.course_type = course_type
        self.course_score = course_score
        self.course_number = course_number


    def set_semester(self, semester):
        self.semester = semester


    def get_info(self):
        return str(self.course_chinese_name.encode('gb2312')) + ": " + str(self.course_credit).encode('gb2312') + "---" + str(self.course_score).encode('gb2312')
        # return str(self.course_chinese_name.encode('utf-8')) + ": " + str(self.course_credit).encode('utf-8') + "---" + str(self.course_score).encode('utf-8')
