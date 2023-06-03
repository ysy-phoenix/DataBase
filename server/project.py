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
        # case1 主码重复
        project = Project.query.filter_by(No=post_data.get("projectNo")).first()
        if project:
            response["status"] = False
            response["message"] = "项目号重复！"
            return jsonify(response)

        # case2 数据类型不符或者约束不满足
        try:
            add_project(
                No=post_data.get("projectNo"),
                name=post_data.get("name"),
                source=post_data.get("source"),
                type=post_data.get("type"),
                funds=post_data.get("funds"),
                startYear=post_data.get("startYear"),
                endYear=post_data.get("endYear"),
            )
            response["message"] = "项目添加成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "项目添加失败！数据类型不符或者约束不满足！"
    elif request.method == "GET":
        projects = Project.query.all()
        response["projects"] = [project.json() for project in projects]
    return jsonify(response)


@project_blueprint.route(
    "/projects/<projectNo>", methods=["PUT", "POST", "GET", "DELETE"]
)
def edit_project_take(projectNo):
    response = {"status": True}
    if request.method == "PUT":  # 增加项目承担
        post_data = request.get_json()
        project = TakeProject.query.filter_by(
            projectNo=post_data.get("projectNo"), teacherNo=post_data.get("teacherNo")
        ).first()

        # case1 主码重复
        if project:
            response["status"] = False
            response["message"] = "项目承担重复！"
            return jsonify(response)

        # case2 排名重复
        project = TakeProject.query.filter_by(
            projectNo=post_data.get("projectNo"), rank=post_data.get("rank")
        ).first()
        if project:
            response["status"] = False
            response["message"] = "排名重复！"
            return jsonify(response)

        # case3 数据类型不符或约束不满足
        try:
            add_take_project(
                teacherNo=post_data.get("teacherNo"),
                projectNo=projectNo,
                rank=post_data.get("rank"),
                takeFunds=post_data.get("takeFunds"),
            )
            response["message"] = "承担项目登记成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "承担项目登记失败！数据类型不符或者约束不满足！"
    elif request.method == "POST":  # 修改项目信息
        post_data = request.get_json()
        project = Project.query.filter_by(No=projectNo).first()
        if not project:
            response["status"] = False
            response["message"] = "项目不存在！"
            return jsonify(response)
        try:
            project.name = post_data.get("name")
            project.source = post_data.get("source")
            project.type = post_data.get("type")
            project.funds = post_data.get("funds")
            project.startYear = post_data.get("startYear")
            project.endYear = post_data.get("endYear")
            db.session.commit()
            response["message"] = "项目修改成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "项目修改失败！数据类型不符或者约束不满足！"
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


@project_blueprint.route(
    "/projects/<projectNo>/<teacherNo>", methods=["POST", "DELETE"]
)
def update_delete_takes(projectNo, teacherNo):
    response = {"status": True}
    take = TakeProject.query.filter_by(projectNo=projectNo, teacherNo=teacherNo).first()
    if not take:
        response["status"] = False
        response["message"] = "项目承担不存在！"
        return jsonify(response)

    if request.method == "POST":  # 修改项目承担
        post_data = request.get_json()

        # case1 排名重复
        project = TakeProject.query.filter_by(
            projectNo=post_data.get("projectNo"), rank=post_data.get("rank")
        ).first()
        if project.teacherNo != post_data.get("teacherNo"):
            response["status"] = False
            response["message"] = "排名重复！"
            return jsonify(response)

        try:
            take.rank = post_data.get("rank")
            take.takeFunds = post_data.get("takeFunds")
            db.session.commit()
            response["message"] = "项目承担修改成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "项目承担修改失败！数据类型不符或者约束不满足！"
            return jsonify(response)
    elif request.method == "DELETE":  # 删除项目承担
        try:
            db.session.delete(take)
            db.session.commit()
            response["message"] = "项目承担删除成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "项目承担删除失败！"
    return jsonify(response)


@project_blueprint.route("/projects/check/<projectNo>", methods=["GET"])
def check_funds(projectNo):
    response = {"status": True}
    project = Project.query.filter_by(No=projectNo).first()
    if not project:
        response["status"] = False
        response["message"] = "检查失败：项目不存在！"
        return jsonify(response)
    sum = 0.0
    takes = TakeProject.query.filter_by(projectNo=projectNo).all()
    for take in takes:
        sum += take.takeFunds
    if sum == project.funds:
        response["message"] = "项目经费核算成功！"
    else:
        response["status"] = False
        response["message"] = "项目经费核算失败！登记经费总额为 {}，实际经费总额为 {}！".format(
            project.funds, sum
        )
    return jsonify(response)
