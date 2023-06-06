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
              @click="getProjects(false)"
              style="white-space: nowrap; font-weight: bold"
            >
              项目查询
            </button>
          </div>
        </div>
        <table class="table table-hover text-center table-striped">
          <thead>
            <tr class="fs-6">
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('No')"
              >
                项目号
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('name')"
              >
                &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;项目名称&nbsp; &nbsp; &nbsp;
                &nbsp;&nbsp;
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('source')"
              >
                &nbsp;&nbsp;项目来源&nbsp;&nbsp;
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('type')"
              >
                项目类型
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('funds')"
              >
                项目总经费
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('startYear')"
              >
                开始年份
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('endYear')"
              >
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
              <td style="white-space: nowrap">
                {{ getProjectType(project.type) }}
              </td>
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
                  data-mdb-toggle="modal"
                  data-mdb-target="#deleteProjectModal"
                  style="white-space: nowrap; font-weight: bold"
                  @click="deleteProjectNo = project.No"
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

    <!-- add new project modal -->
    <div
      class="modal fade modal-xl"
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
            <form @submit.prevent="addProject">
              <div class="table-responsive">
                <table class="table table-bordered">
                  <tbody>
                    <tr>
                      <td style="width: 250px">
                        <label class="form-label" style="font-weight: bold"
                          >项目号:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="addProjectForm.projectNo"
                          required
                        />
                      </td>
                      <td colspan="2">
                        <label class="form-label" style="font-weight: bold"
                          >项目名称:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="addProjectForm.name"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >项目来源:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="addProjectForm.source"
                          required
                        />
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >项目类型:</label
                        >
                        <select
                          class="form-select"
                          aria-label="Default select example"
                          v-model="addProjectForm.type"
                          required
                        >
                          <option value="1">1-国家级项目</option>
                          <option value="2">2-省部级项目</option>
                          <option value="3">3-市厅级项目</option>
                          <option value="4">4-企业合作项目</option>
                          <option value="5">5-其他类型项目</option>
                        </select>
                      </td>
                      <td>
                        <label
                          class="form-label select-label"
                          style="font-weight: bold"
                          >项目经费:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="addProjectForm.funds"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label">开始年份</label>
                        <input
                          type="text"
                          class="form-control"
                          v-model="addProjectForm.startYear"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label">结束年份</label>
                        <input
                          type="text"
                          class="form-control"
                          v-model="addProjectForm.endYear"
                        />
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="text-right">
                <button type="button" class="btn btn-info" @click="addTake">
                  添加负责人
                </button>
              </div>
              <hr />
              <div class="table-responsive">
                <table class="table table-bordered text-center">
                  <thead>
                    <tr>
                      <th>项目号</th>
                      <th>教师工号</th>
                      <th>排名</th>
                      <th>承担经费</th>
                      <th>删除</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(take, index) in addTakes" :key="index">
                      <td>
                        <input
                          type="number"
                          class="form-control"
                          disabled="true"
                          v-model="addProjectForm.projectNo"
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          class="form-control"
                          v-model="take.teacherNo"
                          required
                        />
                      </td>
                      <td>
                        <input
                          type="number"
                          class="form-control"
                          v-model="take.rank"
                          required
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          class="form-control"
                          v-model="take.takeFunds"
                          required
                        />
                      </td>
                      <td>
                        <button
                          type="button"
                          class="btn btn-outline-danger"
                          @click="removeTake(index)"
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

    <!-- update project modal -->
    <div
      ref="updateProjectModal"
      class="modal fade modal-xl"
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
            <form @submit.prevent="updateProject(updateProjectForm.No)">
              <div class="table-responsive">
                <table class="table table-bordered">
                  <tbody>
                    <tr>
                      <td style="width: 250px">
                        <label class="form-label" style="font-weight: bold"
                          >项目号:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          disabled="true"
                          v-model="updateProjectForm.No"
                          required
                        />
                      </td>
                      <td colspan="2">
                        <label class="form-label" style="font-weight: bold"
                          >项目名称:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="updateProjectForm.name"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >项目来源:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="updateProjectForm.source"
                          required
                        />
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >项目类型:</label
                        >
                        <select
                          class="form-select"
                          aria-label="Default select example"
                          v-model="updateProjectForm.type"
                          required
                        >
                          <option value="1">1-国家级项目</option>
                          <option value="2">2-省部级项目</option>
                          <option value="3">3-市厅级项目</option>
                          <option value="4">4-企业合作项目</option>
                          <option value="5">5-其他类型项目</option>
                        </select>
                      </td>
                      <td>
                        <label
                          class="form-label select-label"
                          style="font-weight: bold"
                          >项目经费:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="updateProjectForm.funds"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label">开始年份</label>
                        <input
                          type="text"
                          class="form-control"
                          v-model="updateProjectForm.startYear"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label">结束年份</label>
                        <input
                          type="text"
                          class="form-control"
                          v-model="updateProjectForm.endYear"
                        />
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="text-right">
                <button
                  type="button"
                  class="btn btn-info"
                  @click="addUpdateTake"
                >
                  添加负责人
                </button>
              </div>
              <hr />
              <div class="table-responsive">
                <table class="table table-bordered text-center">
                  <thead>
                    <tr>
                      <th>项目号</th>
                      <th>教师工号</th>
                      <th>排名</th>
                      <th>承担经费</th>
                      <th>删除</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(take, index) in updateTakes" :key="index">
                      <td>
                        <input
                          type="number"
                          class="form-control"
                          disabled="true"
                          v-model="updateProjectForm.No"
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          class="form-control"
                          v-model="take.teacherNo"
                          required
                        />
                      </td>
                      <td>
                        <input
                          type="number"
                          class="form-control"
                          v-model="take.rank"
                          required
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          class="form-control"
                          v-model="take.takeFunds"
                          required
                        />
                      </td>
                      <td>
                        <button
                          type="button"
                          class="btn btn-outline-danger"
                          @click="removeUpdateTake(index)"
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

    <!-- Take modal -->
    <div
      class="modal modal fade"
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
            <h5 class="modal-title">负责人查看</h5>
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
          <div class="modal-body">
            <table class="table table-bordered text-center">
              <thead>
                <tr>
                  <th>项目号</th>
                  <th>教师工号</th>
                  <th>排名</th>
                  <th>承担经费</th>
                </tr>
              </thead>
              <tbody>
                <tr class="text-center align-middle fs-6">
                  <td>{{ take.projectNo }}</td>
                  <td>{{ take.teacherNo }}</td>
                  <td>{{ take.rank }}</td>
                  <td>{{ take.takeFunds }}</td>
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
      id="deleteProjectModal"
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
          <div class="modal-body text-danger text fs-1">确认删除此项目吗？</div>
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
              @click="handleDeleteProject(deleteProjectNo)"
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
import { getProjectType } from '../utils/helpFunc.vue'

