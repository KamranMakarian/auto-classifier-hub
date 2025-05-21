<template>
  <div id="app-layout">
    <header>
      <h1>AutoClassifier Hub</h1>
      <p>Your gateway to no-code machine learning models for classification.</p>
    </header>

    <div class="content">
      <aside>
        <ul>
          <li><router-link to="/">Home</router-link></li>
          <li v-if="!isLoggedIn"><router-link to="/login">Login</router-link></li>
          <li v-if="isLoggedIn"><router-link to="/train">Train a Model</router-link></li>
          <li v-if="isLoggedIn"><router-link to="/predict">Manage & Predict</router-link></li>
          <li v-if="isAdmin"><router-link to="/admin">Admin Dashboard</router-link></li>
          <li><router-link to="/help">Help / FAQ</router-link></li>
          <li><router-link to="/contact">Contact Us</router-link></li>
          <li v-if="isLoggedIn"><router-link to="/logout">Logout</router-link></li>
        </ul>
      </aside>

      <main>
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    isLoggedIn() {
      return this.$store.state.token !== '';
    },
    isAdmin() {
      return this.$store.state.user?.role === 'admin';
    }
  }
};
</script>

<style scoped>
#app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

header {
  background-color: #333;
  color: white;
  padding: 1rem;
  text-align: center;
  font-family: 'Raleway', sans-serif;
}

header h1 {
  font-family: 'Montserrat', sans-serif;
}

header p {
  margin-top: 0.5rem;
  font-size: 1.05rem;
  color: #ddd;
  font-family: 'Poppins', sans-serif;
}

h1 {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.content {
  display: flex;
  flex: 1;
}

aside {
  width: 200px;
  background-color: #f3f3f3;
  padding: 1rem;
}

aside ul {
  list-style: none;
  padding: 0;
}

aside li {
  margin: 0.75rem 0;
}

aside a {
  color: #333;
  text-decoration: none;
}

aside a:hover {
  text-decoration: underline;
}

main {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}
</style>
