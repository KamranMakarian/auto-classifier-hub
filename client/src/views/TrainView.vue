<template>
    <div class="train">
      <h1>📊 Train a Model</h1>
      <p class="description">
        Upload a CSV file and configure training options like model type, target variable, test ratio, and optional hyperparameters.
        Once submitted, your model will be trained and saved for future predictions.
      </p>
  
      <form @submit.prevent="submit" class="train-form" autocomplete="off">
        <div class="form-group file-upload-wrapper">
          <label for="file-upload">Upload CSV <span class="required">*</span></label>
          <input
            type="file"
            id="file-upload"
            ref="fileInput"
            @change="handleFile"
            accept=".csv"
            style="display: none;"
          />
          <button type="button" @click="$refs.fileInput.click()">Choose File</button>
          <p class="file-name" v-if="fileName">📄 {{ fileName }}</p>
        </div>
  
        <div class="form-group">
          <label for="model_type">Model Type<span class="required">*</span></label>
          <select id="model_type" v-model="form.model_type" required>
            <option disabled value="">-- Select Model --</option>
            <option value="logisticregression">Logistic Regression</option>
            <option value="randomforest">Random Forest</option>
            <option value="neuralnet">Neural Net</option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="target">Target Column<span class="required">*</span></label>
          <input type="text" id="target" v-model="form.target" required placeholder="Enter target column name" />
        </div>
  
        <div class="form-group">
          <label for="test_size">Test Size (0.0 - 1.0)<span class="required">*</span></label>
          <input type="number" id="test_size" v-model="form.test_size" step="0.01" min="0" max="1" required />
        </div>
  
        <div class="form-group">
          <label for="file_name">Model File Name</label>
          <input type="text" id="file_name" v-model="form.file_name" placeholder="Optional filename" />
        </div>
  
        <div class="form-group">
          <label for="k_folds">K-Folds</label>
          <input type="number" id="k_folds" v-model="form.k_folds" min="2" placeholder="Optional" />
        </div>
  
        <!-- Hyperparameter Section -->
        <div class="model-params" v-if="form.model_type === 'logisticregression'">
          <div class="form-group">
            <label>Penalty</label>
            <select v-model="modelParams.penalty">
              <option value="l2">l2</option>
              <option value="none">none</option>
            </select>
          </div>
          

          <div class="form-group">
            <label>Solver</label>
            <select v-model="modelParams.solver">
              <option value="liblinear">liblinear</option>
              <option value="lbfgs">lbfgs</option>
              <option value="saga">saga</option>
            </select>
          </div>

          <div class="form-group">
            <label>Max Iterations</label>
            <input type="number" v-model="modelParams.max_iter" min="10" />
          </div>

          <div class="form-group">
            <label>Regularization (C)</label>
            <input type="number" v-model="modelParams.C" step="0.1" min="0.1" />
          </div>
        </div>

        <div class="model-params" v-if="form.model_type === 'randomforest'">
          <div class="form-group">
            <label>Number of Trees</label>
            <input type="number" v-model="modelParams.n_estimators" min="10" />
          </div>

          <div class="form-group">
            <label>Max Depth</label>
            <input type="number" v-model="modelParams.max_depth" min="1" />
          </div>
          
          <div class="form-group">
            <label>Min Samples Split</label>
            <input type="number" v-model="modelParams.min_samples_split" min="2" />
          </div>

          <div class="form-group">
            <label>Min Samples Leaf</label>
            <input type="number" v-model="modelParams.min_samples_leaf" min="1" />
          </div>
          
        </div>

        <div class="model-params" v-if="form.model_type === 'neuralnet'">

          <div class="form-group">
            <label>Hidden Layers (comma separated)</label>
            <input type="text" v-model="modelParams.hidden_layer_sizes" placeholder="e.g. 64,32" />
          </div>
          
          <div class="form-group">
            <label>Activation</label>
            <select v-model="modelParams.activation">
              <option value="relu">ReLU</option>
              <option value="tanh">Tanh</option>
              <option value="sigmoid">Sigmoid</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>Epochs</label>
            <input type="number" v-model="modelParams.epochs" min="1" />
          </div>
          <div class="form-group">
            <label>Batch Size</label>
            <input type="number" v-model="modelParams.batch_size" min="1" />
          </div>

          
        </div>

  
        <button type="submit" :disabled="!file">Train Model</button>
      </form>
  
      <div class="status-section">
        <h3>Status:</h3>
        <loading-spinner :spin="isLoading" id="spinner" />
        <p v-if="message" class="status success">{{ message }}</p>
        <p v-if="error" class="status error">{{ error }}</p>
      </div>
    </div>
