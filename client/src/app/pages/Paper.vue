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
          <div class="d-flex me-3">
            <button
              type="button"
              class="btn btn-primary"
              style="font-weight: bold"
              @click="togglePublishPaperModal"
            >
              发表论文登记
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
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                论文序号
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                论文名称
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                发表源
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                发表年份
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
                类型
              </th>
              <th scope="col" style="white-space: nowrap; font-weight: bold">
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
              <td>{{ getPaperType(paper.type) }}</td>
              <td>{{ getPaperLevel(paper.level) }}</td>
              <th scope="col">
                <div class="dropdown">
                  <button
                    class="btn btn-primary dropdown-toggle"
                    type="button"
                    data-mdb-toggle="dropdown"
                    aria-expanded="false"
                    style="font-weight: bold; white-space: nowrap"
                    @click="getAuthors(paper.No)"
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
                  style="font-weight: bold; white-space: nowrap"
                  @click="handleDeletePaper(paper.No)"
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

    <!-- add new paper modal -->
    <!-- <div
      ref="addPaperModal"
      class="modal fade"
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
            <form @submit.prevent="submitAddPaperForm">
              <div class="mb-3">
                <label class="form-label">论文序号</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="addPaperForm.paperNo"
                  placeholder="Enter PaperNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">论文名称</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="addPaperForm.name"
                  placeholder="Enter name"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">发表源</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="addPaperForm.source"
                  placeholder="Enter source"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">发表年份</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="addPaperForm.publishYear"
                  placeholder="Enter publishYear"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">论文类型</label>
                <select
                  class="form-select"
                  aria-label="Default select example"
                  v-model="addPaperForm.type"
                >
                  <option value="1">1-full paper</option>
                  <option value="2">2-short paper</option>
                  <option value="3">3-poster paper</option>
                  <option value="4">4-demo paper</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">论文级别</label>
                <select
                  class="form-select"
                  aria-label="Default select example"
                  v-model="addPaperForm.level"
                >
                  <option value="1">1-CCF-A</option>
                  <option value="2">2-CCF-B</option>
                  <option value="3">3-CCF-C</option>
                  <option value="4">4-中文 CCF-A</option>
                  <option value="3">5-中文 CCFB</option>
                  <option value="4">6-无级别</option>
                </select>
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
    <div v-if="activeAddPaperModal" class="modal-backdrop fade show"></div> -->

    <!-- Add paper modal -->
    <div
      class="modal modal-xl fade"
      :class="{ show: activeAddPaperModal, 'd-block': activeAddPaperModal }"
      tabindex="-1"
      role="dialog"
      aria-labelledby="addPaperModalLabel"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addPaperModalLabel">添加论文</h5>
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
          <div class="modal-body">
            <form @submit.prevent="submitAddPaperForm">
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
    <!-- End of Add paper modal -->

    <!-- add publish paper modal -->
    <div
      ref="addPaperModal"
      class="modal fade"
      :class="{
        show: activePublishPaperModal,
        'd-block': activePublishPaperModal,
      }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">发表论文登记</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="togglePublishPaperModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="alert alert-danger" v-if="showAlert" role="alert">
            {{ this.message }}
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitPublishPaperForm">
              <div class="mb-3">
                <label class="form-label">教师工号</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="publishPaperForm.teacherNo"
                  placeholder="Enter TeacherNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">论文序号</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="publishPaperForm.paperNo"
                  placeholder="Enter PaperNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">排名</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="publishPaperForm.rank"
                  placeholder="Enter rank"
                />
              </div>
              <div class="mb-3">
                <input
                  type="checkbox"
                  class="form-check-input"
                  v-model="publishPaperForm.isCoAuthor"
                />
                <label class="form-check-label">是否为通讯作者</label>
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
    <div v-if="activePublishPaperModal" class="modal-backdrop fade show"></div>

    <!-- update paper modal -->
    <div
      ref="updatePaperModal"
      class="modal fade"
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
            <form @submit.prevent="submitUpdatePaperForm">
              <div class="mb-3">
                <label class="form-label">论文序号</label>
                <input
                  type="text"
                  class="form-control"
                  disabled="true"
                  v-model="updatePaperForm.No"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">论文名称</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updatePaperForm.name"
                  placeholder="Enter name"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">发表源</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updatePaperForm.source"
                  placeholder="Enter source"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">发表年份</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updatePaperForm.publishYear"
                  placeholder="Enter publishYear"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">论文类型</label>
                <select
                  class="form-select"
                  aria-label="Default select example"
                  v-model="updatePaperForm.type"
                >
                  <option value="1">1-full paper</option>
                  <option value="2">2-short paper</option>
                  <option value="3">3-poster paper</option>
                  <option value="4">4-demo paper</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">论文级别</label>
                <select
                  class="form-select"
                  aria-label="Default select example"
                  v-model="updatePaperForm.level"
                >
                  <option value="1">1-CCF-A</option>
                  <option value="2">2-CCF-B</option>
                  <option value="3">3-CCF-C</option>
                  <option value="4">4-中文 CCF-A</option>
                  <option value="3">5-中文 CCFB</option>
                  <option value="4">6-无级别</option>
                </select>
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
    <div v-if="activeUpdatePaperModal" class="modal-backdrop fade show"></div>

    <!-- add publish paper modal -->
    <div
      ref="addPaperModal"
      class="modal fade"
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
            <h5 class="modal-title">发表论文修改/删除</h5>
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
          <div class="alert alert-danger" v-if="showAlert" role="alert">
            {{ this.message }}
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitUpdateAuthorForm">
              <div class="mb-3">
                <label class="form-label">教师工号</label>
                <input
                  type="text"
                  class="form-control"
                  disabled="true"
                  v-model="updateAuthorForm.teacherNo"
                  placeholder="Enter TeacherNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">论文序号</label>
                <input
                  type="text"
                  disabled="true"
                  class="form-control"
                  v-model="updateAuthorForm.paperNo"
                  placeholder="Enter PaperNo"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">排名</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="updateAuthorForm.rank"
                  placeholder="Enter rank"
                />
              </div>
              <div class="mb-3">
                <input
                  type="checkbox"
                  class="form-check-input"
                  v-model="updateAuthorForm.isCoAuthor"
                />
                <label class="form-check-label">是否为通讯作者</label>
              </div>
              <div class="d-flex justify-content-evenly">
                <button type="submit" class="btn btn-primary">提交</button>
                <button
                  type="button"
                  class="btn btn-warning"
                  @click="resetAuthorForm"
                >
                  重置
                </button>
                <button
                  type="button"
                  class="btn btn-danger"
                  @click="deleteAuthor"
                >
                  删除
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeEditAuthorModal" class="modal-backdrop fade show"></div>
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
      activePublishPaperModal: false,
      activeUpdatePaperModal: false,
      activeEditAuthorModal: false,
      addPaperForm: {
        paperNo: 0,
        name: '',
        source: '',
        publishYear: '',
        type: 0,
        level: 0,
      },
      publishPaperForm: {
        teacherNo: '',
        paperNo: 0,
        rank: 0,
        isCoAuthor: false,
      },
      updatePaperForm: {
        No: 0,
        name: '',
        source: '',
        publishYear: '',
        type: 0,
        level: 0,
      },
      updateAuthorForm: {
        teacherNo: '',
        paperNo: 0,
        rank: 0,
        isCoAuthor: false,
      },
      authors: [],
      addAuthors: [],
      papers: [],
      message: '',
      showMessage: false,
      showAlert: false,
      currentPage: 1,
      pageSize: 5,
      teacherNo: '',
    }
  },

  computed: {
    totalPages() {
      return Math.ceil(this.papers.length / this.pageSize)
    },

    displayedPapers() {
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      return this.papers.slice(startIndex, endIndex)
    },

    pages() {
      const pagesArray = []
      for (let i = 1; i <= this.totalPages; ++i) {
        pagesArray.push(i)
      }
      return pagesArray
    },

    addPaperFormValid() {
      return (
        this.addPaperForm.paperNo &&
        this.addPaperForm.name &&
        this.addPaperForm.source &&
        this.addPaperForm.publishYear &&
        this.addPaperForm.type &&
        this.addPaperForm.level
      )
    },

    publishPaperFormValid() {
      return (
        this.publishPaperForm.teacherNo &&
        this.publishPaperForm.paperNo &&
        this.publishPaperForm.rank
      )
    },

    updatePaperFormValid() {
      return (
        this.updatePaperForm.name &&
        this.updatePaperForm.source &&
        this.updatePaperForm.publishYear &&
        this.updatePaperForm.type &&
        this.updatePaperForm.level
      )
    },

    updateAuthorFormValid() {
      return (
        this.updateAuthorForm.rank &&
        this.updateAuthorForm.isCoAuthor !== undefined
      )
    },
  },

  methods: {
    addAuthor() {
      this.addAuthors.push({
        teacherNo: '',
        rank: '',
        isCoAuthor: false,
      })
    },

    removeAuthor(index) {
      this.addAuthors.splice(index, 1)
    },

    goToPage(page) {
      // 跳转到指定页
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    },

    setAlertMessage(message) {
      this.message = message
      this.showAlert = true
    },

    submitAddPaperForm() {
      if (this.addPaperFormValid) {
        this.addPaper(this.addPaperForm)
      } else {
        this.setAlertMessage('请填写完整信息')
      }
    },

    submitPublishPaperForm() {
      if (this.publishPaperFormValid) {
        this.publishPaper(this.publishPaperForm, this.publishPaperForm.paperNo)
      } else {
        this.setAlertMessage('请填写完整信息')
      }
    },

    submitUpdatePaperForm() {
      if (this.updatePaperFormValid) {
        this.updatePaper(this.updatePaperForm, this.updatePaperForm.No)
      } else {
        this.setAlertMessage('请填写完整信息')
      }
    },

    submitUpdateAuthorForm() {
      if (this.updateAuthorFormValid) {
        this.updateAuthor(
          this.updateAuthorForm,
          this.updateAuthorForm.teacherNo,
          this.updateAuthorForm.paperNo
        )
      } else {
        this.setAlertMessage('请填写完整信息')
      }
    },

    initForm() {
      // 初始化/重置表单
      this.addPaperForm.paperNo = 0
      this.addPaperForm.name = ''
      this.addPaperForm.source = ''
      this.addPaperForm.publishYear = ''
      this.addPaperForm.type = 0
      this.addPaperForm.level = 0
      // publishPaperForm
      this.publishPaperForm.teacherNo = ''
      this.publishPaperForm.paperNo = 0
      this.publishPaperForm.rank = 0
      this.publishPaperForm.isCoAuthor = false
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

    addPaper(payload) {
      // 添加论文信息
      const path = 'http://localhost:5000/papers'
      axios
        .put(path, payload)
        .then((res) => {
          this.getPapers()
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
      this.activeAddPaperModal = !this.activeAddPaperModal
      if (this.activeAddPaperModal) {
        this.showAlert = false
      }
    },

    getAuthors(paperNo) {
      // 获取论文作者信息
      const path = `http://localhost:5000/papers/${paperNo}`
      axios
        .get(path)
        .then((res) => {
          this.authors = res.data.authors
        })
        .catch((error) => {
          console.error(error)
        })
    },

    publishPaper(payload, paperNo) {
      // 添加发表论文信息
      const path = `http://localhost:5000/papers/${paperNo}`
      axios
        .put(path, payload)
        .then((res) => {
          this.getPapers(true)
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.initForm()
            this.togglePublishPaperModal()
          }
        })
        .catch((error) => {
          console.error(error)
          this.getPapers()
        })
      return false
    },

    togglePublishPaperModal() {
      this.activePublishPaperModal = !this.activePublishPaperModal
      if (this.activePublishPaperModal) {
        this.showAlert = false
      }
    },

    updatePaper(payload, paperNo) {
      // 更新论文信息
      const path = `http://localhost:5000/papers/${paperNo}`
      axios
        .post(path, payload)
        .then((res) => {
          this.getPapers(true)
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
      for (let i = 0; i < this.displayedPapers.length; ++i) {
        if (this.displayedPapers[i].No === this.updatePaperForm.No) {
          this.updatePaperForm = _.cloneDeep(this.displayedPapers[i])
          break
        }
      }
    },

    toggleUpdatePaperModal(paper) {
      if (paper) {
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

    updateAuthor(payload, teacherNo, paperNo) {
      // 更新论文发表信息
      const path = `http://localhost:5000/papers/${paperNo}/${teacherNo}`
      axios
        .post(path, payload)
        .then((res) => {
          this.getAuthors(paperNo)
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.toggleEditAuthorModal(null)
          }
        })
        .catch((error) => {
          console.error(error)
          this.getAuthors(paperNo)
        })
    },

    resetAuthorForm() {
      for (let i = 0; i < this.authors.length; ++i) {
        if (authors[i].teacherNo === this.updateAuthorForm.teacherNo) {
          this.updateAuthorForm = _.cloneDeep(this.authors[i])
          break
        }
      }
    },

    deleteAuthor() {
      // 删除论文登记
      const path = `http://localhost:5000/papers/${this.updateAuthorForm.paperNo}/${this.updateAuthorForm.teacherNo}`
      axios
        .delete(path)
        .then((res) => {
          this.getAuthors(this.updateAuthorForm.paperNo)
          this.message = res.data.message
          if (this.manageMessage(res.data.status)) {
            this.toggleEditAuthorModal(null)
          }
        })
        .catch((error) => {
          console.error(error)
          this.getAuthors(this.updateAuthorForm.paperNo)
        })
    },

    toggleEditAuthorModal(author) {
      if (author) {
        this.updateAuthorForm = _.cloneDeep(author)
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
