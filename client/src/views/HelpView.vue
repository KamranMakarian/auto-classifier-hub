<template>
  <div class="help">
    <h1>❔ Frequently Asked Questions</h1>
    <p class="intro">
      Need help? Expand the questions below or <router-link to="/contact">contact us</router-link> directly.
    </p>

    <section class="faq">
      <div
        class="question"
        v-for="(item, index) in faqs"
        :key="index"
      >
        <div
          class="question-title"
          @click="toggle(index)"
        >
          <strong>{{ item.q }}</strong>
          <span class="toggle-icon">{{ openIndex === index ? "▲" : "▼" }}</span>
        </div>
        <transition name="fade">
          <p v-if="openIndex === index" class="answer">
            {{ item.a }}
          </p>
        </transition>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "HelpView",
  data() {
    return {
      openIndex: null,
      faqs: [
        {
          q: "What kind of files can I upload?",
          a: "You can upload CSV files containing your feature data. Ensure it contains only numeric or categorical features — no missing values, and column names should be included."
        },
        {
          q: "What types of models are supported?",
          a: "Currently, the platform supports Logistic Regression, Random Forest, and Neural Networks for classification tasks. Neural Network model strictly supports binary classification only."
        },
        {
          q: "Do I need to be logged in to train or predict?",
          a: "Yes. Both training and prediction operations require authentication to protect your models and data."
        },
        {
          q: "How do I delete a model?",
          a: "Navigate to the Predict page, select your models using the checkboxes, and click the Delete button in the sidebar."
        },
        {
          q: "How can I view metadata about a model?",
          a: "On the Predict page, select a single model and click 'View Details' to retrieve information like accuracy, type, and parameters."
        },
        {
          q: "Why does uploading a second CSV file not trigger prediction?",
          a: "You must click the Predict button again after uploading the new file. The interface does not auto-run predictions on file change."
        },
        {
          q: "How do I rename a model?",
          a: "Select exactly one model in the Predict section, click 'Rename', and enter a new unique name."
        },
        {
          q: "How can I contact support?",
          a: "Use the Contact Us page to send a message directly to the team."
        },
        {
          q: "What is the Target Column?",
          a: "This is the name of the column in your CSV file that contains the labels (the output variable you want to predict). It must match exactly with a column name in your dataset."
        },
        {
          q: "What is Test Size?",
          a: "Test size defines the proportion of the dataset to reserve for evaluating the model (not used in training). A typical value is 0.2, which means 20% of your data will be used for testing."
        },
        {
          q: "What is K-Folds?",
          a: "K-Folds enables cross-validation by splitting your data into K parts. The model trains K times, each time holding out one fold for testing. Use values like 5 or 10 for a good trade-off between accuracy and performance."
        },
        {
          q: "What is the Penalty parameter (Logistic Regression)?",
          a: "This controls the regularization technique. 'l2' is the default and helps prevent overfitting. 'none' disables regularization, which may lead to overfitting on small datasets."
        },
        {
          q: "What is the Solver (Logistic Regression)?",
          a: "This determines the algorithm used for optimization. 'liblinear' is good for small datasets, 'lbfgs' is better for larger ones, and 'saga' supports large-scale and sparse data."
        },
        {
          q: "What does Max Iterations mean?",
          a: "This sets how many times the model can iterate to find the optimal parameters. Increase this if the model fails to converge (doesn't finish training properly)."
        },
        {
          q: "What is Regularization (C) in Logistic Regression?",
          a: "C is the inverse of regularization strength. Smaller values mean stronger regularization, which helps control overfitting. Try starting with C = 1.0."
        },
        {
          q: "What is Number of Trees (Random Forest)?",
          a: "This sets how many decision trees will be built. More trees usually give better accuracy but increase training time. A typical value is 100."
        },
        {
          q: "What is Max Depth (Random Forest)?",
          a: "This limits how deep each tree can grow. Shallow trees are faster and less likely to overfit; deeper trees can capture more complexity."
        },
        {
          q: "What is Min Samples Split (Random Forest)?",
          a: "This sets the minimum number of samples required to split a node. Higher values make the model more conservative (less likely to overfit)."
        },
        {
          q: "What is Min Samples Leaf (Random Forest)?",
          a: "This sets the minimum number of samples required to be at a leaf node. Useful to ensure no leaf represents only a few samples."
        },
        {
          q: "What are Hidden Layers (Neural Net)?",
          a: "Defines the structure of the neural network. Use comma-separated values like '64,32' for two hidden layers with 64 and 32 neurons. More layers/neurons can model more complexity."
        },
        {
          q: "What is Activation (Neural Net)?",
          a: "This controls how neurons fire in the network. 'relu' is fast and common, 'tanh' squashes values between -1 and 1, and 'sigmoid' is used for binary classification."
        },
        {
          q: "What are Epochs (Neural Net)?",
          a: "Epochs define how many times the model sees the entire dataset during training. More epochs can improve accuracy but also risk overfitting."
        },
        {
          q: "What is Batch Size (Neural Net)?",
          a: "This defines how many samples the model processes at once during training. Smaller batches take longer but may converge better; larger batches train faster but use more memory."
        }
      ]
    };
  },
  methods: {
    toggle(index) {
      this.openIndex = this.openIndex === index ? null : index;
    }
  }
};
</script>


<style scoped>
.help {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

.intro {
  margin-top: 0.5rem;
  font-size: 1rem;
  color: #444;
}

.faq {
  margin-top: 2rem;
}

.question {
  border-bottom: 1px solid #ddd;
  padding: 1rem 0;
}

.question-title {
  display: flex;
  justify-content: space-between;
  cursor: pointer;
  font-size: 1.05rem;
  color: #333;
}

.toggle-icon {
  font-size: 0.9rem;
  color: #666;
}

.answer {
  margin-top: 0.75rem;
  color: #555;
  line-height: 1.5;
}

.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}
</style>
