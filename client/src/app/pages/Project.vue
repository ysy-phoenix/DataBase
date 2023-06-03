<template>
  <div class="container top scp">
    <div class="row">
      <div class="col-sm-12">
        <h1 class="text-center">项目</h1>
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
              @click="toggleAddProjectModal"
            >
              项目登记
            </button>
          </div>
          <div class="d-flex me-3">
            <button
              type="button"
              class="btn btn-primary text-nowrap"
              @click="toggleTakeProjectModal"
            >
              承担项目登记
            </button>
          </div>
          <div class="mb-1 d-flex me-3">
            <input
              type="text"
              class="form-control"
              placeholder="请输入项目号"
              v-model="projectNo"
            />
          </div>
          <div class="d-flex">
            <button type="button" class="btn btn-warning" @click="fundCheck">
              经费检查
            </button>
          </div>
        </div>
        <table class="table table-hover text-center table-striped">
          <thead>
            <tr class="fs-7">
              <th scope="col">项目号</th>
              <th scope="col">项目名称</th>
              <th scope="col">项目来源</th>
              <th scope="col">项目类型</th>
              <th scope="col">项目总经费</th>
              <th scope="col">开始年份</th>
              <th scope="col">结束年份</th>
              <th scope="col">负责人</th>
              <th scope="col">项目更新</th>
              <th scope="col">项目删除</th>
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
              <td>{{ project.type }}</td>
              <td>{{ project.funds }}</td>
              <td>{{ project.startYear }}</td>
              <td>{{ project.endYear }}</td>
              <th scope="col">
                <div class="dropdown">
                  <button
                    class="btn btn-primary dropdown-toggle"
                    type="button"
                    id="dropdownMenuButton"
                    data-mdb-toggle="dropdown"
                    aria-expanded="false"
                    @click="getTakes(project.No)"
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
                >
                  Update
                </button>
              </td>
              <td>
                <button
                  type="button"
                  class="btn btn-danger"
                  @click="handleDeleteProject(project.No)"
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
            <form>
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
                  type="button"
                  class="btn btn-primary"
                  @click="addProject(addProjectForm)"
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
            <form>
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
                  type="button"
                  class="btn btn-primary"
                  @click="takeProject(takeProjectForm, takeProjectForm.projectNo)
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
            <form>
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
                  type="button"
                  class="btn btn-primary"
                  @click="updateProject(updateProjectForm, updateProjectForm.No)
                    "
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
            <form>
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
                  type="button"
                  class="btn btn-primary"
                  @click="updateTake(
                      updateTakeForm,
                      updateTakeForm.teacherNo,
                      updateTakeForm.projectNo
                    )
                    "
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

    activeModal () {
      return (
        this.activeAddProjectModal ||
        this.activeTakeProjectModal ||
        this.activeUpdateProjectModal ||
        this.activeEditTakeModal
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

    getProjects () {
      // 获取项目信息
      const path = 'http://localhost:5000/projects'
      axios
        .get(path)
        .then((res) => {
          this.projects = res.data.projects
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
          this.getProjects()
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
          this.getProjects()
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
    },

    updateProject (payload, projectNo) {
      // 更新项目信息
      const path = `http://localhost:5000/projects/${projectNo}`
      axios
        .post(path, payload)
        .then((res) => {
          this.getProjects()
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
    },

    handleDeleteProject (projectNo) {
      // 删除项目
      const path = `http://localhost:5000/projects/${projectNo}`
      axios
        .delete(path)
        .then((res) => {
          this.getProjects()
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
    },

    fundCheck () {
      // 经费检查
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
    },
  },

  created () {
    this.getProjects()
  },
}
</script>

<style scoped>
.top {
  margin-top: 20px;
}
</style>
