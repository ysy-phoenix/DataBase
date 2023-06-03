<template>
  <div class="container top scp">
    <div class="row">
      <div class="col-sm-12">
        <h1 class="text-center">课程</h1>
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
          <div class="d-flex me-3">
            <button
              type="button"
              class="btn btn-success text-nowrap"
              @click="toggleAddCourseModal"
            >
              课程登记
            </button>
          </div>
          <div class="d-flex me-3">
            <button
              type="button"
              class="btn btn-primary text-nowrap"
              @click="toggleTeachCourseModal"
            >
              主讲课程登记
            </button>
          </div>
          <div class="mb-1 d-flex me-3">
            <input
              type="text"
              class="form-control"
              placeholder="请输入课程号"
              v-model="courseNo"
            />
          </div>
          <div class="d-flex">
            <button type="button" class="btn btn-warning" @click="fundCheck">
              学时检查
            </button>
          </div>
        </div>
        <table class="table table-hover text-center table-striped">
          <thead>
            <tr class="fs-7">
              <th scope="col">课程号</th>
              <th scope="col">课程名称</th>
              <th scope="col">学时数</th>
              <th scope="col">课程性质</th>
              <th scope="col">课程更新</th>
              <th scope="col">课程删除</th>
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
              <td>{{ course.type }}</td>
              <th scope="col">
                <div class="dropdown">
                  <button
                    class="btn btn-primary dropdown-toggle"
                    type="button"
                    id="dropdownMenuButton"
                    data-mdb-toggle="dropdown"
                    aria-expanded="false"
                    @click="getTeachers(course.No)"
                  >
                    查看主讲教师
                  </button>
                  <ul
                    class="dropdown-menu"
                    aria-labelledby="dropdownMenuButton"
                  >
                    <li v-for="teacher in teachers" :key="teacher.rank">
                      <button
                        type="button"
                        class="dropdown-item text-center"
                        @click="toggleEditTeachModal(teacher)"
                      >
                        {{ teacher.teacherNo }}
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
                >
                  Update
                </button>
              </td>
              <td>
                <button
                  type="button"
                  class="btn btn-danger"
                  @click="handleDeleteCourse(course.No)"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <nav>
          <ul class="pagination justify-content-center">
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
      class="modal fade"
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
            <form>
              <div class="mb-3">
                <label class="form-label">课程号</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="addCourseForm.courseNo"
                  placeholder="Enter CourseNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">课程名称</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="addCourseForm.name"
                  placeholder="Enter name"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">学时数</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="addCourseForm.creditHour"
                  placeholder="Enter source"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">课程类型</label>
                <select
                  class="form-select"
                  aria-label="Default select example"
                  v-model="addCourseForm.type"
                >
                  <option value="1">1-本科生课程</option>
                  <option value="2">2-研究生课程</option>
                </select>
              </div>

              <div class="d-flex justify-content-evenly">
                <button
                  type="button"
                  class="btn btn-primary"
                  @click="addCourse(addCourseForm)"
                >
                  提交
                </button>
                <button type="button" class="btn btn-danger" @click="initForm">
                  重置
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeAddCourseModal" class="modal-backdrop fade show"></div>

    <!-- add teacher course modal -->
    <div
      ref="addTeachCourseModal"
      class="modal fade"
      :class="{
          show: activeTeachCourseModal,
          'd-block': activeTeachCourseModal,
        }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">主讲课程登记</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleTeachCourseModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="alert alert-danger" v-if="showAlert" role="alert">
            {{ this.message }}
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label class="form-label">教师工号</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="teachCourseForm.teacherNo"
                  placeholder="Enter TeacherNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">课程号</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="teachCourseForm.courseNo"
                  placeholder="Enter CourseNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">年份</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="teachCourseForm.year"
                  placeholder="Enter rank"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">学期</label>
                <select
                  class="form-select"
                  aria-label="Default select example"
                  v-model="teachCourseForm.semester"
                >
                  <option value="1">1-春季学期</option>
                  <option value="2">2-夏季学期</option>
                  <option value="3">3-秋季学期</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">承担学时</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="teachCourseForm.takeCreditHour"
                  placeholder="Enter rank"
                />
              </div>

              <div class="d-flex justify-content-evenly">
                <button
                  type="button"
                  class="btn btn-primary"
                  @click="teachCourse(teachCourseForm, teachCourseForm.courseNo)
                    "
                >
                  提交
                </button>
                <button type="button" class="btn btn-danger" @click="initForm">
                  重置
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeTeachCourseModal" class="modal-backdrop fade show"></div>

    <!-- update course modal -->
    <div
      ref="updateCourseModal"
      class="modal fade"
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
            <form>
              <div class="mb-3">
                <label class="form-label">课程号</label>
                <input
                  type="text"
                  class="form-control"
                  disabled="true"
                  v-model="updateCourseForm.No"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">课程名称</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updateCourseForm.name"
                  placeholder="Enter name"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">学时数</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updateCourseForm.creditHour"
                  placeholder="Enter source"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">课程类型</label>
                <select
                  class="form-select"
                  aria-label="Default select example"
                  v-model="updateCourseForm.type"
                >
                  <option value="1">1-本科生课程</option>
                  <option value="2">2-研究生课程</option>
                </select>
              </div>

              <div class="d-flex justify-content-evenly">
                <button
                  type="button"
                  class="btn btn-primary"
                  @click="updateCourse(updateCourseForm, updateCourseForm.No)"
                >
                  提交
                </button>
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
    <div v-if="activeUpdateCourseModal" class="modal-backdrop fade show"></div>

    <!-- add Edit course modal -->
    <div
      ref="addEditCourseModal"
      class="modal fade"
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
            <h5 class="modal-title">主讲课程修改/删除</h5>
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
          <div class="alert alert-danger" v-if="showAlert" role="alert">
            {{ this.message }}
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label class="form-label">教师工号</label>
                <input
                  type="text"
                  class="form-control"
                  disabled="true"
                  v-model="updateTeachForm.teacherNo"
                  placeholder="Enter TeacherNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">课程号</label>
                <input
                  type="text"
                  disabled="true"
                  class="form-control"
                  v-model="updateTeachForm.courseNo"
                  placeholder="Enter CourseNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">年份</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updateTeachForm.year"
                  placeholder="Enter rank"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">学期</label>
                <select
                  class="form-select"
                  aria-label="Default select example"
                  v-model="updateTeachForm.semester"
                >
                  <option value="1">1-春季学期</option>
                  <option value="2">2-夏季学期</option>
                  <option value="3">3-秋季学期</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">承担学时</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updateTeachForm.takeCreditHour"
                  placeholder="Enter rank"
                />
              </div>

              <div class="d-flex justify-content-evenly">
                <button
                  type="button"
                  class="btn btn-primary"
                  @click="updateTeach(
                      updateTeachForm,
                      updateTeachForm.teacherNo,
                      updateTeachForm.courseNo
                    )
                    "
                >
                  提交
                </button>
                <button
                  type="button"
                  class="btn btn-warning"
                  @click="resetTeachForm"
                >
                  重置
                </button>
                <button
                  type="button"
                  class="btn btn-danger"
                  @click="deleteTeach"
                >
                  删除
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeEditTeachModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import axios from 'axios'
import _ from 'lodash'

