<template>
  <div class="container top scp">
    <div class="row">
      <div class="col-sm-12">
        <h2 class="text-primary text-center">发表论文登记查询</h2>
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
              class="btn btn-success"
              style="font-weight: bold"
              @click="toggleAddPaperModal"
            >
              论文登记
            </button>
          </div>
          <div class="form-outline mb-1 me-3" style="width: 15%">
            <input type="text" class="form-control" v-model="teacherNo" />
            <label class="form-label" style="font-weight: bold"
              >教师工号:</label
            >
          </div>
          <div class="d-flex me-3">
            <button
              type="button"
              class="btn btn-info"
              @click="getPapers(false)"
              style="font-weight: bold"
            >
              论文查询
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
                论文序号
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('name')"
              >
                论文名称
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('source')"
              >
                发表源
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('publishYear')"
              >
                发表年份
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('type')"
              >
                类型
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('level')"
              >
                类别
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                作者
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                论文更新
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                论文删除
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              class="text-center align-middle fs-6"
              v-for="paper in displayedPapers"
              :key="paper.No"
            >
              <td>{{ paper.No }}</td>
              <td>{{ paper.name }}</td>
              <td>{{ paper.source }}</td>
              <td>{{ paper.publishYear }}</td>
              <td style="white-space: nowrap">
                {{ getPaperType(paper.type) }}
              </td>
              <td style="white-space: nowrap">
                {{ getPaperLevel(paper.level) }}
              </td>
              <th scope="col">
                <div class="dropdown">
                  <button
                    class="btn btn-primary dropdown-toggle"
                    type="button"
                    data-mdb-toggle="dropdown"
                    aria-expanded="false"
                    style="font-weight: bold; white-space: nowrap"
                    @click="getAuthors(paper.No, false)"
                  >
                    查看作者
                  </button>
                  <ul
                    class="dropdown-menu"
                    aria-labelledby="dropdownMenuButton"
                  >
                    <li v-for="author in authors" :key="author.rank">
                      <button
                        type="button"
                        class="dropdown-item text-center"
                        v-bind:class="{
                          'text-success': author.isCoAuthor,
                          'text-black': !author.isCoAuthor,
                        }"
                        @click="toggleEditAuthorModal(author)"
                      >
                        {{ author.teacherNo }}
                      </button>
                    </li>
                  </ul>
                </div>
              </th>
              <td>
                <button
                  type="button"
                  class="btn btn-warning"
                  style="font-weight: bold; white-space: nowrap"
                  @click="toggleUpdatePaperModal(paper)"
                >
                  更新
                </button>
              </td>
              <td>
                <button
                  type="button"
                  class="btn btn-danger"
                  data-mdb-toggle="modal"
                  data-mdb-target="#deletePaperModal"
                  style="font-weight: bold; white-space: nowrap"
                  @click="deletePaperNo = paper.No"
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

    <!-- Add paper modal -->
    <div
      class="modal modal-xl fade"
      :class="{ show: activeAddPaperModal, 'd-block': activeAddPaperModal }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">论文登记</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleAddPaperModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="alert alert-danger" v-if="showAlert" role="alert">
            {{ this.message }}
          </div>
          <div class="modal-body">
            <form @submit.prevent="addPaper">
              <div class="table-responsive">
                <table class="table table-bordered">
                  <tbody>
                    <tr>
                      <td style="width: 200px">
                        <label class="form-label" style="font-weight: bold"
                          >论文序号:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="addPaperForm.paperNo"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >论文标题:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="addPaperForm.name"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >发表源:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="addPaperForm.source"
                          required
                        />
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >发表年份:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="addPaperForm.publishYear"
                          required
                        />
                      </td>
                      <td>
                        <label
                          class="form-label select-label"
                          style="font-weight: bold"
                          >论文类型:</label
                        >
                        <select
                          class="form-select"
                          v-model="addPaperForm.type"
                          required
                        >
                          <option value="1">1-full paper</option>
                          <option value="2">2-short paper</option>
                          <option value="3">3-poster paper</option>
                          <option value="4">4-demo paper</option>
                        </select>
                      </td>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >论文级别:</label
                        >
                        <select
                          class="form-select"
                          v-model="addPaperForm.level"
                        >
                          <option value="1">1-CCF-A</option>
                          <option value="2">2-CCF-B</option>
                          <option value="3">3-CCF-C</option>
                          <option value="4">4-中文 CCF-A</option>
                          <option value="3">5-中文 CCFB</option>
                          <option value="4">6-无级别</option>
                        </select>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div class="text-right">
                <button type="button" class="btn btn-info" @click="addAuthor">
                  添加作者
                </button>
              </div>
              <hr />
              <div class="table-responsive">
                <table class="table table-bordered text-center">
                  <thead>
                    <tr>
                      <th>论文序号</th>
                      <th>教师工号</th>
                      <th>排名</th>
                      <th>通讯作者</th>
                      <th>删除</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(author, index) in addAuthors" :key="index">
                      <td>
                        <input
                          type="number"
                          class="form-control"
                          disabled="true"
                          v-model="addPaperForm.paperNo"
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          class="form-control"
                          v-model="author.teacherNo"
                          required
                        />
                      </td>
                      <td>
                        <input
                          type="number"
                          class="form-control"
                          v-model="author.rank"
                          required
                        />
                      </td>
                      <td>
                        <div class="d-flex justify-content-center">
                          <input
                            type="checkbox"
                            class="form-check-input"
                            v-model="author.isCoAuthor"
                          />
                        </div>
                      </td>
                      <td>
                        <button
                          type="button"
                          class="btn btn-outline-danger"
                          @click="removeAuthor(index)"
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

    <!-- update paper modal -->
    <div
      class="modal modal-xl fade"
      :class="{
        show: activeUpdatePaperModal,
        'd-block': activeUpdatePaperModal,
      }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">论文信息更新</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleUpdatePaperModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="alert alert-danger" v-if="showAlert" role="alert">
            {{ this.message }}
          </div>
          <div class="modal-body">
            <form @submit.prevent="updatePaper(updatePaperForm.No)">
              <div class="table-responsive">
                <table class="table table-bordered">
                  <tbody>
                    <tr>
                      <td style="width: 200px">
                        <label class="form-label" style="font-weight: bold"
                          >论文序号:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          disabled="true"
                          v-model="updatePaperForm.No"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >论文标题:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="updatePaperForm.name"
                          required
                        />
                      </td>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >发表源:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="updatePaperForm.source"
                          required
                        />
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >发表年份:</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          v-model="updatePaperForm.publishYear"
                          required
                        />
                      </td>
                      <td>
                        <label
                          class="form-label select-label"
                          style="font-weight: bold"
                          >论文类型:</label
                        >
                        <select
                          class="form-select"
                          v-model="updatePaperForm.type"
                          required
                        >
                          <option value="1">1-full paper</option>
                          <option value="2">2-short paper</option>
                          <option value="3">3-poster paper</option>
                          <option value="4">4-demo paper</option>
                        </select>
                      </td>
                      <td>
                        <label class="form-label" style="font-weight: bold"
                          >论文级别:</label
                        >
                        <select
                          class="form-select"
                          v-model="updatePaperForm.level"
                        >
                          <option value="1">1-CCF-A</option>
                          <option value="2">2-CCF-B</option>
                          <option value="3">3-CCF-C</option>
                          <option value="4">4-中文 CCF-A</option>
                          <option value="3">5-中文 CCFB</option>
                          <option value="4">6-无级别</option>
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
                  @click="addUpdateAuthor"
                >
                  添加作者
                </button>
              </div>
              <hr />
              <div class="table-responsive">
                <table class="table table-bordered text-center">
                  <thead>
                    <tr>
                      <th>论文序号</th>
                      <th>教师工号</th>
                      <th>排名</th>
                      <th>通讯作者</th>
                      <th>删除</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(author, index) in updateAuthors" :key="index">
                      <td>
                        <input
                          type="number"
                          class="form-control"
                          disabled="true"
                          v-model="updatePaperForm.No"
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          class="form-control"
                          v-model="author.teacherNo"
                          required
                        />
                      </td>
                      <td>
                        <input
                          type="number"
                          class="form-control"
                          v-model="author.rank"
                          required
                        />
                      </td>
                      <td>
                        <div class="d-flex justify-content-center">
                          <input
                            type="checkbox"
                            class="form-check-input"
                            v-model="author.isCoAuthor"
                          />
                        </div>
                      </td>
                      <td>
                        <button
                          type="button"
                          class="btn btn-outline-danger"
                          @click="removeUpdateAuthor(index)"
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
                  @click="resetUpdatePaperForm"
                >
                  重置
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Author modal -->
    <div
      ref="addPaperModal"
      class="modal modal fade"
      :class="{
        show: activeEditAuthorModal,
        'd-block': activeEditAuthorModal,
      }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">作者查看</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleEditAuthorModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <table class="table table-bordered text-center">
              <thead>
                <tr>
                  <th>论文序号</th>
                  <th>教师工号</th>
                  <th>排名</th>
                  <th>通讯作者</th>
                </tr>
              </thead>
              <tbody>
                <tr class="text-center align-middle fs-6">
                  <td>{{ author.paperNo }}</td>
                  <td>{{ author.teacherNo }}</td>
                  <td>{{ author.rank }}</td>
                  <td>{{ author.isCoAuthor ? '是' : '否' }}</td>
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
      id="deletePaperModal"
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
          <div class="modal-body text-danger text fs-1">确认删除此论文吗？</div>
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
              @click="handleDeletePaper(deletePaperNo)"
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
import { getPaperLevel, getPaperType } from '../utils/helpFunc.vue'

