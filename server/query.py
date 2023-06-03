from flask import Blueprint, jsonify, request
from utils import *
from db import *

query_blueprint = Blueprint("query", __name__)


def getCourse(teacherNo, startYear, endYear):
    results = (
        db.session.query(Course, TeachCourse)
        .join(Course, TeachCourse.courseNo == Course.No)
        .filter(TeachCourse.teacherNo == teacherNo)
        .filter(TeachCourse.year >= startYear)
        .filter(TeachCourse.year <= endYear)
        .all()
    )
    courses = []
    for result in results:
        courses.append(
            {
                "No": result.Course.No,
                "name": result.Course.name,
                "takeCreditHour": result.TeachCourse.takeCreditHour,
                "year": result.TeachCourse.year,
                "semester": result.TeachCourse.semester,
            }
        )
    return courses


def getPaper(teacherNo, startYear, endYear):
    results = (
        db.session.query(Paper, PublishedPapers)
        .join(Paper, PublishedPapers.paperNo == Paper.No)
        .filter(PublishedPapers.teacherNo == teacherNo)
        .filter(Paper.publishYear >= startYear)
        .filter(Paper.publishYear <= endYear)
        .all()
    )
    papers = []
    for result in results:
        papers.append(
            {
                "No": result.Paper.No,
                "name": result.Paper.name,
                "source": result.Paper.source,
                "year": result.Paper.publishYear,
                "type": result.Paper.type,
                "level": result.Paper.level,
                "rank": result.PublishedPapers.rank,
                "isCoAuthor": result.PublishedPapers.isCoAuthor,
            }
        )
    return papers


def getProject(teacherNo, startYear, endYear):
    results = (
        db.session.query(Project, TakeProject)
        .join(Project, TakeProject.projectNo == Project.No)
        .filter(TakeProject.teacherNo == teacherNo)
        .filter(Project.startYear <= endYear)
        .filter(Project.endYear >= startYear)
        .all()
    )
    projects = []
    for result in results:
        projects.append(
            {
                "No": result.Project.No,
                "name": result.Project.name,
                "source": result.Project.source,
                "type": result.Project.type,
                "startYear": result.Project.startYear,
                "endYear": result.Project.endYear,
                "funds": result.Project.funds,
                "takeFunds": result.TakeProject.takeFunds,
            }
        )
    return projects


@query_blueprint.route("/query/<teacherNo>/<startYear>/<endYear>", methods=["GET"])
def query(teacherNo, startYear, endYear):
    response = {"status": True}
    if request.method == "GET":
        teacher = Teacher.query.filter_by(No=teacherNo).first()
        if not teacher:
            response["status"] = False
            response["message"] = "查询失败：教师工号不存在！"
            return jsonify(response)
        response["teacher"] = teacher.json()
        print(response)

        try:
            response["courses"] = getCourse(teacherNo, startYear, endYear)
        except Exception as e:
            print(e)
            response["status"] = False
            response["message"] = "教学信息获取出错"
            return jsonify(response)
        print(response)

        try:
            response["papers"] = getPaper(teacherNo, startYear, endYear)
        except Exception as e:
            print(e)
            response["status"] = False
            response["message"] = "发表论文信息获取出错"
            return jsonify(response)
        print(response)

        try:
            response["projects"] = getProject(teacherNo, startYear, endYear)
        except Exception as e:
            print(e)
            response["status"] = False
            response["message"] = "承担项目信息获取出错"
            return jsonify(response)

        response["message"] = "查询成功！"
        print(response)
    return jsonify(response)
