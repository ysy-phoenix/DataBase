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
        post_course = post_data.get("course")
        teachers = post_data.get("teachers")

        # case1 主码重复
        course = Course.query.filter_by(No=post_data.get("courseNo")).first()
        if course:
            response["status"] = False
            response["message"] = "课程号重复！"
            return jsonify(response)

        # case2 主讲教师检查
        if len(teachers) == 0:
            response["status"] = False
            response["message"] = "必须提供主讲教师信息！"
            return jsonify(response)

        teacherNo = set()
        years = set()
        semesters = set()
        sum = 0
        for teacher in teachers:
            _teacher = Teacher.query.filter_by(No=teacher["teacherNo"]).first()
            if not _teacher:
                response["status"] = False
                response["message"] = "教师 " + teacher["teacherNo"] + " 不存在！"
                return jsonify(response)
            if teacher.get("teacherNo") in teacherNo:
                response["status"] = False
                response["message"] = "主讲教师 " + teacher["teacherNo"] + " 重复！"
                return jsonify(response)
            teacherNo.add(teacher.get("teacherNo"))
            years.add(teacher.get("year"))
            if len(years) >= 2:
                response["status"] = False
                response["message"] = "年份不一致！"
                return jsonify(response)
            semesters.add(teacher.get("semester"))
            if len(semesters) >= 2:
                response["status"] = False
                response["message"] = "学期不一致！"
                return jsonify(response)
            sum += int(teacher.get("takeCreditHour"))

        if sum != int(post_course.get("creditHour")):
            response["status"] = False
            response["message"] = "学时核算不正确！申报学时为：{}，实际总和为 {}。".format(
                post_course.get("creditHour"),
                sum,
            )
            return jsonify(response)

        # case3 数据类型不符或者约束不满足
        try:
            add_course(
                No=post_course.get("courseNo"),
                name=post_course.get("name"),
                creditHour=post_course.get("creditHour"),
                type=post_course.get("type"),
            )
            response["message"] = "课程添加成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "课程添加失败！数据类型不符或者约束不满足！"

        for teacher in teachers:
            try:
                add_teach_course(
                    teacherNo=teacher.get("teacherNo"),
                    courseNo=post_course.get("courseNo"),
                    year=teacher.get("year"),
                    semester=teacher.get("semester"),
                    takeCreditHour=teacher.get("takeCreditHour"),
                )
            except Exception as e:
                print(e)
                db.session.rollback()
                response["status"] = False
                response["message"] = "主讲教师登记失败！数据类型不符或者约束不满足！"
                return jsonify(response)
        db.session.commit()
        response["message"] = "课程登记成功！"

    elif request.method == "GET":
        courses = Course.query.all()
        response["courses"] = [course.json() for course in courses]
    return jsonify(response)


@course_blueprint.route("/courses/<courseNo>", methods=["POST", "GET", "DELETE"])
def edit_course_teacher(courseNo):
    response = {"status": True}
    if request.method == "POST":  # 修改课程信息
        post_data = request.get_json()
        post_course = post_data.get("course")
        teachers = post_data.get("teachers")

        course = Course.query.filter_by(No=courseNo).first()

        # 主讲教师检查
        if len(teachers) == 0:
            response["status"] = False
            response["message"] = "必须提供主讲教师信息！"
            return jsonify(response)

        old_teachers = TeachCourse.query.filter_by(courseNo=courseNo).all()
        delete_teachers = set([teacher.teacherNo for teacher in old_teachers])
        add_teachers = set()

        teacherNo = set()
        years = set()
        semesters = set()
        sum = 0
        for teacher in teachers:
            _teacher = Teacher.query.filter_by(No=teacher["teacherNo"]).first()
            if not _teacher:
                response["status"] = False
                response["message"] = "教师 " + teacher["teacherNo"] + " 不存在！"
                return jsonify(response)
            if teacher.get("teacherNo") in teacherNo:
                response["status"] = False
                response["message"] = "主讲教师 " + teacher["teacherNo"] + " 重复！"
                return jsonify(response)
            teacherNo.add(teacher.get("teacherNo"))
            years.add(teacher.get("year"))
            if len(years) >= 2:
                response["status"] = False
                response["message"] = "年份不一致！"
                return jsonify(response)
            semesters.add(teacher.get("semester"))
            if len(semesters) >= 2:
                response["status"] = False
                response["message"] = "学期不一致！"
                return jsonify(response)
            if teacher["teacherNo"] in delete_teachers:
                delete_teachers.remove(teacher["teacherNo"])
            else:
                add_teachers.add(teacher["teacherNo"])
            sum += int(teacher.get("takeCreditHour"))

        if sum != int(post_course.get("creditHour")):
            response["status"] = False
            response["message"] = "学时核算不正确！申报学时为：{}，实际总和为 {}。".format(
                post_course.get("creditHour"),
                sum,
            )
            return jsonify(response)

        try:
            course.name = post_course.get("name")
            course.creditHour = post_course.get("creditHour")
            course.type = post_course.get("type")
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "课程修改失败！数据类型不符或者约束不满足！"

        for teacher in delete_teachers:
            teacher = TeachCourse.query.filter_by(
                courseNo=courseNo, teacherNo=teacher
            ).first()
            db.session.delete(teacher)

        for teacher in teachers:
            try:
                if teacher["teacherNo"] in add_teachers:
                    add_teach_course(
                        teacherNo=teacher.get("teacherNo"),
                        courseNo=courseNo,
                        year=teacher.get("year"),
                        semester=teacher.get("semester"),
                        takeCreditHour=teacher.get("takeCreditHour"),
                    )
                else:
                    update_teacher = TeachCourse.query.filter_by(
                        courseNo=courseNo, teacherNo=teacher["teacherNo"]
                    ).first()
                    update_teacher.year = teacher.get("year")
                    update_teacher.semester = teacher.get("semester")
                    update_teacher.takeCreditHour = teacher.get("takeCreditHour")
            except Exception as e:
                print(e)
                db.session.rollback()
                response["status"] = False
                response["message"] = "主讲教师修改失败！数据类型不符或者约束不满足！"
                return jsonify(response)
        response["message"] = "课程信息更新成功！"
        db.session.commit()

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


@course_blueprint.route("/courses/teacher/<teacherNo>", methods=["GET"])
def query_courses(teacherNo):
    response = {"status": True}
    if request.method == "GET":
        teacher = Teacher.query.filter_by(No=teacherNo).first()
        if not teacher:
            response["status"] = False
            response["message"] = "查询失败：教师工号不存在！"
            return jsonify(response)
        results = (
            db.session.query(Course, TeachCourse)
            .join(Course, Course.No == TeachCourse.courseNo)
            .filter(TeachCourse.teacherNo == teacherNo)
            .all()
        )
        response["courses"] = [result.Course.json() for result in results]
        response["message"] = "查询成功！"
    return jsonify(response)