export default {
  data() {
    return {
      activeAddPaperModal: false,
      activeUpdatePaperModal: false,
      activeEditAuthorModal: false,
      addPaperForm: {
        paperNo: '',
        name: '',
        source: '',
        publishYear: '',
        type: 0,
        level: 0,
      },
      updatePaperForm: {
        No: 0,
        name: '',
        source: '',
        publishYear: '',
        type: 0,
        level: 0,
      },
      author: {
        paperNo: '',
        teacherNo: '',
        rank: '',
        isCoAuthor: false,
      },
      authors: [],
      addAuthors: [],
      updateAuthors: [],
      papers: [],
      message: '',
      showMessage: false,
      showAlert: false,
      currentPage: 1,
      pageSize: 10,
      teacherNo: '',
      deletePaperNo: '',
      sortByField: 'No',
      sortDirection: 'asc',
    }
  },

  computed: {
    sortedPaper() {
      const field = this.sortByField
      const direction = this.sortDirection === 'asc' ? 1 : -1
      return this.papers.slice().sort((a, b) => {
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
      return Math.ceil(this.papers.length / this.pageSize)
    },

    displayedPapers() {
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      return this.sortedPaper.slice(startIndex, endIndex)
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

    addAuthor() {
      this.addAuthors.push({
        teacherNo: '',
        rank: '',
        isCoAuthor: false,
      })
    },

    addUpdateAuthor() {
      this.updateAuthors.push({
        teacherNo: '',
        rank: '',
        isCoAuthor: false,
      })
    },

    removeAuthor(index) {
      this.addAuthors.splice(index, 1)
    },

    removeUpdateAuthor(index) {
      this.updateAuthors.splice(index, 1)
    },

    goToPage(page) {
      // 跳转到指定页
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    },

    initForm() {
      // 初始化/重置表单
      this.addPaperForm.paperNo = ''
      this.addPaperForm.name = ''
      this.addPaperForm.source = ''
      this.addPaperForm.publishYear = ''
      this.addPaperForm.type = 0
      this.addPaperForm.level = 0
      this.addAuthors = []
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

    getPapers(flag = false) {
      if (this.teacherNo) {
        this.queryPaper(this.teacherNo, flag)
      } else {
        this.getAllPapers(flag)
      }
    },

    queryPaper(teacherNo, flag = false) {
      // 查询论文信息
      const path = `http://localhost:5000/papers/teacher/${teacherNo}`
      axios
        .get(path)
        .then((res) => {
          if (!flag) {
            this.message = res.data.message
          }
          this.showMessage = true
          if (res.data.status) {
            this.papers = res.data.papers
          }
        })
        .catch((error) => {
          console.error(error)
        })
    },

    getAllPapers(flag = false) {
      // 获取论文信息
      const path = 'http://localhost:5000/papers'
      axios
        .get(path)
        .then((res) => {
          this.papers = res.data.papers
          this.showMessage = flag
        })
        .catch((error) => {
          console.error(error)
        })
    },

    addPaper() {
      const payload = {
        paper: this.addPaperForm,
        authors: this.addAuthors,
      }
      // 添加论文信息
      const path = 'http://localhost:5000/papers'
      axios
        .put(path, payload)
        .then((res) => {
          this.getPapers(res.data.status)
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.initForm()
            this.toggleAddPaperModal()
          }
        })
        .catch((error) => {
          console.error(error)
          this.getPapers()
        })
    },

    toggleAddPaperModal() {
      this.initForm()
      this.activeAddPaperModal = !this.activeAddPaperModal
      if (this.activeAddPaperModal) {
        this.showAlert = false
      }
    },

    getAuthors(paperNo, isUpdate = false) {
      // 获取论文作者信息
      const path = `http://localhost:5000/papers/${paperNo}`
      axios
        .get(path)
        .then((res) => {
          if (isUpdate) {
            this.updateAuthors = res.data.authors
          } else {
            this.authors = res.data.authors
          }
        })
        .catch((error) => {
          console.error(error)
        })
    },

    updatePaper(paperNo) {
      // 更新论文信息
      const path = `http://localhost:5000/papers/${paperNo}`
      const payload = {
        paper: this.updatePaperForm,
        authors: this.updateAuthors,
      }
      axios
        .post(path, payload)
        .then((res) => {
          this.getPapers(res.data.status)
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.toggleUpdatePaperModal(null)
          }
        })
        .catch((error) => {
          console.error(error)
          this.getPapers()
        })
    },

    resetUpdatePaperForm() {
      this.getAuthors(this.updatePaperForm.No, true)
      for (let i = 0; i < this.displayedPapers.length; ++i) {
        if (this.displayedPapers[i].No === this.updatePaperForm.No) {
          this.updatePaperForm = _.cloneDeep(this.displayedPapers[i])
          break
        }
      }
    },

    toggleUpdatePaperModal(paper) {
      if (paper) {
        this.getAuthors(paper.No, true)
        this.updatePaperForm = _.cloneDeep(paper)
      }
      this.activeUpdatePaperModal = !this.activeUpdatePaperModal
      if (this.activeUpdatePaperModal) {
        this.showAlert = false
      }
    },

    handleDeletePaper(paperNo) {
      // 删除论文
      const path = `http://localhost:5000/papers/${paperNo}`
      axios
        .delete(path)
        .then((res) => {
          this.getPapers(true)
          this.message = res.data.message
          this.showMessage = true
        })
        .catch((error) => {
          console.error(error)
          this.getPapers()
        })
    },

    toggleEditAuthorModal(author) {
      if (author) {
        this.author = _.cloneDeep(author)
      }
      this.activeEditAuthorModal = !this.activeEditAuthorModal
      if (this.activeEditAuthorModal) {
        this.showAlert = false
      }
    },

    getPaperLevel,
    getPaperType,
  },

  created() {
    this.getPapers()
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
