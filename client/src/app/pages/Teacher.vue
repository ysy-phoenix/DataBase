<template>
  <div class="container top scp">
    <div class="row">
      <div class="col-sm-12">
        <h2 class="text-primary text-center">教师查看</h2>
        <br />

        <table class="table table-hover text-center table-striped">
          <thead>
            <tr class="fs-6">
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('No')"
              >
                教师工号
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('name')"
              >
                教师姓名
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('gender')"
              >
                教师性别
              </th>
              <th
                scope="col"
                style="white-space: nowrap; font-weight: bold"
                @click="sortBy('title')"
              >
                教师职称
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              class="text-center align-middle fs-6"
              v-for="teacher in displayedTeachers"
              :key="teacher.No"
            >
              <td>{{ teacher.No }}</td>
              <td>{{ teacher.name }}</td>
              <td>{{ getGender(teacher.gender) }}</td>
              <td>{{ getTitle(teacher.title) }}</td>
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
  </div>
</template>

<script>
import axios from 'axios'
import _ from 'lodash'
import { getTitle, getGender } from '../utils/helpFunc.vue'

export default {
  data() {
    return {
      currentPage: 1,
      pageSize: 10,
      teachers: [],
    }
  },

  computed: {
    sortedTeacher() {
      const field = this.sortByField
      const direction = this.sortDirection === 'asc' ? 1 : -1
      return this.teachers.slice().sort((a, b) => {
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
      return Math.ceil(this.teachers.length / this.pageSize)
    },

    displayedTeachers() {
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      return this.sortedTeacher.slice(startIndex, endIndex)
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

    goToPage(page) {
      // 跳转到指定页
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    },

    getTeachers() {
      // 获取论文信息
      const path = 'http://localhost:5000/teachers'
      axios
        .get(path)
        .then((res) => {
          this.teachers = res.data.teachers
        })
        .catch((error) => {
          console.error(error)
        })
    },

    getGender,
    getTitle,
  },

  created() {
    this.getTeachers()
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