</template>

<script>
import axios from "axios";
import LoadingSpinner from "../components/LoadingSpinner.vue";

export default {
  components: {
    LoadingSpinner,
  },
  data() {
    return {
      file: null,
      fileName: "", 
      message: "",
      error: "",
      isLoading: false,
      form: {
        model_type: "",
        file_name: "",
        target: "",
        test_size: "",
        k_folds: "",
        modelParams: {

        }
      }
    };
  },
  methods: {
    handleFile(event) {
      const selected = event.target.files[0];
      if (selected) {
        this.file = selected;
        this.fileName = selected.name;
        this.message = "";
        this.error = "";
      }
    },
    async submit() {
      this.isLoading = true;
      this.message = "";
      this.error = "";

      const formData = new FormData();
      formData.append("file", this.file);
      formData.append("model_type", this.form.model_type);
      formData.append("target", this.form.target);
      if (this.form.file_name) formData.append("file_name", this.form.file_name);
      if (this.form.test_size) formData.append("test_size", this.form.test_size);
      if (this.form.k_folds) formData.append("k_folds", this.form.k_folds);
      // Special handling for neuralnet hidden_layer_sizes
      const paramsToSend = { ...this.modelParams };
      if (this.form.model_type === "neuralnet" && typeof paramsToSend.hidden_layer_sizes === "string") {
        paramsToSend.hidden_layer_sizes = paramsToSend.hidden_layer_sizes
          .split(",")
          .map(n => parseInt(n.trim()))
          .filter(n => !isNaN(n));
      }

      formData.append("params", JSON.stringify(paramsToSend));


      try {
        const response = await axios.post(
          `${import.meta.env.VITE_REMOTE_API}/fit`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.token}`,
              "Content-Type": "multipart/form-data"
            }
          }
        );

        this.message = response.data.message || "✅ Model trained successfully!";
      } catch (err) {
        this.error = err.response?.data?.detail || "❌ Failed to train model.";
      } finally {
        this.isLoading = false;
      }
    }
  },
  watch: {
    'form.model_type'(newType) {
      const defaults = {
        logisticregression: {
          penalty: "l2",
          solver: "liblinear",
          max_iter: 100,
          C: 1.0
        },
        randomforest: {
          n_estimators: 100,
          max_depth: 5,
          min_samples_split: 2,
          min_samples_leaf: 1
        },
        neuralnet: {
          hidden_layer_sizes: "64,32",
          activation: "relu",
          epochs: 20,
          batch_size: 32
        }
      };
      this.modelParams = defaults[newType] || {};
    }
  }
};
</script>

  
<style scoped>

.train {
  max-width: 700px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.description {
  font-size: 1rem;
  color: #444;
  margin-bottom: 1.5rem;
}
  
.train-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

  
input,
select,
textarea {
  padding: 0.5rem;
  font-size: 1rem;
}
  
button {
  padding: 0.6rem 1.5rem;
  font-size: 1rem;
  background-color: #007acc;
  color: white;
  border: none;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.success {
  color: green;
  margin-top: 1rem;
}

.error {
  color: red;
  margin-top: 1rem;
}

.status-section {
  margin-top: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

#spinner {
  color: #007acc;
  font-size: 1.5rem;
}

.status {
  font-weight: 600;
  margin-top: 0.5rem;
}

.success {
  color: green;
}

.error, .required {
  color: red;
}

.file-upload-wrapper {
  margin-top: 1rem;
}

button {
  margin-top: 0rem;
  padding: 0.75rem 1.5rem;
  background-color: #007acc;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #005fa3;
}

.file-name {
  margin-top: 0.5rem;
  color: #333;
  font-style: italic;
}

.model-params {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

  </style>