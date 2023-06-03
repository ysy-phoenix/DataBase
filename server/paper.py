from flask import Blueprint, jsonify, request
import re
from utils import *
from db import *

paper_blueprint = Blueprint("paper", __name__)

# PUT DELETE POST GET 增删改查


@paper_blueprint.route("/papers", methods=["PUT", "GET"])
def all_papers():
    response = {"status": True}
    if request.method == "PUT":
        post_data = request.get_json()
        # case1 主码重复
        paper = Paper.query.filter_by(No=post_data.get("paperNo")).first()
        if paper:
            response["status"] = False
            response["message"] = "论文序号重复！"
            return jsonify(response)

        # case2 论文名引号检测
        if re.search("[\"']", post_data.get("name")):
            response["status"] = False
            response["message"] = "论文名称不允许带引号！"
            return jsonify(response)

        # case3 数据类型不符或者约束不满足
        try:
            add_paper(
                No=post_data.get("paperNo"),
                name=post_data.get("name"),
                source=post_data.get("source"),
                publishYear=post_data.get("publishYear"),
                type=post_data.get("type"),
                level=post_data.get("level"),
            )
            response["message"] = "论文添加成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "论文添加失败！数据类型不符或者约束不满足！"
    elif request.method == "GET":
        papers = Paper.query.all()
        response["papers"] = [paper.json() for paper in papers]
    return jsonify(response)


@paper_blueprint.route("/papers/<paperNo>", methods=["PUT", "POST", "GET", "DELETE"])
def edit_paper_author(paperNo):
    response = {"status": True}
    if request.method == "PUT":  # 增加论文发表
        post_data = request.get_json()
        paper = PublishedPapers.query.filter_by(
            paperNo=post_data.get("paperNo"), teacherNo=post_data.get("teacherNo")
        ).first()

        # case1 主码重复
        if paper:
            response["status"] = False
            response["message"] = "论文发表重复！"
            return jsonify(response)

        # case2 排名重复
        paper = PublishedPapers.query.filter_by(
            paperNo=post_data.get("paperNo"), rank=post_data.get("rank")
        ).first()
        if paper:
            response["status"] = False
            response["message"] = "排名重复！"
            return jsonify(response)

        # case3 只能有一位通讯作者
        if post_data.get("isCoAuthor"):
            paper = PublishedPapers.query.filter_by(
                paperNo=post_data.get("paperNo"), isCoAuthor=True
            ).first()
            if paper:
                response["status"] = False
                response["message"] = "只能有一位通讯作者！"
                return jsonify(response)

        # case4 数据类型不符或约束不满足
        try:
            add_published_papers(
                teacherNo=post_data.get("teacherNo"),
                paperNo=paperNo,
                rank=post_data.get("rank"),
                isCoAuthor=post_data.get("isCoAuthor"),
            )
            response["message"] = "发表论文登记成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "发表论文登记失败！数据类型不符或者约束不满足！"
    elif request.method == "POST":  # 修改论文信息
        post_data = request.get_json()
        paper = Paper.query.filter_by(No=paperNo).first()
        if not paper:
            response["status"] = False
            response["message"] = "论文不存在！"
            return jsonify(response)
        try:
            paper.name = post_data.get("name")
            paper.source = post_data.get("source")
            paper.publishYear = post_data.get("publishYear")
            paper.type = post_data.get("type")
            paper.level = post_data.get("level")
            db.session.commit()
            response["message"] = "论文修改成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "论文修改失败！数据类型不符或者约束不满足！"
    elif request.method == "DELETE":  # 删除论文
        paper = Paper.query.filter_by(No=paperNo).first()
        if not paper:
            response["status"] = False
            response["message"] = "论文不存在！"
            return jsonify(response)
        try:
            db.session.delete(paper)
            db.session.commit()
            response["message"] = "论文删除成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "论文删除失败！"
    elif request.method == "GET":  # 获取论文发表信息
        authors = PublishedPapers.query.filter_by(paperNo=paperNo).all()
        response["authors"] = [author.json() for author in authors]
    return jsonify(response)


@paper_blueprint.route("/papers/<paperNo>/<teacherNo>", methods=["POST", "DELETE"])
def update_delete_author(paperNo, teacherNo):
    response = {"status": True}
    author = PublishedPapers.query.filter_by(
        paperNo=paperNo, teacherNo=teacherNo
    ).first()
    if not author:
        response["status"] = False
        response["message"] = "论文发表不存在！"
        return jsonify(response)

    if request.method == "POST":  # 修改论文发表
        post_data = request.get_json()

        # case1 排名重复
        paper = PublishedPapers.query.filter_by(
            paperNo=post_data.get("paperNo"), rank=post_data.get("rank")
        ).first()
        if paper.teacherNo != post_data.get("teacherNo"):
            response["status"] = False
            response["message"] = "排名重复！"
            return jsonify(response)

        # case2 只能有一位通讯作者
        if post_data.get("isCoAuthor"):
            paper = PublishedPapers.query.filter_by(
                paperNo=post_data.get("paperNo"), isCoAuthor=True
            ).first()
            if paper:
                response["status"] = False
                response["message"] = "只能有一位通讯作者！"
                return jsonify(response)

        try:
            author.rank = post_data.get("rank")
            author.isCoAuthor = post_data.get("isCoAuthor")
            db.session.commit()
            response["message"] = "论文发表修改成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "论文发表修改失败！数据类型不符或者约束不满足！"
            return jsonify(response)
    elif request.method == "DELETE":  # 删除论文发表
        try:
            db.session.delete(author)
            db.session.commit()
            response["message"] = "论文发表删除成功！"
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "论文发表删除失败！"
    return jsonify(response)
