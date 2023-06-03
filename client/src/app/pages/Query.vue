<template>
  <div class="container top scp">
    <div class="row">
      <div class="col-sm-12">
        <h1 class="text-center">教师教学科研科研工作统计</h1>
        <hr />
        <div
          class="alert"
          :class="{
              'alert-danger': message.includes('失败'),
              'alert-success': !message.includes('失败'),
            }"
          role="alert"
          v-if="showMessage"
        >
          {{ message }}
        </div>

        <div class="d-flex justify-content-center">
          <div class="mb-1 d-flex me-3">
            <input
              type="text"
              class="form-control"
              placeholder="请输入教师工号"
              v-model="teacherNo"
            />
          </div>
          <div class="mb-1 d-flex me-3">
            <input
              type="text"
              class="form-control"
              placeholder="请输入开始年份"
              v-model="startYear"
            />
          </div>
          <div class="mb-1 d-flex me-3">
            <input
              type="text"
              class="form-control"
              placeholder="请输入结束年份"
              v-model="endYear"
            />
          </div>
          <div class="d-flex">
            <button type="button" class="btn btn-warning" @click="query">
              查询
            </button>
          </div>
        </div>
        <br/>

        <h2 class="text-center">教师基本信息</h2>
        <table class="table table-hover text-center table-striped">
          <thead>
            <tr class="fs-7">
              <th scope="col">工号</th>
              <th scope="col">姓名</th>
              <th scope="col">性别</th>
              <th scope="col">职称</th>
            </tr>
          </thead>
          <tbody v-if="teacher.No">
            <tr class="text-center align-middle fs-6">
              <td>{{ teacher.No }}</td>
              <td>{{ teacher.name }}</td>
              <td>{{ teacher.gender }}</td>
              <td>{{ teacher.title }}</td>
            </tr>
          </tbody>
        </table>
        <br/>

        <h2 class="text-center">教学情况</h2>
        <table class="table table-hover text-center table-striped">
          <thead>
            <tr class="fs-7">
              <th scope="col">课程号</th>
              <th scope="col">课程名</th>
              <th scope="col">主讲学时</th>
              <th scope="col">年份</th>
              <th scope="col">学期</th>
            </tr>
          </thead>
          <tbody>
            <tr
              class="text-center align-middle fs-6"
              v-for="course in displayedCourses"
              :key="course.No"
            >
              <td>{{ course.No }}</td>
              <td>{{ course.name }}</td>
              <td>{{ course.takeCreditHour }}</td>
              <td>{{ course.year }}</td>
              <td>{{ course.semester }}</td>
            </tr>
          </tbody>
        </table>
        <nav>
          <ul class="pagination justify-content-center">
            <li
              class="page-item"
              :class="{ disabled: currentCoursePage === 1 }"
            >
              <a
                class="page-link"
                href="#"
                @click="goToCoursePage(currentCoursePage - 1)"
                >Previous</a
              >
            </li>
            <li
              class="page-item"
              v-for="page in coursePages"
              :key="page"
              :class="{ active: page === currentCoursePage }"
            >
              <a class="page-link" href="#" @click="goToCoursePage(page)">{{
                page
              }}</a>
            </li>
            <li
              class="page-item"
              :class="{ disabled: currentCoursePage === totalCoursePages }"
            >
              <a
                class="page-link"
                href="#"
                @click="goToCoursePage(currentCoursePage + 1)"
                >Next</a
              >
            </li>
          </ul>
        </nav>
        <br/>

        <h2 class="text-center">发表论文情况</h2>
        <table class="table table-hover text-center table-striped">
          <thead>
            <tr class="fs-7">
              <th scope="col">论文名</th>
              <th scope="col">发表源</th>
              <th scope="col">发表年份</th>
              <th scope="col">类型</th>
              <th scope="col">级别</th>
              <th scope="col">排名</th>
              <th scope="col">是否通讯作者</th>
            </tr>
          </thead>
          <tbody>
            <tr
              class="text-center align-middle fs-6"
              v-for="paper in displayedPapers"
              :key="paper.No"
            >
              <td>{{ paper.name }}</td>
              <td>{{ paper.source }}</td>
              <td>{{ paper.year }}</td>
              <td>{{ paper.type }}</td>
              <td>{{ paper.level }}</td>
              <td>{{ paper.rank }}</td>
              <td>{{ paper.isCoAuthor }}</td>
            </tr>
          </tbody>
        </table>
        <nav>
          <ul class="pagination justify-content-center">
            <li
              class="page-item"
              :class="{ disabled: currentCoursePage === 1 }"
            >
              <a
                class="page-link"
                href="#"
                @click="goToCoursePage(currentCoursePage - 1)"
                >Previous</a
              >
            </li>
            <li
              class="page-item"
              v-for="page in coursePages"
              :key="page"
              :class="{ active: page === currentCoursePage }"
            >
              <a class="page-link" href="#" @click="goToCoursePage(page)">{{
                page
              }}</a>
            </li>
            <li
              class="page-item"
              :class="{ disabled: currentCoursePage === totalCoursePages }"
            >
              <a
                class="page-link"
                href="#"
                @click="goToCoursePage(currentCoursePage + 1)"
                >Next</a
              >
            </li>
          </ul>
        </nav>
        <br/>

        <h2 class="text-center">承担项目情况</h2>
        <table class="table table-hover text-center table-striped">
          <thead>
            <tr class="fs-7">
              <th scope="col">项目名称</th>
              <th scope="col">项目来源</th>
              <th scope="col">项目类型</th>
              <th scope="col">开始年份</th>
              <th scope="col">结束年份</th>
              <th scope="col">项目总经费</th>
              <th scope="col">承担经费</th>
            </tr>
          </thead>
          <tbody>
            <tr
              class="text-center align-middle fs-6"
              v-for="project in displayedProjects"
              :key="project.No"
            >
              <td>{{ project.name }}</td>
              <td>{{ project.source }}</td>
              <td>{{ project.type }}</td>
              <td>{{ project.startYear }}</td>
              <td>{{ project.endYear }}</td>
              <td>{{ project.funds }}</td>
              <td>{{ project.takeFunds }}</td>
            </tr>
          </tbody>
        </table>
        <nav>
          <ul class="pagination justify-content-center">
            <li
              class="page-item"
              :class="{ disabled: currentProjectPage === 1 }"
            >
              <a
                class="page-link"
                href="#"
                @click="goToCoursePage(currentProjectPage - 1)"
                >Previous</a
              >
            </li>
            <li
              class="page-item"
              v-for="page in pages"
              :key="page"
              :class="{ active: page === currentProjectPage }"
            >
              <a class="page-link" href="#" @click="goToProjectPage(page)">{{
                page
              }}</a>
            </li>
            <li
              class="page-item"
              :class="{ disabled: currentProjectPage === totalProjectPages }"
            >
              <a
                class="page-link"
                href="#"
                @click="goToProjectPage(currentProjectPage + 1)"
                >Next</a
              >
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import _ from 'lodash'

