from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random

# create the extension
db = SQLAlchemy()


class Teacher(db.Model):
    __tablename__ = "Teacher"
    No = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(256))
    gender = db.Column(db.Integer)
    title = db.Column(db.Integer)
    publishedPapers = db.relationship(
        "PublishedPapers", backref="teacher", cascade="all, delete"
    )
    teachCourse = db.relationship(
        "TeachCourse", backref="teacher", cascade="all, delete"
    )
    takeProject = db.relationship(
        "TakeProject", backref="teacher", cascade="all, delete"
    )

    __table_args__ = (
        db.CheckConstraint("gender in (1, 2)"),
        db.CheckConstraint("title >= 1 and title <= 11"),
    )

    def __repr__(self):  # 相当于toString
        return "No: %r name: %r gender %r title: %r " % (
            self.No,
            self.name,
            self.gender,
            self.title,
        )

    def json(self):
        return {
            "No": self.No,
            "name": self.name,
            "gender": self.gender,
            "title": self.title,
        }


class Paper(db.Model):
    __tablename__ = "Paper"
    No = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    source = db.Column(db.String(256))
    publishYear = db.Column(db.Integer)
    type = db.Column(db.Integer)
    level = db.Column(db.Integer)
    publishedPapers = db.relationship(
        "PublishedPapers", backref="paper", cascade="all, delete"
    )

    __table_args__ = (
        db.CheckConstraint("type >= 1 and type <= 4"),
        db.CheckConstraint("level >= 1 and level <= 6"),
    )

    def __repr__(self):
        return "No: %r name: %r source: %r publishYear: %r type: %r level: %r " % (
            self.No,
            self.name,
            self.source,
            self.publishYear,
            self.type,
            self.level,
        )

    def json(self):
        return {
            "No": self.No,
            "name": self.name,
            "source": self.source,
            "publishYear": self.publishYear,
            "type": self.type,
            "level": self.level,
        }


class Project(db.Model):
    __tablename__ = "Project"
    No = db.Column(db.String(256), primary_key=True)
    name = db.Column(db.String(256))
    source = db.Column(db.String(256))
    type = db.Column(db.Integer)
    funds = db.Column(db.Float)
    startYear = db.Column(db.Integer)
    endYear = db.Column(db.Integer)
    takeProject = db.relationship(
        "TakeProject", backref="project", cascade="all, delete"
    )

    __table_args__ = (
        db.CheckConstraint("type >= 1 and type <= 5"),
        db.CheckConstraint("startYear <= endYear"),
        db.CheckConstraint("funds > 0"),
    )

    def __repr__(self):
        return (
            "No: %r name: %r source: %r type: %r funds: %r startYear: %r endYear: %r "
            % (
                self.No,
                self.name,
                self.source,
                self.type,
                self.funds,
                self.startYear,
                self.endYear,
            )
        )

    def json(self):
        return {
            "No": self.No,
            "name": self.name,
            "source": self.source,
            "type": self.type,
            "funds": self.funds,
            "startYear": self.startYear,
            "endYear": self.endYear,
        }


class Course(db.Model):
    __tablename__ = "Course"
    No = db.Column(db.String(256), primary_key=True)
    name = db.Column(db.String(256))
    creditHour = db.Column(db.Integer)
    type = db.Column(db.Integer)
    teachCourse = db.relationship(
        "TeachCourse", backref="course", cascade="all, delete"
    )

    __table_args__ = (
        db.CheckConstraint("type in (1, 2)"),
        db.CheckConstraint("creditHour > 0"),
    )

    def __repr__(self):
        return "No: %r name: %r creditHour: %r type: %r" % (
            self.No,
            self.name,
            self.creditHour,
            self.type,
        )

    def json(self):
        return {
            "No": self.No,
            "name": self.name,
            "creditHour": self.creditHour,
            "type": self.type,
        }


