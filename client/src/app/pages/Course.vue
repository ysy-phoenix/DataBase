<template>
  <div class="container top scp">
    <div class="row">
      <div class="col-sm-12">
        <h2 class="text-center text-primary">主讲课程登记查询</h2>
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
          <div class="d-flex me-3">
            <button
              type="button"
              class="btn btn-success text-nowrap"
              @click="toggleAddCourseModal"
              style="white-space: nowrap; font-weight: bold"
            >
              课程登记
            </button>
          </div>
          <div class="form-outline mb-1 me-1" style="width: 15%">
            <input type="text" class="form-control" v-model="teacherNo" />
            <label
              class="form-label"
              style="white-space: nowrap; font-weight: bold"
              >教师工号:</label
            >
          </div>
          <div class="d-flex me-3">
            <button
              type="button"
              class="btn btn-info"
              @click="getCourses(false)"
              style="white-space: nowrap; font-weight: bold"
            >
              课程查询
            </button>
          </div>
        </div>
        <table class="table table-hover text-center table-striped">
          <thead>
            <tr class="fs-7">
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('No')"
              >
                课程号
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('name')"
              >
                课程名称
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('creditHour')"
              >
                学时数
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('type')"
              >
                课程性质
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                主讲教师
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                课程更新
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                课程删除
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
              <td>{{ course.creditHour }}</td>
              <td>{{ getCourseType(course.type) }}</td>
              <th scope="col">
                <div class="dropdown">
                  <button
                    class="btn btn-primary dropdown-toggle"
                    type="button"
                    data-mdb-toggle="dropdown"
                    aria-expanded="false"
                    @click="getTeachers(course.No)"
                    style="white-space: nowrap; font-weight: bold"
                  >
                    查看主讲教师
                  </button>
                  <ul
                    class="dropdown-menu"
                    aria-labelledby="dropdownMenuButton"
                  >
                    <li v-for="teacher in teachers" :key="teacher.teacherNo">
                      <button
                        type="button"
                        class="dropdown-item text-center"
                        @click="toggleEditTeachModal(teacher)"
                        style="white-space: nowrap"
                      >
                        {{
                          teacher.year +
                          ' ' +
                          getSemester(teacher.semester) +
                          ' ' +
                          teacher.teacherNo
                        }}
                      </button>
                    </li>
                  </ul>
                </div>
              </th>
              <td>
                <button
                  type="button"
                  class="btn btn-warning"
                  @click="toggleUpdateCourseModal(course)"
                  style="white-space: nowrap; font-weight: bold"
                >
                  更新
                </button>
              </td>
              <td>
                <button
                  type="button"
                  class="btn btn-danger"
                  data-mdb-toggle="modal"
                  data-mdb-target="#deleteCourseModal"
                  style="font-weight: bold; white-space: nowrap"
                  @click="deleteCourseNo = course.No"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <nav>
          <ul class="pagination justify-content-center">
            <li class="page-item">
              <a class="page-link">Rows per page:</a>
            </li>
            <li class="page-item" style="width: 5%">
              <input type="text" class="form-control" v-model="pageSize" />
            </li>
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <a class="page-link" href="#" @click="goToPage(currentPage - 1)"
                >Previous</a
              >
            </li>
            <li
              class="page-item"
              v-for="page in pages"
              :key="page"
              :class="{ active: page === currentPage }"
            >
              <a class="page-link" href="#" @click="goToPage(page)">{{
                page
              }}</a>
            </li>
            <li
              class="page-item"
              :class="{ disabled: currentPage === totalPages }"
            >
              <a class="page-link" href="#" @click="goToPage(currentPage + 1)"
                >Next</a
              >
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <!-- add new course modal -->
    <div
      ref="addCourseModal"
      class="modal modal-xl fade"
      :class="{ show: activeAddCourseModal, 'd-block': activeAddCourseModal }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">课程登记</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleAddCourseModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="alert alert-danger" v-if="showAlert" role="alert">
            {{ this.message }}
          </div>
          <div class="modal-body">
            <form @submit.prevent="addCourse">
              <div class="table-responsive">
                <table class="table table-bordered">
                  <tbody>
                    <tr>
                      <td style="width: 200px">
                        <label class="form-label" style="font-weight: bold"
                          >课程号:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="addCourseForm.courseNo"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >课程名称:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="addCourseForm.name"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >学时数:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="addCourseForm.creditHour"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >课程性质:</label
                        >
                        <select
                          class="form-select"
                          aria-label="Default select example"
                          v-model="addCourseForm.type"
                        >
                          <option value="1">1-本科生课程</option>
                          <option value="2">2-研究生课程</option>
                        </select>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div class="text-right">
                <button type="button" class="btn btn-info" @click="addTeacher">
                  添加主讲教师
                </button>
              </div>
              <hr />
              <div class="table-responsive">
                <table class="table table-bordered text-center">
                  <thead>
                    <tr>
                      <th>课程号</th>
                      <th>教师工号</th>
                      <th>年份</th>
                      <th>学期</th>
                      <th>承担学时</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(teacher, index) in addTeachers" :key="index">
                      <td>
                        <input
                          type="text"
                          class="form-control"
                          disabled="true"
                          v-model="addCourseForm.courseNo"
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          class="form-control"
                          v-model="teacher.teacherNo"
                          required
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          class="form-control"
                          v-model="teacher.year"
                          required
                        />
                      </td>
                      <td>
                        <select
                          class="form-select"
                          aria-label="Default select example"
                          v-model="teacher.semester"
                        >
                          <option value="1">1-春季学期</option>
                          <option value="2">2-夏季学期</option>
                          <option value="3">3-秋季学期</option>
                        </select>
                      </td>
                      <td>
                        <input
                          type="text"
                          class="form-control"
                          v-model="teacher.takeCreditHour"
                          required
                        />
                      </td>
                      <td>
                        <button
                          type="button"
                          class="btn btn-outline-danger"
                          @click="removeTeacher(index)"
                        >
                          <i class="far fa-trash-can"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="d-flex justify-content-evenly">
                <button type="submit" class="btn btn-primary">提交</button>
                <button type="button" class="btn btn-danger" @click="initForm">
                  重置
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- update course modal -->
    <div
      ref="updateCourseModal"
      class="modal modal-xl fade"
      :class="{
        show: activeUpdateCourseModal,
        'd-block': activeUpdateCourseModal,
      }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">课程信息更新</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleUpdateCourseModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="alert alert-danger" v-if="showAlert" role="alert">
            {{ this.message }}
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateCourse(updateCourseForm.No)">
              <div class="table-responsive">
                <table class="table table-bordered">
                  <tbody>
                    <tr>
                      <td style="width: 200px">
                        <label class="form-label" style="font-weight: bold"
                          >课程号:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          disabled="true"
                          v-model="updateCourseForm.No"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >课程名称:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="updateCourseForm.name"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >学时数:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="updateCourseForm.creditHour"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >课程性质:</label
                        >
                        <select
                          class="form-select"
                          aria-label="Default select example"
                          v-model="updateCourseForm.type"
                        >
                          <option value="1">1-本科生课程</option>
                          <option value="2">2-研究生课程</option>
                        </select>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div class="text-right">
                <button
                  type="button"
                  class="btn btn-info"
                  @click="addUpdateTeacher"
                >
                  添加主讲教师
                </button>
              </div>
              <hr />
              <div class="table-responsive">
                <table class="table table-bordered text-center">
                  <thead>
                    <tr>
                      <th>课程号</th>
                      <th>教师工号</th>
                      <th>年份</th>
                      <th style="width: 20%">学期</th>
                      <th>承担学时</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(teacher, index) in updateTeachers" :key="index">
                      <td>
                        <input
                          type="text"
                          class="form-control"
                          disabled="true"
                          v-model="updateCourseForm.No"
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          class="form-control"
                          v-model="teacher.teacherNo"
                          required
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          class="form-control"
                          v-model="teacher.year"
                          required
                        />
                      </td>
                      <td>
                        <select
                          class="form-select"
                          aria-label="Default select example"
                          v-model="teacher.semester"
                        >
                          <option value="1">1-春季学期</option>
                          <option value="2">2-夏季学期</option>
                          <option value="3">3-秋季学期</option>
                        </select>
                      </td>
                      <td>
                        <input
                          type="text"
                          class="form-control"
                          v-model="teacher.takeCreditHour"
                          required
                        />
                      </td>
                      <td>
                        <button
                          type="button"
                          class="btn btn-outline-danger"
                          @click="removeUpdateTeacher(index)"
                        >
                          <i class="far fa-trash-can"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="d-flex justify-content-evenly">
                <button type="submit" class="btn btn-primary">提交</button>
                <button
                  type="button"
                  class="btn btn-danger"
                  @click="resetUpdateCourseForm"
                >
                  重置
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Teacher modal -->
    <div
      class="modal modal-lg fade"
      :class="{
        show: activeEditTeachModal,
        'd-block': activeEditTeachModal,
      }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">主讲教师查看</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleEditTeachModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <table class="table table-bordered text-center">
              <thead>
                <tr>
                  <th>课程号</th>
                  <th>教师工号</th>
                  <th>年份</th>
                  <th style="width: 20%">学期</th>
                  <th>承担学时</th>
                </tr>
              </thead>
              <tbody>
                <tr class="text-center align-middle fs-6">
                  <td>{{ teach.courseNo }}</td>
                  <td>{{ teach.teacherNo }}</td>
                  <td>{{ teach.year }}</td>
                  <td>{{ getSemester(teach.semester) }}</td>
                  <td>{{ teach.takeCreditHour }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- delete Modal -->
    <div
      class="modal fade"
      tabindex="-1"
      id="deleteCourseModal"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">删除确认</h5>
            <button
              type="button"
              class="btn-close"
              data-mdb-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body text-danger text fs-1">确认删除此课程吗？</div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
            >
              Close
            </button>
            <button
              type="button"
              class="btn btn-danger"
              data-mdb-dismiss="modal"
              @click="handleDeleteCourse(deleteCourseNo)"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import _ from 'lodash'
import { getCourseType, getSemester } from '../utils/helpFunc.vue'

export default {
  data() {
    return {
      activeAddCourseModal: false,
      activeUpdateCourseModal: false,
      activeEditTeachModal: false,
      addCourseForm: {
        courseNo: '',
        name: '',
        creditHour: 0,
        type: 0,
      },
      updateCourseForm: {
        No: '',
        name: '',
        creditHour: 0,
        type: 0,
      },
      teach: {
        teacherNo: '',
        courseNo: '',
        year: 0,
        semester: 0,
        takeCreditHour: 0,
      },
      teachers: [],
      addTeachers: [],
      updateTeachers: [],
      courses: [],
      message: '',
      showMessage: false,
      showAlert: false,
      currentPage: 1,
      pageSize: 10,
      courseNo: '',
      teacherNo: '',
      deleteCourseNo: '',
      sortByField: 'No',
      sortDirection: 'asc',
    }
  },

  computed: {
    sortedCourse() {
      const field = this.sortByField
      const direction = this.sortDirection === 'asc' ? 1 : -1
      return this.courses.slice().sort((a, b) => {
        const aValue = a[field]
        const bValue = b[field]
        if (aValue < bValue) {
          return -1 * direction
        }
        if (aValue > bValue) {
          return 1 * direction
        }
        return 0
      })
    },

    totalPages() {
      return Math.ceil(this.courses.length / this.pageSize)
    },

    displayedCourses() {
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      return this.sortedCourse.slice(startIndex, endIndex)
    },

    pages() {
      const pagesArray = []
      for (let i = 1; i <= this.totalPages; ++i) {
        pagesArray.push(i)
      }
      return pagesArray
    },
  },

  methods: {
    sortBy(field) {
      if (field === this.sortByField) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortByField = field
        this.sortDirection = 'asc'
      }
    },

    addTeacher() {
      this.addTeachers.push({
        teacherNo: '',
        year: 0,
        semester: 0,
        takeCreditHour: 0,
      })
    },

    addUpdateTeacher() {
      this.updateTeachers.push({
        teacherNo: '',
        year: 0,
        semester: 0,
        takeCreditHour: 0,
      })
    },

    removeTeacher(index) {
      this.addTeachers.splice(index, 1)
    },

    removeUpdateTeacher(index) {
      this.updateTeachers.splice(index, 1)
    },

    goToPage(page) {
      // 跳转到指定页
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    },

    initForm() {
      // 初始化/重置表单
      this.addCourseForm.courseNo = ''
      this.addCourseForm.name = ''
      this.addCourseForm.creditHour = 0
      this.addCourseForm.type = 0
      this.addTeachers = []
    },

    manageMessage(status) {
      if (status) {
        this.showMessage = true
        return true
      } else {
        this.showAlert = true
        return false
      }
    },

    getCourses(flag = false) {
      if (this.teacherNo) {
        this.queryCourse(this.teacherNo, flag)
      } else {
        this.getAllCourses(flag)
      }
    },

    queryCourse(teacherNo, flag = false) {
      // 查询论文信息
      const path = `http://localhost:5000/courses/teacher/${teacherNo}`
      axios
        .get(path)
        .then((res) => {
          if (!flag) {
            this.message = res.data.message
          }
          this.showMessage = true
          if (res.data.status) {
            this.courses = res.data.courses
          }
        })
        .catch((error) => {
          console.error(error)
        })
    },

    getAllCourses(flag = false) {
      // 获取课程信息
      const path = 'http://localhost:5000/courses'
      axios
        .get(path)
        .then((res) => {
          this.courses = res.data.courses
          this.showMessage = flag
        })
        .catch((error) => {
          console.error(error)
        })
    },

    addCourse() {
      // 添加课程信息
      const path = 'http://localhost:5000/courses'
      const payload = {
        course: this.addCourseForm,
        teachers: this.addTeachers,
      }
      axios
        .put(path, payload)
        .then((res) => {
          this.getCourses(res.data.status)
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.initForm()
            this.toggleAddCourseModal()
          }
        })
        .catch((error) => {
          console.error(error)
          this.getCourses()
        })
    },

    toggleAddCourseModal() {
      this.initForm()
      this.activeAddCourseModal = !this.activeAddCourseModal
      if (this.activeAddCourseModal) {
        this.showAlert = false
      }
    },

    getTeachers(courseNo, isUpdate = false) {
      // 获取课程主讲信息
      const path = `http://localhost:5000/courses/${courseNo}`
      axios
        .get(path)
        .then((res) => {
          if (isUpdate) {
            this.updateTeachers = res.data.teachers
            this.updateTeachers.sort((a, b) => a.year - b.year)
          } else {
            this.teachers = res.data.teachers
            this.teachers.sort((a, b) => a.year - b.year)
          }
        })
        .catch((error) => {
          console.error(error)
        })
    },

    updateCourse(courseNo) {
      // 更新课程信息
      const path = `http://localhost:5000/courses/${courseNo}`
      const payload = {
        course: this.updateCourseForm,
        teachers: this.updateTeachers,
      }
      axios
        .post(path, payload)
        .then((res) => {
          this.getCourses(res.data.status)
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.toggleUpdateCourseModal(null)
          }
        })
        .catch((error) => {
          console.error(error)
          this.getCourses()
        })
    },

    resetUpdateCourseForm() {
      this.getTeachers(this.updateCourseForm.No, true)
      for (let i = 0; i < this.displayedCourses.length; ++i) {
        if (this.displayedCourses[i].No === this.updateCourseForm.No) {
          this.updateCourseForm = _.cloneDeep(this.displayedCourses[i])
          break
        }
      }
    },

    toggleUpdateCourseModal(course) {
      if (course) {
        this.getTeachers(course.No, true)
        this.updateCourseForm = _.cloneDeep(course)
      }
      this.activeUpdateCourseModal = !this.activeUpdateCourseModal
      if (this.activeUpdateCourseModal) {
        this.showAlert = false
      }
    },

    handleDeleteCourse(courseNo) {
      // 删除课程
      const path = `http://localhost:5000/courses/${courseNo}`
      axios
        .delete(path)
        .then((res) => {
          this.getCourses(true)
          this.message = res.data.message
          this.showMessage = true
        })
        .catch((error) => {
          console.error(error)
          this.getCourses()
        })
    },

    toggleEditTeachModal(teacher) {
      if (teacher) {
        this.teach = _.cloneDeep(teacher)
      }
      this.activeEditTeachModal = !this.activeEditTeachModal
      if (this.activeEditTeachModal) {
        this.showAlert = false
      }
    },

    getCourseType,
    getSemester,
  },

  created() {
    this.getCourses()
  },

  mounted() {
    document.querySelectorAll('.form-outline').forEach((formOutline) => {
      new mdb.Input(formOutline).update()
    })
  },
}
</script>

<style scoped>
.top {
  margin-top: 20px;
}
</style>
