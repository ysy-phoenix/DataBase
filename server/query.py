from flask import Blueprint, jsonify, request, Response, send_file, make_response
import pdfkit
import base64

import json
from reportlab.pdfgen import canvas
from utils import *
from db import *

query_blueprint = Blueprint("query", __name__)

genderMap = {1: "男", 2: "女"}

titleMap = {
    1: "博士后",
    2: "助教",
    3: "讲师",
    4: "副教授",
    5: "特任教授",
    6: "教授",
    7: "助理研究员",
    8: "特任副研究员",
    9: "副研究员",
    10: "特任研究员",
    11: "研究员",
}

paperTypeMap = {1: "full paper", 2: "short paper", 3: "poster paper", 4: "demo paper"}

paperLevelMap = {
    1: "CCF-A",
    2: "CCF-B",
    3: "CCF-C",
    4: "中文 CCF-A",
    5: "中文 CCF-B",
    6: "无级别",
}

projectMap = {1: "国家级项目", 2: "省部级项目", 3: "市厅级项目", 4: "企业合作项目", 5: "其它类型项目"}

coAuthorMap = {False: "否", True: "是"}

semesterMap = {1: "春", 2: "夏", 3: "秋"}


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
def query(teacherNo, startYear, endYear, local=False):
    response = {"status": True}
    teacher = Teacher.query.filter_by(No=teacherNo).first()
    if not teacher:
        response["status"] = False
        response["message"] = "查询失败：教师工号不存在！"
        return jsonify(response)
    response["teacher"] = teacher.json()

    try:
        response["courses"] = getCourse(teacherNo, startYear, endYear)
    except Exception as e:
        print(e)
        response["status"] = False
        response["message"] = "教学信息获取出错"
        return jsonify(response)

    try:
        response["papers"] = getPaper(teacherNo, startYear, endYear)
    except Exception as e:
        print(e)
        response["status"] = False
        response["message"] = "发表论文信息获取出错"
        return jsonify(response)

    try:
        response["projects"] = getProject(teacherNo, startYear, endYear)
    except Exception as e:
        print(e)
        response["status"] = False
        response["message"] = "承担项目信息获取出错"
        return jsonify(response)

    response["message"] = "查询成功！"
    if local:
        return (
            response["teacher"],
            response["courses"],
            response["papers"],
            response["projects"],
        )
    return jsonify(response)


def generatePDF(teacherNo, startYear, endYear):
    teacher, courses, papers, projects = query(
        teacherNo, startYear, endYear, local=True
    )
    html = """
    <html>
    <head>
    <style>
    h1 {
        text-align: center;
    }
    h2 {
        border-bottom: 1px solid black;
        padding-bottom: 0.25em;
        margin-bottom: 1.0em;
    }
    table {
        border-collapse: collapse;
        margin: 0 auto;
    }
    th, td {
        border: 1px solid black;
        padding: 0.5em;
        text-align: center;
    }
    th {
        background-color: #eee;
    }
    </style>
    </head>
    <body>
    <h1>教师教学科研工作统计（"""

    html += str(startYear) + "-" + str(endYear)

    html += """）</h1>

    <h2>教师基本信息</h2>
    <p style="font-size: 24px;">"""

    k = 6
    html += "工号：" + teacher["No"] + "&nbsp;" * k
    html += "姓名：" + teacher["name"] + "&nbsp;" * k
    html += "性别：" + genderMap[teacher["gender"]] + "&nbsp;" * k
    html += "职称：" + titleMap[teacher["title"]] + "</p>"

    html += """

    <h2>教学情况</h2>
    <table>
        <tr>
            <th>课程号</th>
            <th>课程名</th>
            <th>主讲学时</th>
            <th>学期</th>
        </tr>
"""
    for row in courses:
        html += "<tr>"
        html += "<td>" + row["No"] + "</td>"
        html += "<td>" + row["name"] + "</td>"
        html += "<td>" + str(row["takeCreditHour"]) + "</td>"
        html += "<td>" + str(row["year"]) + semesterMap[row["semester"]] + "</td>"
        html += "</tr>"

    html += """
    </table>

    <h2>发表论文情况</h2>
    <table>
        <tr>
            <th style="white-space: nowrap">论文标题</th>
            <th style="white-space: nowrap">发表源</th>
            <th style="white-space: nowrap">发表年份</th>
            <th style="white-space: nowrap">类型</th>
            <th style="white-space: nowrap">级别</th>
            <th style="white-space: nowrap">排名</th>
            <th style="white-space: nowrap">通讯作者</th>
        </tr>
    """

    for row in papers:
        html += "<tr>"
        html += "<td>" + row["name"] + "</td>"
        html += '<td style="white-space: nowrap">' + row["source"] + "</td>"
        html += "<td>" + str(row["year"]) + "</td>"
        html += '<td style="white-space: nowrap">' + paperTypeMap[row["type"]] + "</td>"
        html += (
            '<td style="white-space: nowrap">' + paperLevelMap[row["level"]] + "</td>"
        )
        html += "<td>第" + str(row["rank"]) + "</td>"
        html += "<td>" + coAuthorMap[row["isCoAuthor"]] + "</td>"
        html += "</tr>"

    html += """
    </table>

    <h2>承担项目情况</h2>
    <table>
        <tr>
            <th style="white-space: nowrap">项目名称</th>
            <th style="white-space: nowrap">项目级别</th>
            <th style="white-space: nowrap">起止年份</th>
            <th style="white-space: nowrap">总经费</th>
            <th style="white-space: nowrap">承担经费</th>
        </tr>
    """

    for row in projects:
        html += "<tr>"
        html += "<td>" + row["name"] + "</td>"
        html += "<td>" + projectMap[row["type"]] + "</td>"
        html += "<td>" + str(row["startYear"]) + "-" + str(row["endYear"]) + "</td>"
        html += "<td>" + str(row["funds"]) + "</td>"
        html += "<td>" + str(row["takeFunds"]) + "</td>"
        html += "</tr>"

    html += """
    </table>

    </body>
    </html>
    """

    # 将 HTML 转换为 PDF 文件
    options = {
        "page-size": "A4",
        "encoding": "UTF-8",
    }
    pdfkit.from_string(html, "output.pdf", options=options)
    # time.sleep(1)


@query_blueprint.route("/export/pdf/<teacherNo>/<startYear>/<endYear>", methods=["GET"])
def export_pdf(teacherNo, startYear, endYear):
    generatePDF(teacherNo, startYear, endYear)
    # 读取PDF文件的二进制数据
    with open("output.pdf", "rb") as f:
        pdf_data = f.read()

    # 构造响应对象，并设置响应头和响应体
    response = make_response(pdf_data)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=output.pdf"

    return response
