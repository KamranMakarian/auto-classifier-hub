<template>
  <section id="login-section" class="page-section">
    <h2>🔓 Please Sign In</h2>
    <form @submit.prevent="login" class="login-form">
      <label for="username">Username <span class="required">*</span></label>
      <input
        type="text"
        id="username"
        placeholder="Enter your username"
        v-model="user.username"
        required
        autocomplete="off"
      />

      <label for="password">Password <span class="required">*</span></label>
      <input
        type="password"
        id="password"
        placeholder="Enter your password"
        v-model="user.password"
        required
        autocomplete="off"
      />

      <button type="submit">Sign In</button>

      <p class="register-link">
        Don’t have an account?
        <router-link :to="{ name: 'register' }">Register here</router-link>
      </p>
    </form>
  </section>
</template>

<script>
import authService from "../services/AuthService";

export default {
  data() {
    return {
      user: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    login() {
      authService
        .login(this.user)
        .then((response) => {
          if (response.status === 200) {
            const token = response.data.access_token;

            // Decode token to get user info like role
            const payload = JSON.parse(atob(token.split('.')[1]));

            // Save token and user info in Vuex + localStorage
            this.$store.commit("SET_AUTH_TOKEN", token);
            this.$store.commit("SET_USER", {
              id: payload.sub,
              role: payload.role
            });

            this.$router.push({ name: "train" });
          }
        })
        .catch((error) => {
          const response = error.response;
          if (!response) {
            alert(error);
          } else if (response.status === 401) {
            alert("Invalid username or password.");
          } else {
            alert(response.data.message || "Login failed.");
          }
        });
    },
  },
};
</script>

<style scoped>
.page-section {
  max-width: 500px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #fff;
}

h1 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

h2 {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-top: 1rem;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.6rem;
  margin-top: 0.25rem;
  box-sizing: border-box;
}

button {
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #007acc;
  color: white;
  border: none;
  cursor: pointer;
  width: 100%;
}

button:hover {
  background-color: #005fa3;
}

.register-link {
  margin-top: 1.5rem;
  text-align: center;
}

.required {
  color: red;
}
</style>
