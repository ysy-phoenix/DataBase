import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// import './assets/main.css'
// import 'bootstrap/dist/css/bootstrap.css'
import 'mdb-vue-ui-kit/css/mdb.min.css'
import '/@/common/style/font.css'

// load fonts
import 'fontsource-roboto/100.css'
import 'fontsource-roboto/300.css'
import 'fontsource-roboto/400.css'
import 'fontsource-roboto/500.css'
import 'fontsource-roboto/700.css'
import 'fontsource-roboto/900.css'
// import 'fontsource-noto-sans-sc/100.css'
import 'fontsource-noto-sans-sc/300.css'
import 'fontsource-noto-sans-sc/400.css'
import 'fontsource-noto-sans-sc/500.css'
import 'fontsource-noto-sans-sc/700.css'
// import 'fontsource-noto-sans-sc/900.css'
import 'fontsource-alata'

const app = createApp(App)

app.use(router)

router.isReady().then(() => app.mount('#app'))