export default {
  data () {
    return {
      activeAddCourseModal: false,
      activeTeachCourseModal: false,
      activeUpdateCourseModal: false,
      activeEditTeachModal: false,
      addCourseForm: {
        courseNo: '',
        name: '',
        creditHour: 0,
        type: 0,
      },
      teachCourseForm: {
        teacherNo: '',
        courseNo: '',
        year: 0,
        semester: 0,
        takeCreditHour: 0,
      },
      updateCourseForm: {
        No: '',
        name: '',
        creditHour: 0,
        type: 0,
      },
      updateTeachForm: {
        teacherNo: '',
        courseNo: '',
        year: 0,
        semester: 0,
        takeCreditHour: 0,
      },
      teachers: [],
      courses: [],
      message: '',
      showMessage: false,
      showAlert: false,
      currentPage: 1,
      pageSize: 5,
      courseNo: '',
    }
  },

  computed: {
    totalPages () {
      return Math.ceil(this.courses.length / this.pageSize)
    },

    displayedCourses () {
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      return this.courses.slice(startIndex, endIndex)
    },

    pages () {
      const pagesArray = []
      for (let i = 1; i <= this.totalPages; ++i) {
        pagesArray.push(i)
      }
      return pagesArray
    },

    activeModal () {
      return (
        this.activeAddCourseModal ||
        this.activeTeachCourseModal ||
        this.activeUpdateCourseModal ||
        this.activeEditTeachModal
      )
    },

    controlModal () {
      const body = document.querySelector('body')
      if (this.activeModal) {
        this.showAlert = false
        body.classList.add('modal-open')
      } else {
        body.classList.remove('modal-open')
      }
    },
  },

  methods: {
    goToPage (page) {
      // 跳转到指定页
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    },

    initForm () {
      // 初始化/重置表单
      this.addCourseForm.courseNo = ''
      this.addCourseForm.name = ''
      this.addCourseForm.creditHour = 0
      this.addCourseForm.type = 0
      // teacherCourseForm
      this.teachCourseForm.teacherNo = ''
      this.teachCourseForm.courseNo = ''
      this.teachCourseForm.year = 0
      this.teachCourseForm.semester = 0
      this.teachCourseForm.takeCreditHour = 0
    },

    manageMessage (status) {
      if (status) {
        this.showMessage = true
        return true
      } else {
        this.showAlert = true
        return false
      }
    },

    getCourses () {
      // 获取课程信息
      const path = 'http://localhost:5000/courses'
      axios
        .get(path)
        .then((res) => {
          this.courses = res.data.courses
        })
        .catch((error) => {
          console.error(error)
        })
    },

    addCourse (payload) {
      // 添加课程信息
      const path = 'http://localhost:5000/courses'
      axios
        .put(path, payload)
        .then((res) => {
          this.getCourses()
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

    toggleAddCourseModal () {
      this.activeAddCourseModal = !this.activeAddCourseModal
    },

    getTeachers (courseNo) {
      // 获取课程主讲信息
      const path = `http://localhost:5000/courses/${courseNo}`
      axios
        .get(path)
        .then((res) => {
          this.teachers = res.data.teachers
          console.log(this.teachers)
        })
        .catch((error) => {
          console.error(error)
        })
    },

    teachCourse (payload, courseNo) {
      // 添加主讲课程信息
      const path = `http://localhost:5000/courses/${courseNo}`
      axios
        .put(path, payload)
        .then((res) => {
          this.getCourses()
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.initForm()
            this.toggleTeachCourseModal()
          }
        })
        .catch((error) => {
          console.error(error)
          this.getCourses()
        })
      return false
    },

    toggleTeachCourseModal () {
      this.activeTeachCourseModal = !this.activeTeachCourseModal
    },

    updateCourse (payload, courseNo) {
      // 更新课程信息
      const path = `http://localhost:5000/courses/${courseNo}`
      axios
        .post(path, payload)
        .then((res) => {
          this.getCourses()
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

    resetUpdateCourseForm () {
      for (let i = 0; i < this.displayedCourses.length; ++i) {
        if (this.displayedCourses[i].No === this.updateCourseForm.No) {
          this.updateCourseForm = _.cloneDeep(this.displayedCourses[i])
          break
        }
      }
    },

    toggleUpdateCourseModal (course) {
      if (course) {
        this.updateCourseForm = _.cloneDeep(course)
      }
      this.activeUpdateCourseModal = !this.activeUpdateCourseModal
    },

    handleDeleteCourse (courseNo) {
      // 删除课程
      const path = `http://localhost:5000/courses/${courseNo}`
      axios
        .delete(path)
        .then((res) => {
          this.getCourses()
          this.message = res.data.message
          this.showMessage = true
        })
        .catch((error) => {
          console.error(error)
          this.getCourses()
        })
    },

    updateTeach (payload, teacherNo, courseNo) {
      // 更新课程主讲信息
      const path = `http://localhost:5000/courses/${courseNo}/${teacherNo}`
      axios
        .post(path, payload)
        .then((res) => {
          this.getTeachers(courseNo)
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.toggleEditTeachModal(null)
          }
        })
        .catch((error) => {
          console.error(error)
          this.getTeachers(courseNo)
        })
    },

    resetTeachForm () {
      for (let i = 0; i < this.teachers.length; ++i) {
        if (teachers[i].teacherNo === this.updateTeachForm.teacherNo) {
          this.updateTeachForm = _.cloneDeep(this.teachers[i])
          break
        }
      }
    },

    deleteTeach () {
      // 删除课程登记
      const path = `http://localhost:5000/courses/${this.updateTeachForm.courseNo}/${this.updateTeachForm.teacherNo}`
      axios
        .delete(path)
        .then((res) => {
          this.getTeachers(this.updateTeachForm.courseNo)
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.toggleEditTeachModal(null)
          }
        })
        .catch((error) => {
          console.error(error)
          this.getTeachers(this.updateTeachForm.courseNo)
        })
    },

    toggleEditTeachModal (teacher) {
      if (teacher) {
        this.updateTeachForm = _.cloneDeep(teacher)
      }
      this.activeEditTeachModal = !this.activeEditTeachModal
    },

    fundCheck () {
      // 经费检查
      const path = `http://localhost:5000/courses/check/${this.courseNo}`
      axios
        .get(path)
        .then((res) => {
          this.message = res.data.message
          this.showMessage = true
        })
        .catch((error) => {
          console.error(error)
        })
    },
  },

  created () {
    this.getCourses()
  },
}
</script>

<style scoped>
.top {
  margin-top: 20px;
}
</style>
