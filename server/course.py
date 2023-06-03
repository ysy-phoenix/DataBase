from flask import Blueprint, jsonify, request
from utils import *
from db import *

course_blueprint = Blueprint("course", __name__)

# PUT DELETE POST GET 增删改查


@course_blueprint.route("/courses", methods=["PUT", "GET"])
def all_courses():
    response = {"status": True}
    if request.method == "PUT":
        post_data = request.get_json()
        # case1 主码重复
        course = Course.query.filter_by(No=post_data.get("courseNo")).first()
        if course:
            response["status"] = False
            response["message"] = "课程号重复！"
            return jsonify(response)

        # case2 数据类型不符或者约束不满足
        try:
            add_course(
                No=post_data.get("courseNo"),
                name=post_data.get("name"),
                creditHour=post_data.get("creditHour"),
                type=post_data.get("type"),
            )
            response["message"] = "课程添加成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "课程添加失败！数据类型不符或者约束不满足！"
    elif request.method == "GET":
        courses = Course.query.all()
        response["courses"] = [course.json() for course in courses]
    return jsonify(response)


@course_blueprint.route("/courses/<courseNo>", methods=["PUT", "POST", "GET", "DELETE"])
def edit_course_teacher(courseNo):
    response = {"status": True}
    if request.method == "PUT":  # 增加课程主讲
        post_data = request.get_json()
        course = TeachCourse.query.filter_by(
            courseNo=post_data.get("courseNo"), teacherNo=post_data.get("teacherNo")
        ).first()

        # case1 主码重复
        if course:
            response["status"] = False
            response["message"] = "主讲课程重复！"
            return jsonify(response)

        # case2 数据类型不符或约束不满足
        try:
            add_teach_course(
                teacherNo=post_data.get("teacherNo"),
                courseNo=courseNo,
                year=post_data.get("year"),
                semester=post_data.get("semester"),
                takeCreditHour=post_data.get("takeCreditHour"),
            )
            response["message"] = "主讲课程登记成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "主讲课程登记失败！数据类型不符或者约束不满足！"
    elif request.method == "POST":  # 修改课程信息
        post_data = request.get_json()
        course = Course.query.filter_by(No=courseNo).first()
        if not course:
            response["status"] = False
            response["message"] = "课程不存在！"
            return jsonify(response)
        try:
            course.name = post_data.get("name")
            course.creditHour = post_data.get("creditHour")
            course.type = post_data.get("type")
            db.session.commit()
            response["message"] = "课程修改成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "课程修改失败！数据类型不符或者约束不满足！"
    elif request.method == "DELETE":  # 删除课程
        course = Course.query.filter_by(No=courseNo).first()
        if not course:
            response["status"] = False
            response["message"] = "课程不存在！"
            return jsonify(response)
        try:
            db.session.delete(course)
            db.session.commit()
            response["message"] = "课程删除成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "课程删除失败！"
    elif request.method == "GET":  # 获取课程主讲信息
        teachers = TeachCourse.query.filter_by(courseNo=courseNo).all()
        response["teachers"] = [teacher.json() for teacher in teachers]
    return jsonify(response)


@course_blueprint.route("/courses/<courseNo>/<teacherNo>", methods=["POST", "DELETE"])
def update_delete_teachers(courseNo, teacherNo):
    response = {"status": True}
    teacher = TeachCourse.query.filter_by(
        courseNo=courseNo, teacherNo=teacherNo
    ).first()
    if not teacher:
        response["status"] = False
        response["message"] = "主讲课程不存在！"
        return jsonify(response)

    if request.method == "POST":  # 修改课程主讲
        post_data = request.get_json()
        try:
            teacher.year = post_data.get("year")
            teacher.semester = post_data.get("semester")
            teacher.takeCreditHour = post_data.get("takeCreditHour")
            db.session.commit()
            response["message"] = "主讲课程修改成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "主讲课程修改失败！数据类型不符或者约束不满足！"
            return jsonify(response)
    elif request.method == "DELETE":  # 删除课程主讲
        try:
            db.session.delete(teacher)
            db.session.commit()
            response["message"] = "主讲课程删除成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "课程主讲删除失败！"
    return jsonify(response)


@course_blueprint.route("/courses/check/<courseNo>", methods=["GET"])
def check_creditHour(courseNo):
    response = {"status": True}
    course = Course.query.filter_by(No=courseNo).first()
    if not course:
        response["status"] = False
        response["message"] = "检查失败：课程不存在！"
        return jsonify(response)
    sum = 0
    teachers = TeachCourse.query.filter_by(courseNo=courseNo).all()
    for teacher in teachers:
        sum += teacher.takeCreditHour
    if sum == course.creditHour:
        response["message"] = "课程学时核算成功！"
    else:
        response["status"] = False
        response["message"] = "课程学时核算失败！登记总学时为 {}，实际承担总学时为 {}！".format(
            course.creditHour, sum
        )
    return jsonify(response)
