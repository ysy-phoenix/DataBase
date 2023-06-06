<template>
  <table class="table">
    <thead>
      <tr>
        <th @click="sortBy('name')">
          姓名
          <i
            v-if="sortByField === 'name' && sortDirection === 'asc'"
            class="fas fa-sort-up"
          ></i>
          <i
            v-if="sortByField === 'name' && sortDirection === 'desc'"
            class="fas fa-sort-down"
          ></i>
        </th>
        <th @click="sortBy('age')">
          年龄
          <i
            v-if="sortByField === 'age' && sortDirection === 'asc'"
            class="fas fa-sort-up"
          ></i>
          <i
            v-if="sortByField === 'age' && sortDirection === 'desc'"
            class="fas fa-sort-down"
          ></i>
        </th>
        <th @click="sortBy('gender')">
          性别
          <i
            v-if="sortByField === 'gender' && sortDirection === 'asc'"
            class="fas fa-sort-up"
          ></i>
          <i
            v-if="sortByField === 'gender' && sortDirection === 'desc'"
            class="fas fa-sort-down"
          ></i>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in sortedData" :key="item.id">
        <td>{{ item.name }}</td>
        <td>{{ item.age }}</td>
        <td>{{ item.gender }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { ref, computed } from 'vue'
import { mdbTable } from 'mdbvue'

export default {
  components: {
    mdbTable,
  },
  data() {
    return {
      data: [
        { id: 1, name: '张三', age: 25, gender: '男' },
        { id: 2, name: '李四', age: 30, gender: '男' },
        { id: 3, name: '王五', age: 28, gender: '女' },
      ],
      sortByField: 'name',
      sortDirection: 'asc',
    }
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
  },
  computed: {
    sortedData() {
      const field = this.sortByField
      const direction = this.sortDirection === 'asc' ? 1 : -1
      return this.data.slice().sort((a, b) => {
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
  },
}
</script>
