<template>
  <div class="container top scp">
    <div class="row">
      <div class="col-sm-12">
        <h2 class="text-center text-primary">承担项目登记查询</h2>
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
              style="white-space: nowrap; font-weight: bold"
              @click="toggleAddProjectModal"
            >
              项目登记
            </button>
          </div>
          <div class="d-flex me-3">
            <button
              type="button"
              class="btn btn-primary text-nowrap"
              style="white-space: nowrap; font-weight: bold"
              @click="toggleTakeProjectModal"
            >
              承担项目登记
            </button>
          </div>
          <div class="form-outline mb-1 me-1" style="width: 15%">
            <input type="text" class="form-control" v-model="projectNo" />
            <label
              class="form-label"
              style="white-space: nowrap; font-weight: bold"
              >项目号:</label
            >
          </div>
          <div class="d-flex me-3">
            <button
              type="button"
              class="btn btn-warning"
              @click="fundCheck"
              style="white-space: nowrap; font-weight: bold"
            >
              经费检查
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
              @click="getProjects"
              style="white-space: nowrap; font-weight: bold"
            >
              项目查询
            </button>
          </div>
        </div>
        <table class="table table-hover text-center table-striped">
          <thead>
            <tr class="fs-6">
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                项目号
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;项目名称&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                &nbsp;&nbsp;项目来源&nbsp;&nbsp;
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                &nbsp;项目类型&nbsp;
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                项目总经费
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                开始年份
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                结束年份
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                负责人
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                项目更新
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                项目删除
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              class="text-center align-middle fs-6"
              v-for="project in displayedProjects"
              :key="project.No"
            >
              <td>{{ project.No }}</td>
              <td>{{ project.name }}</td>
              <td>{{ project.source }}</td>
              <td>{{ getProjectType(project.type) }}</td>
              <td>{{ project.funds }}</td>
              <td>{{ project.startYear }}</td>
              <td>{{ project.endYear }}</td>
              <th scope="col">
                <div class="dropdown">
                  <button
                    class="btn btn-primary dropdown-toggle"
                    type="button"
                    data-mdb-toggle="dropdown"
                    aria-expanded="false"
                    @click="getTakes(project.No)"
                    style="white-space: nowrap; font-weight: bold"
                  >
                    查看负责人
                  </button>
                  <ul
                    class="dropdown-menu"
                    aria-labelledby="dropdownMenuButton"
                  >
                    <li v-for="take in takes" :key="take.rank">
                      <button
                        type="button"
                        class="dropdown-item text-center"
                        @click="toggleEditTakeModal(take)"
                      >
                        {{ take.teacherNo }}
                      </button>
                    </li>
                  </ul>
                </div>
              </th>
              <td>
                <button
                  type="button"
                  class="btn btn-warning"
                  @click="toggleUpdateProjectModal(project)"
                  style="white-space: nowrap; font-weight: bold"
                >
                  更新
                </button>
              </td>
              <td>
                <button
                  type="button"
                  class="btn btn-danger"
                  @click="handleDeleteProject(project.No)"
                  style="white-space: nowrap; font-weight: bold"
                >
                  删除
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

    <!-- add new project modal -->
    <div
      ref="addProjectModal"
      class="modal fade"
      :class="{ show: activeAddProjectModal, 'd-block': activeAddProjectModal }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">项目登记</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleAddProjectModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="alert alert-danger" v-if="showAlert" role="alert">
            {{ this.message }}
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitAddProjectForm">
              <div class="mb-3">
                <label class="form-label">项目号</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="addProjectForm.projectNo"
                  placeholder="Enter ProjectNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">项目名称</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="addProjectForm.name"
                  placeholder="Enter name"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">项目来源</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="addProjectForm.source"
                  placeholder="Enter source"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">项目类型</label>
                <select
                  class="form-select"
                  aria-label="Default select example"
                  v-model="addProjectForm.type"
                >
                  <option value="1">1-国家级项目</option>
                  <option value="2">2-省部级项目</option>
                  <option value="3">3-市厅级项目</option>
                  <option value="4">4-企业合作项目</option>
                  <option value="5">5-其他类型项目</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">总经费</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="addProjectForm.funds"
                  placeholder="Enter Funds"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">开始年份</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="addProjectForm.startYear"
                  placeholder="Enter source"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">结束年份</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="addProjectForm.endYear"
                  placeholder="Enter source"
                />
              </div>

              <div class="d-flex justify-content-evenly">
                <button
                  type="submit"
                  class="btn btn-primary"
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
    <div v-if="activeAddProjectModal" class="modal-backdrop fade show"></div>

    <!-- add take project modal -->
    <div
      ref="addTakeProjectModal"
      class="modal fade"
      :class="{
          show: activeTakeProjectModal,
          'd-block': activeTakeProjectModal,
        }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">承担项目登记</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleTakeProjectModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="alert alert-danger" v-if="showAlert" role="alert">
            {{ this.message }}
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitTakeProjectForm">
              <div class="mb-3">
                <label class="form-label">教师工号</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="takeProjectForm.teacherNo"
                  placeholder="Enter TeacherNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">项目号</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="takeProjectForm.projectNo"
                  placeholder="Enter ProjectNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">排名</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="takeProjectForm.rank"
                  placeholder="Enter rank"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">承担经费</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="takeProjectForm.takeFunds"
                  placeholder="Enter rank"
                />
              </div>
              <div class="d-flex justify-content-evenly">
                <button
                  type="submit"
                  class="btn btn-primary"
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
    <div v-if="activeTakeProjectModal" class="modal-backdrop fade show"></div>

    <!-- update project modal -->
    <div
      ref="updateProjectModal"
      class="modal fade"
      :class="{
          show: activeUpdateProjectModal,
          'd-block': activeUpdateProjectModal,
        }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">项目信息更新</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleUpdateProjectModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="alert alert-danger" v-if="showAlert" role="alert">
            {{ this.message }}
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitUpdateProjectForm">
              <div class="mb-3">
                <label class="form-label">项目号</label>
                <input
                  type="text"
                  class="form-control"
                  disabled="true"
                  v-model="updateProjectForm.No"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">项目名称</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updateProjectForm.name"
                  placeholder="Enter name"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">项目来源</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updateProjectForm.source"
                  placeholder="Enter source"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">项目类型</label>
                <select
                  class="form-select"
                  aria-label="Default select example"
                  v-model="updateProjectForm.type"
                >
                  <option value="1">1-国家级项目</option>
                  <option value="2">2-省部级项目</option>
                  <option value="3">3-市厅级项目</option>
                  <option value="4">4-企业合作项目</option>
                  <option value="5">5-其他类型项目</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">总经费</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updateProjectForm.funds"
                  placeholder="Enter Funds"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">开始年份</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updateProjectForm.startYear"
                  placeholder="Enter source"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">结束年份</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updateProjectForm.endYear"
                  placeholder="Enter source"
                />
              </div>
              <div class="d-flex justify-content-evenly">
                <button
                  type="submit"
                  class="btn btn-primary"
                >
                  提交
                </button>
                <button
                  type="button"
                  class="btn btn-danger"
                  @click="resetUpdateProjectForm"
                >
                  重置
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeUpdateProjectModal" class="modal-backdrop fade show"></div>

    <!-- add Edit project modal -->
    <div
      ref="addEditProjectModal"
      class="modal fade"
      :class="{
          show: activeEditTakeModal,
          'd-block': activeEditTakeModal,
        }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">承担项目修改/删除</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleEditTakeModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="alert alert-danger" v-if="showAlert" role="alert">
            {{ this.message }}
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitUpdateTakeForm">
              <div class="mb-3">
                <label class="form-label">教师工号</label>
                <input
                  type="text"
                  class="form-control"
                  disabled="true"
                  v-model="updateTakeForm.teacherNo"
                  placeholder="Enter TeacherNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">项目号</label>
                <input
                  type="text"
                  disabled="true"
                  class="form-control"
                  v-model="updateTakeForm.projectNo"
                  placeholder="Enter ProjectNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">排名</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updateTakeForm.rank"
                  placeholder="Enter rank"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">承担经费</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updateTakeForm.takeFunds"
                  placeholder="Enter rank"
                />
              </div>
              <div class="d-flex justify-content-evenly">
                <button
                  type="submit"
                  class="btn btn-primary"
                >
                  提交
                </button>
                <button
                  type="button"
                  class="btn btn-warning"
                  @click="resetTakeForm"
                >
                  重置
                </button>
                <button
                  type="button"
                  class="btn btn-danger"
                  @click="deleteTake"
                >
                  删除
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeEditTakeModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import axios from 'axios'
import _ from 'lodash'
import { getProjectType } from '../utils/helpFunc.vue'

