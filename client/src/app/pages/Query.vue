<template>
  <div class="container top scp">
    <div class="row">
      <div class="col-sm-12">
        <h2 class="text-center text-primary">教师教学科研科研工作统计</h2>
        <br />
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
          <div class="form-outline mb-1 me-3" style="width: 15%">
            <input type="text" class="form-control" v-model="teacherNo" />
            <label
              class="form-label"
              style="white-space: nowrap; font-weight: bold"
              >教师工号:</label
            >
          </div>
          <div class="form-outline mb-1 me-3" style="width: 15%">
            <input type="text" class="form-control" v-model="startYear" />
            <label
              class="form-label"
              style="white-space: nowrap; font-weight: bold"
              >开始年份:</label
            >
          </div>
          <div class="form-outline mb-1 me-3" style="width: 15%">
            <input type="text" class="form-control" v-model="endYear" />
            <label
              class="form-label"
              style="white-space: nowrap; font-weight: bold"
              >结束年份:</label
            >
          </div>
          <div class="d-flex me-3">
            <button
              type="button"
              class="btn btn-warning"
              @click="query"
              style="white-space: nowrap; font-weight: bold"
            >
              查询
            </button>
          </div>
          <div class="d-flex">
            <button
              type="button"
              class="btn btn-danger"
              @click="export_pdf"
              style="white-space: nowrap; font-weight: bold"
            >
              导出 pdf
            </button>
          </div>
        </div>
        <br />

        <h3 class="text-info">教师基本信息</h3>
        <table class="table table-hover text-center table-striped">
          <thead>
            <tr class="fs-6">
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                工号
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                姓名
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                性别
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                职称
              </th>
            </tr>
          </thead>
          <tbody v-if="teacher.No">
            <tr class="text-center align-middle fs-6">
              <td>{{ teacher.No }}</td>
              <td>{{ teacher.name }}</td>
              <td>{{ getGender(teacher.gender) }}</td>
              <td>{{ getTitle(teacher.title) }}</td>
            </tr>
          </tbody>
        </table>
        <br />

        <h3 class="text-info">教学情况</h3>
        <table class="table table-hover text-center table-striped">
          <thead>
            <tr class="fs-6">
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                课程号
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                课程名
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                主讲学时
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                年份
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                学期
              </th>
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
              <td>{{ getSemester(course.semester) }}</td>
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
        <br />

        <h3 class="text-info">发表论文情况</h3>
        <table class="table table-hover text-center table-striped">
          <thead>
            <tr class="fs-6">
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                论文名
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发表源&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                发表年份
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                类型
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                &nbsp;&nbsp;&nbsp;级别&nbsp;&nbsp;&nbsp;
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                排名
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                是否通讯作者
              </th>
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
              <td>{{ getPaperType(paper.type) }}</td>
              <td>{{ getPaperLevel(paper.level) }}</td>
              <td>{{ paper.rank }}</td>
              <td>{{ paper.isCoAuthor ? '是' : '否' }}</td>
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
              v-for="page in paperPages"
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
        <br />

        <h3 class="text-info">承担项目情况</h3>
        <table class="table table-hover text-center table-striped">
          <thead>
            <tr class="fs-6">
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                项目名称
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                项目来源
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                项目类型
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                开始年份
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                结束年份
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                项目总经费
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                承担经费
              </th>
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
              <td>{{ getProjectType(project.type) }}</td>
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
              v-for="page in projectPages"
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
import {
  getTitle,
  getGender,
  getPaperLevel,
  getPaperType,
  getSemester,
  getProjectType,
} from '../utils/helpFunc.vue'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

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
      if (this.teacherNo && this.startYear && this.endYear) {
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
      } else {
        this.message = '查询失败：请填写完整的查询信息！'
        this.showMessage = true
      }
    },

    export_pdf () {
      this.query()
      if (this.teacherNo && this.startYear && this.endYear) {
        const path = `http://localhost:5000/export/pdf/${this.teacherNo}/${this.startYear}/${this.endYear}`
        axios
          .get(path, { responseType: 'blob' })
          .then((res) => {
            this.showMessage = true
            this.message = '导出成功！'
            const url = window.URL.createObjectURL(res.data);
            window.open(url, '_blank');
          })
          .catch((err) => {
            console.log('err: ', err)
            this.showMessage = true
            this.message = '导出失败：发生错误！'
          })
      } else {
        this.message = '导出失败：请填写完整的查询信息！'
        this.showMessage = true
      }
    },

    getTitle,
    getGender,
    getPaperLevel,
    getPaperType,
    getSemester,
    getProjectType,
  },

  mounted () {
    document.querySelectorAll('.form-outline').forEach((formOutline) => {
      new mdb.Input(formOutline).update()
    })
  },
}
</script>

<style scoped>
.top {
  margin-top: 20px;
  /* margin-left: 50px; */
  /* margin-right: 20px; */
}
</style>