export default {
  data() {
    return {
      activeAddProjectModal: false,
      activeUpdateProjectModal: false,
      activeEditTakeModal: false,
      activedeleteProjectModal: false,
      addProjectForm: {
        projectNo: '',
        name: '',
        source: '',
        type: 0,
        funds: 0.0,
        startYear: 0,
        endYear: 0,
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
      take: {
        projectNo: '',
        teacherNo: '',
        rank: '',
        takeFunds: 0.0,
      },
      takes: [],
      addTakes: [],
      updateTakes: [],
      projects: [],
      message: '',
      showMessage: false,
      showAlert: false,
      currentPage: 1,
      pageSize: 5,
      teacherNo: '',
      deleteProjectNo: '',
      sortByField: 'No',
      sortDirection: 'asc',
    }
  },

  computed: {
    sortedProject() {
      const field = this.sortByField
      const direction = this.sortDirection === 'asc' ? 1 : -1
      return this.projects.slice().sort((a, b) => {
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
      return Math.ceil(this.projects.length / this.pageSize)
    },

    displayedProjects() {
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      return this.sortedProject.slice(startIndex, endIndex)
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

    addTake() {
      this.addTakes.push({
        teacherNo: '',
        rank: '',
        takeFunds: 0.0,
      })
    },

    addUpdateTake() {
      this.updateTakes.push({
        teacherNo: '',
        rank: '',
        takeFunds: 0.0,
      })
    },

    removeTake(index) {
      this.addTakes.splice(index, 1)
    },

    removeUpdateTake(index) {
      this.updateTakes.splice(index, 1)
    },

    goToPage(page) {
      // 跳转到指定页
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    },

    initForm() {
      // 初始化/重置表单
      this.addProjectForm.projectNo = ''
      this.addProjectForm.name = ''
      this.addProjectForm.source = ''
      this.addProjectForm.type = 0
      this.addProjectForm.funds = 0.0
      this.addProjectForm.startYear = 0
      this.addProjectForm.endYear = 0
      // takeProjectForm
      this.addTakes = []
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

    getProjects(flag = false) {
      if (this.teacherNo) {
        this.queryProject(this.teacherNo, flag)
      } else {
        this.getAllProjects(flag)
      }
    },

    queryProject(teacherNo, flag = false) {
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

    getAllProjects(flag = false) {
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

    addProject() {
      const path = 'http://localhost:5000/projects'
      const payload = {
        project: this.addProjectForm,
        takes: this.addTakes,
      }
      // 添加项目信息
      axios
        .put(path, payload)
        .then((res) => {
          this.getProjects(res.data.status)
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

    toggleAddProjectModal() {
      this.initForm()
      this.activeAddProjectModal = !this.activeAddProjectModal
      if (this.activeAddProjectModal) {
        this.showAlert = false
      }
    },

    getTakes(projectNo, isUpdate = false) {
      // 获取项目承担信息
      const path = `http://localhost:5000/projects/${projectNo}`
      axios
        .get(path)
        .then((res) => {
          if (isUpdate) {
            this.updateTakes = res.data.takes
          } else {
            this.takes = res.data.takes
          }
        })
        .catch((error) => {
          console.error(error)
        })
    },

    updateProject(projectNo) {
      // 更新项目信息
      const path = `http://localhost:5000/projects/${projectNo}`
      const payload = {
        project: this.updateProjectForm,
        takes: this.updateTakes,
      }
      axios
        .post(path, payload)
        .then((res) => {
          this.getProjects(res.data.status)
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

    resetUpdateProjectForm() {
      this.getTakes(this.updateProjectForm.No, true)
      for (let i = 0; i < this.displayedProjects.length; ++i) {
        if (this.displayedProjects[i].No === this.updateProjectForm.No) {
          this.updateProjectForm = _.cloneDeep(this.displayedProjects[i])
          break
        }
      }
    },

    toggleUpdateProjectModal(project) {
      if (project) {
        this.getTakes(project.No, true)
        this.updateProjectForm = _.cloneDeep(project)
      }
      this.activeUpdateProjectModal = !this.activeUpdateProjectModal
      if (this.activeUpdateProjectModal) {
        this.showAlert = false
      }
    },

    handleDeleteProject(projectNo) {
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

    toggleEditTakeModal(take) {
      if (take) {
        this.take = _.cloneDeep(take)
      }
      this.activeEditTakeModal = !this.activeEditTakeModal
      if (this.activeEditTakeModal) {
        this.showAlert = false
      }
    },

    getProjectType,
  },

  created() {
    this.getProjects()
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
  margin-left: 50px;
  margin-right: 50px;
}
</style>
