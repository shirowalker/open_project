# 建表语句

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS course;

CREATE TABLE user(
  study_id VARCHAR(20) PRIMARY KEY ,
  JSESSIONID VARCHAR(100) NOT NULL
);

CREATE TABLE course(
  study_id VARCHAR(20),
  course_order VARCHAR(5),
  course_chinese_name VARCHAR(50) ,
  course_english_name VARCHAR(200),
  credit NUMERIC(2, 1),
  type VARCHAR(20),
  score NUMERIC(4, 0),
  course_number VARCHAR(10),
  PRIMARY KEY (study_id, course_number)
)