class PublishedPapers(db.Model):
    __tablename__ = "PublishedPapers"
    teacherNo = db.Column(db.String(5), db.ForeignKey("Teacher.No"), primary_key=True)
    paperNo = db.Column(db.Integer, db.ForeignKey("Paper.No"), primary_key=True)
    rank = db.Column(db.Integer)
    isCoAuthor = db.Column(db.Boolean)

    __table_args__ = (
        db.CheckConstraint("`rank` >= 1"),
        db.UniqueConstraint("paperNo", "rank", name="uq_paper_ranking"),
    )

    def __repr__(self):
        return "teacherNo: %r paperNo: %r rank: %r isCorrespondingAuthor: %r " % (
            self.teacherNo,
            self.paperNo,
            self.rank,
            self.isCoAuthor,
        )

    def json(self):
        return {
            "paperNo": self.paperNo,
            "teacherNo": self.teacherNo,
            "rank": self.rank,
            "isCoAuthor": self.isCoAuthor,
        }


class TakeProject(db.Model):
    __tablename__ = "TakeProject"
    teacherNo = db.Column(db.String(5), db.ForeignKey("Teacher.No"), primary_key=True)
    projectNo = db.Column(db.String(256), db.ForeignKey("Project.No"), primary_key=True)
    rank = db.Column(db.Integer)
    takeFunds = db.Column(db.Float)

    __table_args__ = (
        db.CheckConstraint("`rank` >= 1"),
        db.CheckConstraint("takeFunds > 0"),
        db.UniqueConstraint("projectNo", "rank", name="uq_project_ranking"),
    )

    def __repr__(self):
        return "teacherWorkNo: %r projectNo: %r rank: %r takeFunds: %r" % (
            self.teacherNo,
            self.projectNo,
            self.rank,
            self.takeFunds,
        )

    def json(self):
        return {
            "projectNo": self.projectNo,
            "teacherNo": self.teacherNo,
            "rank": self.rank,
            "takeFunds": self.takeFunds,
        }


class TeachCourse(db.Model):
    __tablename__ = "TeachCourse"
    teacherNo = db.Column(db.String(5), db.ForeignKey("Teacher.No"), primary_key=True)
    courseNo = db.Column(db.String(256), db.ForeignKey("Course.No"), primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.Integer, primary_key=True)
    takeCreditHour = db.Column(db.Integer)

    __table_args__ = (
        db.CheckConstraint("semester >= 1 and semester <= 3"),
        db.CheckConstraint("takeCreditHour > 0"),
    )

    def __repr__(self):
        return "teacherWorkNo: %r courseNo: %r year: %r semester: %r takeCreditHour" % (
            self.teacherNo,
            self.courseNo,
            self.year,
            self.semester,
            self.takeCreditHour,
        )

    def json(self):
        return {
            "courseNo": self.courseNo,
            "teacherNo": self.teacherNo,
            "year": self.year,
            "semester": self.semester,
            "takeCreditHour": self.takeCreditHour,
        }


class User(db.Model):
    __tablename__ = "User"
    username = db.Column(db.String(256), db.ForeignKey("Teacher.No"), primary_key=True)
    password = db.Column(db.String(256))

    def __repr__(self):
        return "username: %r password: %r" % (self.username, self.password)


def add_user(username, password):
    db.session.add(User(username=username, password=password))
    db.session.commit()


def add_teacher(No, name, gender, title):
    db.session.add(Teacher(No=No, name=name, gender=gender, title=title))
    db.session.commit()


def add_paper(No, name, source, publishYear, type, level):
    db.session.add(
        Paper(
            No=No,
            name=name,
            source=source,
            publishYear=publishYear,
            type=type,
            level=level,
        )
    )
    db.session.commit()


def add_project(No, name, source, type, funds, startYear, endYear):
    db.session.add(
        Project(
            No=No,
            name=name,
            source=source,
            type=type,
            funds=funds,
            startYear=startYear,
            endYear=endYear,
        )
    )
    db.session.commit()


