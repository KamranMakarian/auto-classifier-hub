<template>
  <div class="admin">
    <h1>🛠️ Admin Dashboard</h1>
    <p class="description">
      As an administrator, you can view and delete any registered user or model in the system.
    </p>

    <!-- Users List -->
    <section class="admin-section">
      <h2>👥 Registered Users</h2>
      <div v-if="users.length" class="list-box">
        <ul class="item-list">
          <li v-for="user in users" :key="user.id">
            {{ user.username }} ({{ user.email }})
            <button class="danger" @click="deleteUser(user.id)">Delete</button>
          </li>
        </ul>
      </div>
      <p v-else>No users found.</p>
    </section>

    <!-- Models List -->
    <section class="admin-section">
      <h2>🧠 All Models</h2>
      <div v-if="models.length" class="list-box">
        <ul class="item-list">
          <li v-for="model in models" :key="model.id">
            {{ model.name }} (Owner ID: {{ model.user_id }})
            <button class="danger" @click="deleteModel(model.file_path)">Delete</button>
          </li>
        </ul>
      </div>
      <p v-else>No models found.</p>
    </section>

    <div v-if="message" class="message-box">{{ message }}</div>
    <div v-if="error" class="message-box error">{{ error }}</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      users: [],
      models: [],
      message: "",
      error: ""
    };
  },
  mounted() {
    this.fetchUsers();
    this.fetchModels();
  },
  methods: {
    async fetchUsers() {
      try {
        const res = await axios.get("/admin/users", {
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        });
        this.users = res.data;
      } catch (err) {
        this.error = "Failed to load users.";
      }
    },
    async fetchModels() {
      try {
        const res = await axios.get("/list-models", {
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        });
        this.models = res.data.models || res.data;
      } catch (err) {
        this.error = "Failed to load models.";
      }
    },
    async deleteUser(userId) {
      if (!confirm("Are you sure you want to delete this user?")) return;
      try {
        await axios.delete(`/admin/user/${userId}`, {
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        });
        this.message = `User ${userId} deleted.`;
        this.fetchUsers();
      } catch (err) {
        this.error = "Failed to delete user.";
      }
    },
    async deleteModel(filePath) {
      const fileName = filePath.split("/").pop();
      if (!confirm(`Are you sure you want to delete model "${fileName}"?`)) return;
      try {
        await axios.delete("/delete-model", {
          params: { file_name: fileName },
          headers: { Authorization: `Bearer ${this.$store.state.token}` }
        });
        this.message = `Model "${fileName}" deleted.`;
        this.fetchModels();
      } catch (err) {
        this.error = "Failed to delete model.";
      }
    }
  }
};
</script>

<style scoped>
.admin {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.description {
  margin-bottom: 1rem;
  color: #444;
}

.admin-section {
  margin-top: 2rem;
}

.list-box {
  border: 1px solid #ccc;
  background: #fdfdfd;
  padding: 1rem;
  border-radius: 4px;
  min-height: 120px;
}

.item-list {
  list-style: none;
  padding: 0;
}

.item-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

button {
  padding: 0.3rem 0.8rem;
  background-color: #007acc;
  color: white;
  border: none;
  cursor: pointer;
}

button.danger {
  background-color: crimson;
}

button:hover:not(:disabled) {
  background-color: #005fa3;
}

button.danger:hover:not(:disabled) {
  background-color: #a30000;
}

.message-box {
  border: 1px solid #999;
  padding: 1rem;
  margin-top: 1rem;
  background-color: #f5f5f5;
}

.message-box.error {
  color: red;
  background-color: #ffe5e5;
  border-color: red;
}
</style>
