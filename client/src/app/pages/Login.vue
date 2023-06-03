<template>
  <section class="h-100 gradient-form scp" style="background-color: #eee">
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-xl-10">
          <div class="card rounded-3 text-black">
            <div class="row g-0">
              <div class="col-lg-6">
                <div class="card-body p-md-5 mx-md-4">
                  <div class="text-center">
                    <img
                      src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/lotus.webp"
                      style="width: 185px"
                      alt="logo"
                    />
                    <h4 class="mt-1 mb-5 pb-1 text-primary">
                      USTC 教学科研登记系统
                    </h4>
                  </div>
                  <div
                    v-bind:class="{
                    		'alert alert-success': loginFlag,
                    		'alert alert-danger': !loginFlag,
                    	}"
                    v-if="showLoginAlert"
                    role="alert"
                  >
                    {{ this.message }}
                  </div>
                  <form>
                    <p>Please login to your account</p>

                    <div class="mb-4">
                      <input
                        type="email"
                        id="form2Example11"
                        class="form-control"
                        placeholder="User name"
                        v-model="loginForm.username"
                      />
                      <!-- <label class="form-label" for="form2Example11">Username</label> -->
                    </div>

                    <div class="mb-4">
                      <input
                        type="password"
                        id="form2Example22"
                        class="form-control"
                        placeholder="Password"
                        v-model="loginForm.password"
                      />
                      <!-- <label class="form-label" for="form2Example22">Password</label> -->
                    </div>

                    <div class="text-center d-flex justify-content-center">
                      <button
                        class="btn btn-primary gradient-custom-2 mb-3"
                        type="button"
                        @click="login(loginForm)"
                      >
                        Log in
                      </button>
                      <!-- <div></div> -->
                      <!-- <h class="text-muted" href="#!">Forgot password?</h> -->
                    </div>

                    <div
                      class="d-flex align-items-center justify-content-center pb-4"
                    >
                      <p class="mb-0 me-2">Don't have an account?</p>
                      <button
                        type="button"
                        class="btn btn-outline-danger"
                        @click="toggleRegisterModal"
                      >
                        Create new
                      </button>
                    </div>
                  </form>
                </div>
              </div>
              <div class="col-lg-6 d-flex align-items-center gradient-custom-2">
                <div class="text-white px-3 py-4 p-md-5 mx-md-4">
                  <h4 class="mb-4">We are more than just a company</h4>
                  <p class="small mb-0">
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit,
                    sed do eiusmod tempor incididunt ut labore et dolore magna
                    aliqua. Ut enim ad minim veniam, quis nostrud exercitation
                    ullamco laboris nisi ut aliquip ex ea commodo consequat.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- add new book modal -->
  <div
    ref="registerModal"
    class="modal fade scp"
    :class="{
    		show: activeRegisterModal,
    		'd-block': activeRegisterModal,
    	}"
    tabindex="-1"
    role="dialog"
  >
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Create a new account</h5>
          <button
            type="button"
            class="close"
            data-dismiss="modal"
            aria-label="Close"
            @click="toggleRegisterModal"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div
          v-bind:class="{
          		'alert alert-success': registerFlag,
          		'alert alert-danger': !registerFlag,
          	}"
          v-if="showRegisterAlert"
          role="alert"
        >
          {{ this.message }}
        </div>

        <div class="modal-body">
          <form>
            <div class="mb-3">
              <label for="addUsername" class="form-label">Username:</label>
              <input
                type="text"
                class="form-control"
                id="addUserName"
                placeholder="User name"
                v-model="registerForm.username"
              />
            </div>
            <div class="mb-3">
              <label for="addPassword" class="form-label">Password:</label>
              <input
                type="text"
                class="form-control"
                id="addPassword"
                placeholder="password"
                v-model="registerForm.password"
              />
            </div>
            <div class="d-flex justify-content-evenly">
              <button
                type="button"
                class="btn btn-primary btn"
                @click="register(registerForm)"
              >
                Register
              </button>
              <button
                type="button"
                class="btn btn-danger btn"
                @click="registerReset"
              >
                Reset
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
  <div v-if="activeRegisterModal" class="modal-backdrop fade show"></div>
  <!-- edit book modal -->

</template>

<script>
import axios from 'axios'
import Alert from '../components/Alert.vue'

export default {
	data () {
		return {
			activeRegisterModal: false,
			showRegisterAlert: false,
			registerFlag: false,
			showLoginAlert: false,
			loginFlag: false,
			message: '',
			registerForm: {
				username: '',
				password: '',
			},
			loginForm: {
				username: '',
				password: '',
			},
		}
	},
	components: {
		alert: Alert,
	},
	methods: {
		toggleRegisterModal () {
			const body = document.querySelector('body')
			this.activeRegisterModal = !this.activeRegisterModal
			this.showRegisterAlert = false
			if (this.activeAddBookModal) {
				body.classList.add('modal-open')
			} else {
				body.classList.remove('modal-open')
			}
		},
		register (payload) {
			const path = 'http://localhost:5000/login/register'
			axios
				.put(path, payload)
				.then((res) => {
					this.showRegisterAlert = true
					this.message = res.data.message
					this.registerFlag = res.data.flag
					console.log(this.registerFlag, res.data.flag, res.data.flag == true, res.data.flag === true)
				})
				.catch((error) => {
					console.error(error)
				})
		},
		registerReset () {
			this.registerForm.username = ''
			this.registerForm.password = ''
		},
		login (payload) {
			const path = 'http://localhost:5000/login/login'
			axios
				.put(path, payload)
				.then((res) => {
					this.showLoginAlert = true
					this.message = res.data.message
					this.loginFlag = res.data.flag
					if (this.loginFlag) {
						window.location.href = "http://localhost:5173/Books"
					}
				})
				.catch((error) => {
					console.error(error)
				})
		}
	},
}
</script>

<style>
.gradient-custom-2 {
	/* fallback for old browsers */
	background: #fccb90;

	/* Chrome 10-25, Safari 5.1-6 */
	background: -webkit-linear-gradient(to right,
			#ee7724,
			#d8363a,
			#dd3675,
			#b44593);


	/* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
	background: linear-gradient(to right, #ee7724, #d8363a, #dd3675, #b44593);
}

@media (min-width: 768px) {
	.gradient-form {
		height: 100vh !important;
	}
}

@media (min-width: 769px) {
	.gradient-custom-2 {
		border-top-right-radius: 0.3rem;
		border-bottom-right-radius: 0.3rem;
	}
}
</style>