def add_course(No, name, creditHour, type):
    db.session.add(Course(No=No, name=name, creditHour=creditHour, type=type))
    db.session.commit()


def add_published_papers(teacherNo, paperNo, rank, isCoAuthor):
    db.session.add(
        PublishedPapers(
            teacherNo=teacherNo, paperNo=paperNo, rank=rank, isCoAuthor=isCoAuthor
        )
    )
    db.session.commit()


def add_take_project(teacherNo, projectNo, rank, takeFunds):
    db.session.add(
        TakeProject(
            teacherNo=teacherNo, projectNo=projectNo, rank=rank, takeFunds=takeFunds
        )
    )
    db.session.commit()


def add_teach_course(teacherNo, courseNo, year, semester, takeCreditHour):
    db.session.add(
        TeachCourse(
            teacherNo=teacherNo,
            courseNo=courseNo,
            year=year,
            semester=semester,
            takeCreditHour=takeCreditHour,
        )
    )
    db.session.commit()


def init_data():
    # Assume that the teacher and course information is already in the database
    # now insert some record

    # add teacher
    add_teacher("jpq01", "Peiquan Jin", 1, 6)
    add_teacher("zxm01", "Xinming Zhang", 1, 6)
    add_teacher("zy01", "Yu Zhang", 2, 6)
    add_teacher("lxy01", "Xiangyang Li", 1, 6)
    add_teacher("jjm01", "Jianmin JI", 1, 6)

    genders = [1, 2]
    titles = range(1, 12)
    teachers_list = [
        "Emily Lee",
        "Matthew Brown",
        "Sarah Williams",
        "Christopher Davis",
        "Katherine Johnson",
        "Michael Taylor",
        "Jessica Clark",
        "Daniel Anderson",
        "Samantha Nelson",
        "Benjamin Wilson",
        "Elizabeth Turner",
        "Jonathan Martin",
        "Rachel Garcia",
        "William Jackson",
        "Lauren Scott",
        "David Perez",
        "Jennifer Garcia",
        "Robert Wright",
        "Victoria Thomas",
        "Adam Roberts",
    ]
    teacher_list = [
        ("t{:02d}".format(i), name, random.choice(genders), random.choice(titles))
        for i, name in enumerate(teachers_list[:20], 1)
    ]
    for teacher in teacher_list:
        add_teacher(*teacher)

    add_paper(1, "ZB+tree:一种ZNS SSD感知的新型索引结构", "计算机研究与发展", 2023, 1, 4)
    add_published_papers("jpq01", 1, 2, True)
    add_paper(
        2, "ZoneKV: A Space-Efficient Key-Value Store for ZNS SSDs", "DAC", 2023, 1, 1
    )
    add_published_papers("jpq01", 2, 2, True)

    journals = [
        "Journal CS",
        "IEEE",
        "ACM",
        "VLDB",
        "SIGMOD",
    ]  # 常见的计算机科学期刊

    # 生成20篇论文，并将它们插入到Paper表中
    paper_list = []
    for i in range(1, 21):
        title = "Paper {}".format(i)
        source = random.choice(journals)
        year = random.randint(2018, 2023)
        _type = random.randint(1, 4)
        level = random.randint(1, 6)
        paper_list.append((i + 5, title, source, year, _type, level))

    for paper in paper_list:
        add_paper(*paper)

    for i in range(1, 20):
        paper_id = i + 5
        ranks = [1, 2, 3]
        authors = random.sample(teacher_list, 3)
        for author in authors:
            teacherNo, _, _, _ = author
            rank = random.choice(ranks)
            ranks.remove(rank)
            is_corresponding = True if rank == 1 else False
            add_published_papers(teacherNo, paper_id, rank, is_corresponding)

    add_project("db1", "面向异构混合内存的NVM感知索引及自适应学习方法研究", "国家自然科学基金委", 1, 580000, 2021, 2024)
    add_take_project("jpq01", "db1", 1, 300000)
    add_take_project("zxm01", "db1", 2, 280000)
    add_project("db2", "量子安全数据库系统关键技术研发及产业化", "安徽省科技厅", 2, 2000000, 2022, 2025)
    add_take_project("jpq01", "db2", 1, 1000000)
    add_take_project("jjm01", "db2", 2, 1000000)

    funding_sources = ["国家自然科学基金委", "教育部", "科技部", "安徽省科技厅", "合肥市科技局"]
    project_list = []
    fundings = []
    for i in range(1, 21):
        no = "p{:02d}".format(i)
        name = "Project {}".format(i)
        source = random.choice(funding_sources)
        type_ = random.randint(1, 5)
        funding = random.randint(100000, 1000000)
        fundings.append(funding)
        start_year = random.randint(2018, 2021)
        end_year = start_year + random.randint(2, 5)
        project_list.append((no, name, source, type_, funding, start_year, end_year))

    for project in project_list:
        add_project(*project)

    for i in range(1, 21):
        project_no = "p{:02d}".format(i)
        fund = fundings[i - 1]
        ranks = [1, 2, 3]
        teachers = random.sample(teacher_list, 3)
        for k, teacher in enumerate(teachers):
            teacher_no, _, _, _ = teacher
            rank = random.choice(ranks)
            ranks.remove(rank)
            take_funding = random.randint(fund // 10, fund) if k < 2 else fund
            fund -= take_funding
            add_take_project(teacher_no, project_no, rank, take_funding)

    add_course("CSCOMP001", "数据库系统及应用", 100, 1)
    add_teach_course("jpq01", "CSCOMP001", 2023, 1, 50)
    add_teach_course("jjm01", "CSCOMP001", 2023, 1, 50)
    add_course("CSCOMP011", "高级数据库系统", 100, 1)
    add_teach_course("jpq01", "CSCOMP011", 2022, 1, 70)
    add_teach_course("lxy01", "CSCOMP011", 2022, 1, 30)

    course_list = [
        ("CSCOMP101", "计算机组成原理", 100, 1),
        ("CSCOMP102", "计算机网络", 100, 1),
        ("CSCOMP103", "操作系统", 100, 1),
        ("CSCOMP104", "编译原理", 100, 1),
        ("CSCOMP105", "算法设计与分析", 100, 1),
        ("CSCOMP106", "数据库", 100, 2),
        ("CSCOMP107", "计算机图形学", 100, 2),
        ("CSCOMP108", "机器学习", 100, 2),
        ("CSCOMP109", "人工智能基础", 100, 2),
        ("CSCOMP110", "软件工程", 100, 2),
        ("CSENG001", "大学物理", 100, 1),
        ("CSENG002", "大学英语", 100, 1),
        ("CSENG003", "高等数学", 100, 1),
        ("CSENG004", "线性代数", 100, 1),
        ("CSENG005", "概率论与数理统计", 100, 1),
        ("CSENG006", "离散数学", 100, 2),
        ("CSENG007", "数值计算方法", 100, 2),
        ("CSENG008", "微积分学", 100, 2),
        ("CSENG009", "复变函数与积分变换", 100, 2),
        ("CSENG010", "实变函数与泛函分析", 100, 2),
    ]

    for course in course_list:
        add_course(*course)

    for i in range(1, 21):
        course_no = course_list[i - 1][0]
        teachers = random.sample(teacher_list, 3)
        year = random.randint(2018, 2023)
        term = random.randint(1, 3)
        h = 100
        for k, teacher in enumerate(teachers):
            teacher_no = teacher[0]
            hours = random.randint(h // 10, h - 1) if k < 2 else h
            h -= hours
            add_teach_course(teacher_no, course_no, year, term, hours)
