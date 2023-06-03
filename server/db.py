from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

    __table_args__ = (db.CheckConstraint("type >= 1 and type <= 5"),)

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

    __table_args__ = (db.CheckConstraint("type in (1, 2)"),)

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
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    takeCreditHour = db.Column(db.Integer)

    __table_args__ = (db.CheckConstraint("semester >= 1 and semester <= 3"),)

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
    add_teacher("jpq01", "Peiquan Jin", 1, 6)
    add_teacher("zxm01", "Xinming Zhang", 1, 6)
    add_teacher("zy01", "Yu Zhang", 2, 6)
    add_teacher("lxy01", "Xiangyang Li", 1, 6)
    add_teacher("jjm01", "Jianmin JI", 1, 6)

    add_paper(1, "DataBase1", "IEEE", 2020, 1, 1)
    add_published_papers("jpq01", 1, 1, True)
    add_paper(2, "DataBase2", "IEEE", 2021, 1, 1)
    add_published_papers("jpq01", 2, 1, True)

    add_project("dbproject1", "DataBase", "NSF", 1, 100, 2020, 2023)
    add_take_project("jpq01", "dbproject1", 1, 70)
    add_take_project("zxm01", "dbproject1", 2, 30)
    add_project("dbproject2", "DataBase", "NSF", 1, 200, 2020, 2023)
    add_take_project("jpq01", "dbproject2", 1, 180)
    add_take_project("jjm01", "dbproject2", 2, 20)

    add_course("db001", "DataBase", 100, 1)
    add_teach_course("jpq01", "db001", 2023, 1, 50)
    add_teach_course("jjm01", "db001", 2023, 1, 50)
    add_course("db002", "DataBase", 100, 1)
    add_teach_course("jpq01", "db002", 2022, 1, 70)
    add_teach_course("lxy01", "db002", 2022, 1, 30)