export default {
  data () {
    return {
      activeAddProjectModal: false,
      activeTakeProjectModal: false,
      activeUpdateProjectModal: false,
      activeEditTakeModal: false,
      addProjectForm: {
        projectNo: '',
        name: '',
        source: '',
        type: 0,
        funds: 0.0,
        startYear: 0,
        endYear: 0,
      },
      takeProjectForm: {
        teacherNo: '',
        projectNo: '',
        rank: 0,
        takeFunds: 0.0,
      },
      updateProjectForm: {
        No: '',
        name: '',
        source: '',
        type: 0,
        funds: 0.0,
        startYear: 0,
        endYear: 0,
      },
      updateTakeForm: {
        teacherNo: '',
        projectNo: '',
        rank: 0,
        takeFunds: 0.0,
      },
      takes: [],
      projects: [],
      message: '',
      showMessage: false,
      showAlert: false,
      currentPage: 1,
      pageSize: 5,
      projectNo: '',
      teacherNo: '',
    }
  },

  computed: {
    totalPages () {
      return Math.ceil(this.projects.length / this.pageSize)
    },

    displayedProjects () {
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      return this.projects.slice(startIndex, endIndex)
    },

    pages () {
      const pagesArray = []
      for (let i = 1; i <= this.totalPages; ++i) {
        pagesArray.push(i)
      }
      return pagesArray
    },

    addProjectFormValid () {
      return (
        this.addProjectForm.projectNo &&
        this.addProjectForm.name &&
        this.addProjectForm.source &&
        this.addProjectForm.type &&
        this.addProjectForm.funds &&
        this.addProjectForm.startYear &&
        this.addProjectForm.endYear
      )
    },

    takeProjectFormValid () {
      return (
        this.takeProjectForm.teacherNo &&
        this.takeProjectForm.projectNo &&
        this.takeProjectForm.rank &&
        this.takeProjectForm.takeFunds
      )
    },

    updateProjectFormValid () {
      return (
        this.updateProjectForm.name &&
        this.updateProjectForm.source &&
        this.updateProjectForm.type &&
        this.updateProjectForm.funds &&
        this.updateProjectForm.startYear &&
        this.updateProjectForm.endYear
      )
    },

    updateTakeFormValid () {
      return (
        this.updateTakeForm.rank &&
        this.updateTakeForm.takeFunds
      )
    },
  },

  methods: {
    goToPage (page) {
      // 跳转到指定页
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    },

    setAlertMessage (message) {
      this.message = message
      this.showAlert = true
    },

    submitAddProjectForm () {
      if (this.addProjectFormValid) {
        this.addProject(this.addProjectForm)
      } else {
        this.setAlertMessage('请填写完整的项目信息')
      }
    },

    submitTakeProjectForm () {
      if (this.takeProjectFormValid) {
        this.takeProject(this.takeProjectForm, this.takeProjectForm.projectNo)
      } else {
        this.setAlertMessage('请填写完整的承担项目信息')
      }
    },

    submitUpdateProjectForm () {
      if (this.updateProjectFormValid) {
        this.updateProject(
          this.updateProjectForm,
          this.updateProjectForm.No
        )
      } else {
        this.setAlertMessage('请填写完整的项目信息')
      }
    },

    submitUpdateTakeForm () {
      if (this.updateTakeFormValid) {
        this.updateTake(
          this.updateTakeForm,
          this.updateTakeForm.teacherNo,
          this.updateTakeForm.projectNo
        )
      } else {
        this.setAlertMessage('请填写完整的承担项目信息')
      }
    },

    initForm () {
      // 初始化/重置表单
      this.addProjectForm.projectNo = ''
      this.addProjectForm.name = ''
      this.addProjectForm.source = ''
      this.addProjectForm.type = 0
      this.addProjectForm.funds = 0.0
      this.addProjectForm.startYear = 0
      this.addProjectForm.endYear = 0
      // takeProjectForm
      this.takeProjectForm.teacherNo = ''
      this.takeProjectForm.projectNo = ''
      this.takeProjectForm.rank = 0
      this.takeProjectForm.takeFunds = 0.0
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

    getProjects (flag = false) {
      if (this.teacherNo) {
        this.queryProject(this.teacherNo, flag)
      } else {
        this.getAllProjects(flag)
      }
    },

    queryProject (teacherNo, flag = false) {
      // 查询论文信息
      const path = `http://localhost:5000/projects/teacher/${teacherNo}`
      axios
        .get(path)
        .then((res) => {
          if (!flag) {
            this.message = res.data.message
          }
          this.showMessage = true
          if (res.data.status) {
            this.projects = res.data.projects
          }
        })
        .catch((error) => {
          console.error(error)
        })
    },

    getAllProjects (flag = false) {
      // 获取项目信息
      const path = 'http://localhost:5000/projects'
      axios
        .get(path)
        .then((res) => {
          this.projects = res.data.projects
          this.showMessage = flag
        })
        .catch((error) => {
          console.error(error)
        })
    },

    addProject (payload) {
      // 添加项目信息
      const path = 'http://localhost:5000/projects'
      axios
        .put(path, payload)
        .then((res) => {
          this.getProjects(true)
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.initForm()
            this.toggleAddProjectModal()
          }
        })
        .catch((error) => {
          console.error(error)
          this.getProjects()
        })
    },

    toggleAddProjectModal () {
      this.activeAddProjectModal = !this.activeAddProjectModal
      if (this.activeAddProjectModal) {
        this.showAlert = false
      }
    },

    getTakes (projectNo) {
      // 获取项目承担信息
      const path = `http://localhost:5000/projects/${projectNo}`
      axios
        .get(path)
        .then((res) => {
          this.takes = res.data.takes
        })
        .catch((error) => {
          console.error(error)
        })
    },

    takeProject (payload, projectNo) {
      // 添加承担项目信息
      const path = `http://localhost:5000/projects/${projectNo}`
      axios
        .put(path, payload)
        .then((res) => {
          this.getProjects(true)
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.initForm()
            this.toggleTakeProjectModal()
          }
        })
        .catch((error) => {
          console.error(error)
          this.getProjects()
        })
      return false
    },

    toggleTakeProjectModal () {
      this.activeTakeProjectModal = !this.activeTakeProjectModal
      if (this.activeTakeProjectModal) {
        this.showAlert = false
      }
    },

    updateProject (payload, projectNo) {
      // 更新项目信息
      const path = `http://localhost:5000/projects/${projectNo}`
      axios
        .post(path, payload)
        .then((res) => {
          this.getProjects(true)
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.toggleUpdateProjectModal(null)
          }
        })
        .catch((error) => {
          console.error(error)
          this.getProjects()
        })
    },

    resetUpdateProjectForm () {
      for (let i = 0; i < this.displayedProjects.length; ++i) {
        if (this.displayedProjects[i].No === this.updateProjectForm.No) {
          this.updateProjectForm = _.cloneDeep(this.displayedProjects[i])
          break
        }
      }
    },

    toggleUpdateProjectModal (project) {
      if (project) {
        this.updateProjectForm = _.cloneDeep(project)
      }
      this.activeUpdateProjectModal = !this.activeUpdateProjectModal
      if (this.activeUpdateProjectModal) {
        this.showAlert = false
      }
    },

    handleDeleteProject (projectNo) {
      // 删除项目
      const path = `http://localhost:5000/projects/${projectNo}`
      axios
        .delete(path)
        .then((res) => {
          this.getProjects(true)
          this.message = res.data.message
          this.showMessage = true
        })
        .catch((error) => {
          console.error(error)
          this.getProjects()
        })
    },

    updateTake (payload, teacherNo, projectNo) {
      // 更新项目承担信息
      const path = `http://localhost:5000/projects/${projectNo}/${teacherNo}`
      axios
        .post(path, payload)
        .then((res) => {
          this.getTakes(projectNo)
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.toggleEditTakeModal(null)
          }
        })
        .catch((error) => {
          console.error(error)
          this.getTakes(projectNo)
        })
    },

    resetTakeForm () {
      for (let i = 0; i < this.takes.length; ++i) {
        if (takes[i].teacherNo === this.updateTakeForm.teacherNo) {
          this.updateTakeForm = _.cloneDeep(this.takes[i])
          break
        }
      }
    },

    deleteTake () {
      // 删除项目登记
      const path = `http://localhost:5000/projects/${this.updateTakeForm.projectNo}/${this.updateTakeForm.teacherNo}`
      axios
        .delete(path)
        .then((res) => {
          this.getTakes(this.updateTakeForm.projectNo)
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.toggleEditTakeModal(null)
          }
        })
        .catch((error) => {
          console.error(error)
          this.getTakes(this.updateTakeForm.projectNo)
        })
    },

    toggleEditTakeModal (take) {
      if (take) {
        this.updateTakeForm = _.cloneDeep(take)
      }
      this.activeEditTakeModal = !this.activeEditTakeModal
      if (this.activeEditTakeModal) {
        this.showAlert = false
      }
    },

    fundCheck () {
      // 经费检查
      if (this.projectNo) {
        const path = `http://localhost:5000/projects/check/${this.projectNo}`
        axios
          .get(path)
          .then((res) => {
            this.message = res.data.message
            this.showMessage = true
          })
          .catch((error) => {
            console.error(error)
          })
      } else {
        this.message = '检查失败：项目号不能为空！'
        this.showMessage = true
      }
    },

    getProjectType,
  },

  created () {
    this.getProjects()
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
  margin-left: 50px;
  margin-right: 50px;
}
</style>
