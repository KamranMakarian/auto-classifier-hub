import './assets/main.css'

import { createApp } from 'vue'
import MyApp from './App.vue'
import { createStore } from './store'
import router from './router'
import axios from 'axios'

/* import fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faCartPlus, faTrashCan, faXmark, faMagnifyingGlass, faRotate, faTable, faGrip }
  from '@fortawesome/free-solid-svg-icons'

/* add icons to the library */
library.add(faCartPlus);
library.add(faTrashCan);
library.add(faXmark);
library.add(faMagnifyingGlass);
library.add(faRotate);
library.add(faTable);
library.add(faGrip);

/* sets the base url for server API communication with axios */
axios.defaults.baseURL = import.meta.env.VITE_REMOTE_API;

/*
 * The authorization header is set for axios when you login but what happens when
 * you come back or the page is refreshed. When that happens you need to check
 * for the token in local storage and if it exists you should set the header
 * so that it will be attached to each request.
 */
let currentToken = localStorage.getItem('token')
let currentUser = JSON.parse(localStorage.getItem('user'));

if (currentToken) {
  // Set token axios requests
  axios.defaults.headers.common['Authorization'] = `Bearer ${currentToken}`;
}


// Create the Vuex store passing in the stored credentials
const store = createStore(currentToken, currentUser);

// Axios interceptor for catching 401 Unauthorized responses
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      alert("⚠️ Your session has expired. Please log in again.");
      store.commit("LOGOUT");
      router.push("/login");
    }
    return Promise.reject(error);
  }
);

// Mount Vue app
const app = createApp(MyApp);
app.use(store);
app.use(router);

// Route guards (moved here because store is now available)
router.beforeEach((to) => {
  const requiresAuth = to.meta.requiresAuth;
  const requiresAdmin = to.meta.requiresAdmin;
  const isAuthenticated = store.state.token !== '';
  const isAdmin = store.state.user?.role === 'admin';

  if (requiresAuth && !isAuthenticated) {
    return { name: "login" };
  }

  if (requiresAdmin && !isAdmin) {
    alert("❌ Access denied: Admins only.");
    return { name: "home" };
  }
});

app.component('font-awesome-icon', FontAwesomeIcon);
app.mount('#app');

