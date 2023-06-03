<template>
  <div class="d-flex flex-column min-vh-100">
    <main class="flex-grow-1">
      <nav
        class="navbar navbar-light navbar-expand-lg scp"
        style="background-color: #e3f2fd"
      >
        <!-- Container wrapper -->
        <div class="container-fluid">
          <!-- Toggle button -->
          <button
            class="navbar-toggler"
            type="button"
            data-mdb-toggle="collapse"
            data-mdb-target="#navbarCenteredExample"
            aria-controls="navbarCenteredExample"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <i class="fas fa-bars"></i>
          </button>

          <!-- Collapsible wrapper -->
          <div
            class="collapse navbar-collapse justify-content-center"
            id="navbarCenteredExample"
          >
            <!-- Left links -->
            <ul class="navbar-nav mb-2 mb-lg-0">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="/">Home</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">Link</a>
              </li>
              <!-- Navbar dropdown -->
              <li class="nav-item dropdown">
                <a
                  class="nav-link dropdown-toggle"
                  href="#"
                  id="navbarDropdown"
                  role="button"
                  data-mdb-toggle="dropdown"
                  aria-expanded="false"
                >
                  Dropdown
                </a>
                <!-- Dropdown menu -->
                <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                  <li>
                    <a class="dropdown-item" href="#">Action</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#">Another action</a>
                  </li>
                  <li><hr class="dropdown-divider" /></li>
                  <li>
                    <a class="dropdown-item" href="#">Something else here</a>
                  </li>
                </ul>
              </li>
              <li class="nav-item">
                <a class="nav-link disabled">Disabled</a>
              </li>
            </ul>
            <!-- Left links -->
          </div>
          <!-- Collapsible wrapper -->
        </div>
        <!-- Container wrapper -->
      </nav>
      <div class="mar">
        <!-- Tabs navs -->
        <ul
          class="nav nav-tabs mb-3 justify-content-center"
          id="ex-with-icons"
          role="tablist"
        >
          <li class="nav-item" role="presentation">
            <a
              class="nav-link active"
              id="ex-with-icons-tab-1"
              data-mdb-toggle="tab"
              href="#ex-with-icons-tabs-1"
              role="tab"
              aria-controls="ex-with-icons-tabs-1"
              aria-selected="true"
              ><i class="fas fa-chart-pie fa-fw me-2"></i>论文登记</a
            >
          </li>
          <li class="nav-item" role="presentation">
            <a
              class="nav-link"
              id="ex-with-icons-tab-2"
              data-mdb-toggle="tab"
              href="#ex-with-icons-tabs-2"
              role="tab"
              aria-controls="ex-with-icons-tabs-2"
              aria-selected="false"
              ><i class="fas fa-chart-line fa-fw me-2"></i>项目登记</a
            >
          </li>
          <li class="nav-item" role="presentation">
            <a
              class="nav-link"
              id="ex-with-icons-tab-3"
              data-mdb-toggle="tab"
              href="#ex-with-icons-tabs-3"
              role="tab"
              aria-controls="ex-with-icons-tabs-3"
              aria-selected="false"
              ><i class="fas fa-cogs fa-fw me-2"></i>课程登记</a
            >
          </li>
          <li class="nav-item" role="presentation">
            <a
              class="nav-link"
              id="ex-with-icons-tab-4"
              data-mdb-toggle="tab"
              href="#ex-with-icons-tabs-4"
              role="tab"
              aria-controls="ex-with-icons-tabs-4"
              aria-selected="false"
              ><i class="fab fa-app-store-ios fa-fw me-2"></i>查询</a
            >
          </li>
        </ul>
        <!-- Tabs navs -->

        <!-- Tabs content -->

        <div class="tab-content" id="ex-with-icons-content">
          <div
            class="tab-pane fade show active"
            id="ex-with-icons-tabs-1"
            role="tabpanel"
            aria-labelledby="ex-with-icons-tab-1"
          >
            <Paper />
          </div>
          <div
            class="tab-pane fade"
            id="ex-with-icons-tabs-2"
            role="tabpanel"
            aria-labelledby="ex-with-icons-tab-2"
          >
            <Project />
          </div>
          <div
            class="tab-pane fade"
            id="ex-with-icons-tabs-3"
            role="tabpanel"
            aria-labelledby="ex-with-icons-tab-3"
          >
            <Course />
          </div>
          <div
            class="tab-pane fade"
            id="ex-with-icons-tabs-4"
            role="tabpanel"
            aria-labelledby="ex-with-icons-tab-4"
          >
            <Query />
          </div>
        </div>
      </div>
    </main>
    <!-- Tabs content -->
    <!-- Copyright -->
    <footer>
      <div
        class="text-center p-3 scp"
        style="background-color: rgba(0, 0, 0, 0.2)"
      >
        © 2023 Copyright:
        <a class="text-reset fw-bold" href="https://github.com/ysy-phoenix"
          >https://github.com/ysy-phoenix</a
        >
      </div>
    </footer>
    <!-- Copyright -->
  </div>
</template>

<script setup>
// import Books from './Books.vue'
import Paper from './Paper.vue'
import Project from './Project.vue'
import Course from './Course.vue'
import Query from './Query.vue'
</script>

<style>
.mar {
    margin: 20px;
}
</style>
