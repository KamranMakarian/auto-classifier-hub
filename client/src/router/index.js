import { createRouter as createRouter, createWebHistory } from 'vue-router'
import { useStore } from 'vuex'

import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import LogoutView from '../views/LogoutView.vue'
import RegisterView from '../views/RegisterView.vue'
import TrainView from '../views/TrainView.vue';
import PredictView from '../views/PredictView.vue'
import HelpView from '../views/HelpView.vue';
import ContactView from '../views/ContactView.vue'


const routes = [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        requiresAuth: false
      }
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
      meta: {
        requiresAuth: false
      }
    },
    {
      path: "/logout",
      name: "logout",
      component: LogoutView,
      meta: {
        requiresAuth: false
      }
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
      meta: {
        requiresAuth: false
      }
    },
    {
      path: "/train",
      name: "train",
      component: TrainView,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/predict",
      name: "predict",
      component: PredictView,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/help",
      name: "help",
      component: HelpView,
      meta: {
        requiresAuth: false
      }
    },
    {
      path: "/contact",
      name: "contact",
      component: ContactView,
      meta: {
        requiresAuth: false
      }, 
      props: (route) => {
        const store = useStore();
        return { user: store.state.user };
      }
    },
    {
      path: '/admin',
      name: 'AdminDashboard',
      component: () => import('../views/AdminDashboard.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    }    
    
  ];

// Create the router
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 };
  }
});

router.beforeEach((to) => {
  const store = useStore();

  const requiresAuth = to.matched.some(x => x.meta.requiresAuth);
  const requiresAdmin = to.matched.some(x => x.meta.requiresAdmin);

  if (requiresAuth && store.state.token === '') {
    return { name: "login" };
  }

  if (requiresAdmin && store.state.user.role !== 'admin') {
    alert("❌ Access denied: Admins only.");
    return { name: "home" };
  }
});

export default router;
