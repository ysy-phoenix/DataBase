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
        post_paper = post_data.get("paper")
        authors = post_data.get("authors")

        # case1 主码重复
        paper = Paper.query.filter_by(No=post_paper.get("paperNo")).first()
        if paper:
            response["status"] = False
            response["message"] = "论文序号重复！"
            return jsonify(response)

        # case2 论文名引号检测
        if re.search("[\"']", post_paper.get("name")):
            response["status"] = False
            response["message"] = "论文名称不允许带引号！"
            return jsonify(response)

        # case3 作者检查
        if len(authors) == 0:
            response["status"] = False
            response["message"] = "必须提供作者信息！"
            return jsonify(response)
        teacherNo = set()
        ranks = set()
        isCoAuthor = False
        for author in authors:
            teacher = Teacher.query.filter_by(No=author["teacherNo"]).first()
            if not teacher:
                response["status"] = False
                response["message"] = "教师 " + author["teacherNo"] + " 不存在！"
                return jsonify(response)
            if author.get("teacherNo") in teacherNo:
                response["status"] = False
                response["message"] = "作者 " + author["teacherNo"] + " 重复！"
                return jsonify(response)
            if author.get("rank") in ranks:
                response["status"] = False
                response["message"] = "论文排名重复！"
                return jsonify(response)
            if isCoAuthor and author.get("isCoAuthor"):
                response["status"] = False
                response["message"] = "只能有一位通讯作者！"
                return jsonify(response)
            if author.get("isCoAuthor"):
                isCoAuthor = True
            teacherNo.add(author.get("teacherNo"))
            ranks.add(author.get("rank"))

        # case4 数据类型不符或者约束不满足
        try:
            add_paper(
                No=post_paper.get("paperNo"),
                name=post_paper.get("name"),
                source=post_paper.get("source"),
                publishYear=post_paper.get("publishYear"),
                type=post_paper.get("type"),
                level=post_paper.get("level"),
            )
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "论文添加失败！数据类型不符或者约束不满足！"
            return jsonify(response)

        for author in authors:
            try:
                add_published_papers(
                    teacherNo=author.get("teacherNo"),
                    paperNo=post_paper.get("paperNo"),
                    rank=author.get("rank"),
                    isCoAuthor=author.get("isCoAuthor"),
                )
            except Exception as e:
                print(e)
                db.session.rollback()
                response["status"] = False
                response["message"] = "论文作者登记失败！数据类型不符或者约束不满足！"
                return jsonify(response)
        db.session.commit()
        response["message"] = "发表论文登记成功！"

    elif request.method == "GET":
        papers = Paper.query.all()
        response["papers"] = [paper.json() for paper in papers]
    return jsonify(response)


@paper_blueprint.route("/papers/<paperNo>", methods=["POST", "GET", "DELETE"])
def edit_paper_author(paperNo):
    response = {"status": True}
    if request.method == "POST":  # 修改论文信息
        post_data = request.get_json()
        post_paper = post_data.get("paper")
        authors = post_data.get("authors")

        paper = Paper.query.filter_by(No=paperNo).first()

        if re.search("[\"']", post_paper.get("name")):
            response["status"] = False
            response["message"] = "论文名称不允许带引号！"
            return jsonify(response)

        if len(authors) == 0:
            response["status"] = False
            response["message"] = "必须提供作者信息！"
            return jsonify(response)

        old_authors = PublishedPapers.query.filter_by(paperNo=paperNo).all()
        delete_authors = set([author.teacherNo for author in old_authors])
        add_authors = set()

        # 作者检查
        teacherNo = set()
        ranks = set()
        isCoAuthor = False
        for author in authors:
            teacher = Teacher.query.filter_by(No=author["teacherNo"]).first()
            if not teacher:
                response["status"] = False
                response["message"] = "教师 " + author["teacherNo"] + " 不存在！"
                return jsonify(response)
            if author.get("teacherNo") in teacherNo:
                response["status"] = False
                response["message"] = "作者 " + author["teacherNo"] + " 重复！"
                return jsonify(response)
            if author.get("rank") in ranks:
                response["status"] = False
                response["message"] = "论文排名重复！"
                return jsonify(response)
            if isCoAuthor and author.get("isCoAuthor"):
                response["status"] = False
                response["message"] = "只能有一位通讯作者！"
                return jsonify(response)
            if author.get("isCoAuthor"):
                isCoAuthor = True
            teacherNo.add(author.get("teacherNo"))
            ranks.add(author.get("rank"))
            if author["teacherNo"] in delete_authors:
                delete_authors.remove(author["teacherNo"])
            else:
                add_authors.add(author["teacherNo"])

        try:
            paper.name = post_paper.get("name")
            paper.source = post_paper.get("source")
            paper.publishYear = post_paper.get("publishYear")
            paper.type = post_paper.get("type")
            paper.level = post_paper.get("level")
        except Exception as e:
            print(e)
            db.session.rollback()
            response["status"] = False
            response["message"] = "论文修改失败！数据类型不符或者约束不满足！"

        for author in delete_authors:
            author = PublishedPapers.query.filter_by(
                paperNo=paperNo, teacherNo=author
            ).first()
            db.session.delete(author)

        for author in authors:
            try:
                if author["teacherNo"] in add_authors:
                    add_published_papers(
                        teacherNo=author.get("teacherNo"),
                        paperNo=paperNo,
                        rank=author.get("rank"),
                        isCoAuthor=author.get("isCoAuthor"),
                    )
                else:
                    update_author = PublishedPapers.query.filter_by(
                        paperNo=paperNo, teacherNo=author["teacherNo"]
                    ).first()
                    update_author.rank = author.get("rank")
                    update_author.isCoAuthor = author.get("isCoAuthor")
            except Exception as e:
                print(e)
                db.session.rollback()
                response["status"] = False
                response["message"] = "论文作者修改失败！数据类型不符或者约束不满足！"
                return jsonify(response)
        response["message"] = "发表论文信息更新成功！"
        db.session.commit()

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


@paper_blueprint.route("/papers/teacher/<teacherNo>", methods=["GET"])
def query_papers(teacherNo):
    response = {"status": True}
    if request.method == "GET":
        teacher = Teacher.query.filter_by(No=teacherNo).first()
        if not teacher:
            response["status"] = False
            response["message"] = "查询失败：教师工号不存在！"
            return jsonify(response)
        results = (
            db.session.query(Paper, PublishedPapers)
            .join(Paper, PublishedPapers.paperNo == Paper.No)
            .filter(PublishedPapers.teacherNo == teacherNo)
            .all()
        )
        response["papers"] = [result.Paper.json() for result in results]
        response["message"] = "查询成功！"
    return jsonify(response)
