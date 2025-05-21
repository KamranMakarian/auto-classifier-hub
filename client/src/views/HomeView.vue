<template>
  <div class="home">
    <div id="heading-line">
      <h1>Welcome to AutoClassifier Hub</h1>
    </div>

    <section class="intro">
      <p>
        <strong>AutoClassifier Hub</strong> is your all-in-one platform to build, manage, and use machine learning models 🎉
        <em>no coding required</em> 🎉. Whether you're a student, researcher, or business analyst, you can train models,
        make predictions, and evaluate results directly from your browser.
      </p>

      <p>
        Just upload your dataset and configure your model settings through a friendly UI, and we’ll handle the training, evaluation,
        and saving of your models behind the scenes.
      </p>
    </section>

    <section class="features">
      <h2>What You Can Do as a Registered User:</h2>
      <p>Once you're logged into your dashboard, you can do any of the following:</p>
      <ul>
        <li>📂 Upload CSV files and train models like Logistic Regression, Random Forest, or Neural Nets.</li>
        <li>📊 Configure model parameters, test sizes, and validation options.</li>
        <li>🔎 Use your saved models to make predictions on custom data or uploaded files.</li>
        <li>⚙️ Manage your models (e.g. rename, delete, reload, etc.).</li>
        <li>❔Get help via FAQs or send us a message through the contact page.</li>
      </ul>
    </section>

    <section class="cta">
      <p>
        🚀 Ready to get started? 
        <router-link to="/login"><strong>Log in</strong></router-link> or 
        <router-link to="/register"><strong>create an account</strong></router-link> to begin your machine learning journey.
      </p>
    </section>
  </div>
</template>

<script>
export default {
  computed: {
    isLoggedIn() {
      return this.$store.state.token.length > 0;
    },
  },
};
</script>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

.intro,
.features,
.cta {
  margin-top: 1.5rem;
}

.features ul {
  list-style: none;
  padding-left: 1.5;
}

.features li {
  margin-bottom: 0.75rem;
}

a {
  color: #007acc;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>