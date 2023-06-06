from flask import Blueprint, jsonify, request
from utils import *
from db import *

project_blueprint = Blueprint("project", __name__)

# PUT DELETE POST GET 增删改查


@project_blueprint.route("/projects", methods=["PUT", "GET"])
def all_projects():
    response = {"status": True}
    if request.method == "PUT":
        post_data = request.get_json()
        post_project = post_data.get("project")
        takes = post_data.get("takes")
        # case1 主码重复
        project = Project.query.filter_by(No=post_project.get("projectNo")).first()
        if project:
            response["status"] = False
            response["message"] = "项目号重复！"
            return jsonify(response)

        # case2 负责人检查
        if len(takes) == 0:
            response["status"] = False
            response["message"] = "必须提供负责人信息！"
            return jsonify(response)

        teacherNo = set()
        ranks = set()
        sum = 0.0
        for take in takes:
            teacher = Teacher.query.filter_by(No=take["teacherNo"]).first()
            if not teacher:
                response["status"] = False
                response["message"] = "教师 " + take["teacherNo"] + " 不存在！"
                return jsonify(response)
            if take.get("teacherNo") in teacherNo:
                response["status"] = False
                response["message"] = "负责人 " + take["teacherNo"] + " 重复！"
                return jsonify(response)
            if take.get("rank") in ranks:
                response["status"] = False
                response["message"] = "项目排名重复！"
                return jsonify(response)
            teacherNo.add(take.get("teacherNo"))
            ranks.add(take.get("rank"))
            sum += float(take.get("takeFunds"))

        if sum != float(post_project.get("funds")):
            response["status"] = False
            response["message"] = "经费核算不正确！申报承担经费为：{}，承担总和为 {}。".format(
                post_project.get("funds"),
                sum,
            )
            return jsonify(response)

        # case3 数据类型不符或者约束不满足
        try:
            add_project(
                No=post_project.get("projectNo"),
                name=post_project.get("name"),
                source=post_project.get("source"),
                type=post_project.get("type"),
                funds=post_project.get("funds"),
                startYear=post_project.get("startYear"),
                endYear=post_project.get("endYear"),
            )
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "项目添加失败！数据类型不符或者约束不满足！"
            return jsonify(response)

        for take in takes:
            try:
                add_take_project(
                    teacherNo=take.get("teacherNo"),
                    projectNo=post_project.get("projectNo"),
                    rank=take.get("rank"),
                    takeFunds=take.get("takeFunds"),
                )
            except Exception as e:
                print(e)
                db.session.rollback()
                response["status"] = False
                response["message"] = "项目负责人登记失败！数据类型不符或者约束不满足！"
                return jsonify(response)
        db.session.commit()
        response["message"] = "承担项目登记成功！"

    elif request.method == "GET":
        projects = Project.query.all()
        response["projects"] = [project.json() for project in projects]
    return jsonify(response)


@project_blueprint.route("/projects/<projectNo>", methods=["POST", "GET", "DELETE"])
def edit_project_take(projectNo):
    response = {"status": True}
    if request.method == "POST":  # 修改项目信息
        post_data = request.get_json()
        post_project = post_data.get("project")
        takes = post_data.get("takes")

        project = Project.query.filter_by(No=projectNo).first()

        if len(takes) == 0:
            response["status"] = False
            response["message"] = "必须提供负责人信息！"
            return jsonify(response)

        old_takes = TakeProject.query.filter_by(projectNo=projectNo).all()
        delete_takes = set([take.teacherNo for take in old_takes])
        add_takes = set()

        # 负责人检查
        teacherNo = set()
        ranks = set()
        sum = 0.0
        for take in takes:
            teacher = Teacher.query.filter_by(No=take["teacherNo"]).first()
            if not teacher:
                response["status"] = False
                response["message"] = "教师 " + take["teacherNo"] + " 不存在！"
                return jsonify(response)
            if take.get("teacherNo") in teacherNo:
                response["status"] = False
                response["message"] = "负责人 " + take["teacherNo"] + " 重复！"
                return jsonify(response)
            if take.get("rank") in ranks:
                response["status"] = False
                response["message"] = "项目排名重复！"
                return jsonify(response)
            teacherNo.add(take.get("teacherNo"))
            ranks.add(take.get("rank"))
            if take["teacherNo"] in delete_takes:
                delete_takes.remove(take["teacherNo"])
            else:
                add_takes.add(take["teacherNo"])
            sum += float(take.get("takeFunds"))

        if sum != float(post_project.get("funds")):
            response["status"] = False
            response["message"] = "经费核算不正确！申报承担经费为：{}，承担总和为 {}。".format(
                post_project.get("funds"),
                sum,
            )
            return jsonify(response)

        try:
            project.name = post_project.get("name")
            project.source = post_project.get("source")
            project.type = post_project.get("type")
            project.funds = post_project.get("funds")
            project.startYear = post_project.get("startYear")
            project.endYear = post_project.get("endYear")
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "项目修改失败！数据类型不符或者约束不满足！"

        for take in delete_takes:
            take = TakeProject.query.filter_by(
                projectNo=projectNo, teacherNo=take
            ).first()
            db.session.delete(take)

        for take in takes:
            try:
                if take["teacherNo"] in add_takes:
                    add_take_project(
                        teacherNo=take.get("teacherNo"),
                        projectNo=projectNo,
                        rank=take.get("rank"),
                        isCotake=take.get("isCotake"),
                    )
                else:
                    update_take = TakeProject.query.filter_by(
                        projectNo=projectNo, teacherNo=take["teacherNo"]
                    ).first()
                    update_take.rank = take.get("rank")
                    update_take.takeFunds = take.get("takeFunds")
            except Exception as e:
                print(e)
                db.session.rollback()
                response["status"] = False
                response["message"] = "项目负责人修改失败！数据类型不符或者约束不满足！"
                return jsonify(response)
        response["message"] = "项目承担信息更新成功！"
        db.session.commit()

    elif request.method == "DELETE":  # 删除项目
        project = Project.query.filter_by(No=projectNo).first()
        if not project:
            response["status"] = False
            response["message"] = "项目不存在！"
            return jsonify(response)
        try:
            db.session.delete(project)
            db.session.commit()
            response["message"] = "项目删除成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "项目删除失败！"
    elif request.method == "GET":  # 获取项目承担信息
        takes = TakeProject.query.filter_by(projectNo=projectNo).all()
        response["takes"] = [take.json() for take in takes]
    return jsonify(response)


@project_blueprint.route("/projects/teacher/<teacherNo>", methods=["GET"])
def query_projects(teacherNo):
    response = {"status": True}
    if request.method == "GET":
        teacher = Teacher.query.filter_by(No=teacherNo).first()
        if not teacher:
            response["status"] = False
            response["message"] = "查询失败：教师工号不存在！"
            return jsonify(response)
        results = (
            db.session.query(Project, TakeProject)
            .join(Project, Project.No == TakeProject.projectNo)
            .filter(TakeProject.teacherNo == teacherNo)
            .all()
        )
        response["projects"] = [result.Project.json() for result in results]
        response["message"] = "查询成功！"
    return jsonify(response)
