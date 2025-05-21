<template>
  <section id="register-section" class="page-section">
    <h2>📝 Create an Account</h2>
    <form @submit.prevent="register" class="register-form">
      <label for="username">Username <span class="required">*</span></label>
      <input
        type="text"
        id="username"
        v-model="user.username"
        required
        autocomplete="off"
        placeholder="Enter a username"
      />

      <label for="name">Full Name <span class="required">*</span></label>
      <input
        type="text"
        id="name"
        v-model="user.name"
        required
        autocomplete="off"
        placeholder="Enter your full name"
      />

      <label for="email">Email <span class="required">*</span></label>
      <input
        type="email"
        id="email"
        v-model="user.email"
        required
        autocomplete="off"
        placeholder="Enter your email"
      />

      <label for="password">Password <span class="required">*</span></label>
      <input
        type="password"
        id="password"
        v-model="user.password"
        required
        autocomplete="off"
        placeholder="Enter a password"
      />

      <label for="confirmPassword">Confirm Password <span class="required">*</span></label>
      <input
        type="password"
        id="confirmPassword"
        v-model="user.confirmPassword"
        required
        autocomplete="off"
        placeholder="Re-enter your password"
      />

      <button type="submit">Create Account</button>

      <p class="login-link">
        Already have an account?
        <router-link :to="{ name: 'login' }">Sign in here</router-link>
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
        name: "",
        email: "",
        password: "",
        confirmPassword: "",
        role: "user",
      },
    };
  },
  methods: {
    error(msg) {
      alert(msg);
    },
    success(msg) {
      alert(msg);
    },
    register() {
      if (this.user.password !== this.user.confirmPassword) {
        this.error("Passwords do not match.");
        return;
      }

      authService
        .register(this.user)
        .then((response) => {
          if (response.status === 201) {
            this.success("Thanks for registering. You can now log in.");
            this.$router.push({ name: "login" });
          }
        })
        .catch((error) => {
          const res = error.response;
          if (!res) {
            this.error(error);
          } else if (res.status === 400) {
            this.error(res.data.detail || "Registration failed.");
          } else {
            this.error(res.data.message || "Unexpected error occurred.");
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

.login-link {
  margin-top: 1.5rem;
  text-align: center;
}

.required {
  color: red;
}
</style>