export default {
  data () {
    return {
      teacher: {
        No: '',
        name: '',
        gender: 0,
        title: 0,
      },
      courses: [],
      papers: [],
      projects: [],
      message: '',
      showMessage: false,
      currentCoursePage: 1,
      currentPaperPage: 1,
      currentProjectPage: 1,
      pageSize: 5,
      teacherNo: '',
      startYear: '',
      endYear: '',
    }
  },

  computed: {
    totalCoursePages () {
      return Math.ceil(this.courses.length / this.pageSize)
    },

    displayedCourses () {
      const startIndex = (this.currentCoursePage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      return this.courses.slice(startIndex, endIndex)
    },

    coursePages () {
      const pagesArray = []
      for (let i = 1; i <= this.totalCoursePages; ++i) {
        pagesArray.push(i)
      }
      return pagesArray
    },

    totalPaperPages () {
      return Math.ceil(this.papers.length / this.pageSize)
    },

    displayedPapers () {
      const startIndex = (this.currentPaperPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      return this.papers.slice(startIndex, endIndex)
    },

    paperPages () {
      const pagesArray = []
      for (let i = 1; i <= this.totalPaperPages; ++i) {
        pagesArray.push(i)
      }
      return pagesArray
    },

    totalProjectPages () {
      return Math.ceil(this.projects.length / this.pageSize)
    },

    displayedProjects () {
      const startIndex = (this.currentProjectPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      return this.projects.slice(startIndex, endIndex)
    },

    projectPages () {
      const pagesArray = []
      for (let i = 1; i <= this.totalProjectPages; ++i) {
        pagesArray.push(i)
      }
      return pagesArray
    },
  },

  methods: {
    goToCoursePage (page) {
      if (page >= 1 && page <= this.totalCoursePages) {
        this.currentCoursePage = page
      }
    },

    goToPaperPage (page) {
      if (page >= 1 && page <= this.totalPaperPages) {
        this.currentPaperPage = page
      }
    },

    goToProjectPage (page) {
      if (page >= 1 && page <= this.totalProjectPages) {
        this.currentProjectPage = page
      }
    },

    query () {
      const path = `http://localhost:5000/query/${this.teacherNo}/${this.startYear}/${this.endYear}`
      axios
        .get(path)
        .then((res) => {
          this.showMessage = true
          this.message = res.data.message
          if (res.data.status) {
            this.teacher = res.data.teacher
            this.courses = res.data.courses
            this.papers = res.data.papers
            this.projects = res.data.projects
          }
        })
        .catch((err) => {
          this.showMessage = true
          this.message = err.response.data.message
        })
    },
  },
}
</script>

<style scoped>
.top {
  margin-top: 20px;
}
</style>
