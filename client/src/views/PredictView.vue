<template>
    <div class="predict">
      <h1>🔎 Predict with a Model</h1>
      <p class="description">
        Select a previously trained model to make predictions. You can enter samples manually or upload a file. Once completed, you can download the predictions as a csv file. You can also rename, delete, or view details about your models.
      </p>
  
      <!-- Model Selection & Action Buttons -->
      <section class="models-section">
        <h2>Your Models:</h2>
        <div class="model-actions-layout">
          <div class="model-list-box">
            <ul v-if="models.length" class="model-list">
              <li v-for="model in models" :key="model.id">
                <label>
                  <input
                    type="checkbox"
                    :value="model.name"
                    v-model="selectedModels"
                  />
                  {{ model.name || "(Unnamed model)" }}
                </label>
              </li>
            </ul>
            <div v-else class="model-list empty">
              <p>No models found.</p>
            </div>
          </div>
  
          <div class="action-buttons">
            <button
              @click="viewDetails(selectedModels[0])"
              :disabled="selectedModels.length !== 1"
            >View Details</button>
  
            <button
              @click="loadModel(selectedModels[0])"
              :disabled="selectedModels.length !== 1"
            >Load</button>
  
            <button
              @click="renameModel(selectedModels[0])"
              :disabled="selectedModels.length !== 1"
            >Rename</button>
  
            <button
              class="danger"
              @click="deleteSelectedModels"
              :disabled="selectedModels.length === 0"
            >Delete</button>
          </div>
        </div>
  
        <div v-if="modelActionResponse || error" class="message-box">
          <p v-if="modelActionResponse">{{ modelActionResponse }}</p>
          <p v-if="error" class="error">{{ error }}</p>
        </div>
      </section>
  
      <!-- Prediction Input Section -->
      <section class="prediction-section" v-if="currentModel">
        <h2>📈 Make a Prediction</h2>
  
        <!-- Prediction Mode Switch -->
        <div class="mode-toggle">
          <label>
            <input type="radio" value="file" v-model="inputMode" />
            Upload CSV File
          </label>
          <label>
            <input type="radio" value="manual" v-model="inputMode" />
            Enter Manually
          </label>
        </div>
  
        <!-- File Upload Input -->
        <div v-if="inputMode === 'file'" class="file-upload">
          <br>
          <label for="csv-upload">Choose Sample CSV File:</label>
          <input type="file" id="csv-upload" ref="fileInput" @change="handleFile" accept=".csv" />
        </div>

        <!-- Manual Input Textarea -->
        <div v-if="inputMode === 'manual'">
          <br>
          <label for="manual-input">Enter JSON Array of Samples:</label>
          <textarea
            id="manual-input"
            v-model="jsonInput"
            rows="6"
            placeholder='[{"feature1": 1.2, "feature2": 3.4}]'
          ></textarea>
        </div>
  
        <!-- Predict Button -->
        <button @click="makePrediction">Predict</button>
  
        <!-- Tabular Results -->
        <div class="results" v-if="parsedPredictions.length">
        <label><strong>Predictions:</strong></label>
            <table class="prediction-table">
                <thead>
                <tr>
                    <th>#</th>
                    <th>Prediction</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="row in parsedPredictions" :key="row.index">
                    <td>{{ row.index }}</td>
                    <td>{{ row.value }}</td>
                </tr>
                </tbody>
            </table>
            <textarea readonly rows="6">{{ jsonOutput }}</textarea>
        </div>
        <div class="save-section" v-if="parsedPredictions.length">
          <br><label for="csvFileName"><strong>File Name:</strong></label><br>
          <input type="text" id="csvFileName" v-model="csvFileName" placeholder="predictions.csv" />

          <button @click="downloadCSV">💾 Save As CSV</button>
        </div>


      </section>
    </div>
  </template>
  


  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        models: [],
        selectedModels: [],
        currentModel: null,
        jsonInput: "",
        jsonOutput: "",
        csvFile: null,
        modelActionResponse: "",
        error: "",
        modelMetadata: null,
        inputMode: "file",
        parsedPredictions: [],
        csvFileName: "predictions.csv",
      };
    },
    mounted() {
      this.fetchModels();
    },
    methods: {
      async fetchModels() {
        try {
          const res = await axios.get(`${import.meta.env.VITE_REMOTE_API}/list-models`, {
            headers: { Authorization: `Bearer ${this.$store.state.token}` }
          });
          this.models = res.data.models || res.data;
        } catch {
          this.error = "Failed to load models.";
        }
      },
      async loadModel(modelName) {
        try {
            const formData = new FormData();
            formData.append("file_name", modelName); 

            const res = await axios.post(`${import.meta.env.VITE_REMOTE_API}/load-model`, formData, {
            headers: {
                Authorization: `Bearer ${this.$store.state.token}`,
                "Content-Type": "multipart/form-data"  
            }
            });

            this.currentModel = modelName;
            this.modelActionResponse = res.data.message || `Model "${modelName}" loaded successfully.`;
            this.jsonInput = "";
            this.jsonOutput = "";
            this.csvFile = null;
        } catch (err) {
            this.error = err.response?.data?.detail || "Failed to load model.";
        }

        
        },

        async makePrediction() {
            this.jsonOutput = "";
            this.error = "";
            this.modelActionResponse = "";

            if (!this.currentModel) {
                this.error = "Please load a model before making a prediction.";
                return;
            }

            if (this.csvFile) {
                try {
                const formData = new FormData();
                formData.append("file", this.csvFile);
                formData.append("name", this.currentModel);

                const res = await axios.post(`${import.meta.env.VITE_REMOTE_API}/predict-file`, formData, {
                    headers: {
                    Authorization: `Bearer ${this.$store.state.token}`,
                    "Content-Type": "multipart/form-data"
                    }
                });

                this.jsonOutput = JSON.stringify(res.data, null, 2);
                this.parsedPredictions = res.data.predictions || [];
                this.csvFile = null;
                if (this.$refs.fileInput) {
                    this.$refs.fileInput.value = null;
                }
                } catch (err) {
                this.error = err.response?.data?.detail || "Prediction from file failed.";
                }
                return;
            }

            if (this.jsonInput.trim()) {
                try {
                const parsed = JSON.parse(this.jsonInput);
                if (!Array.isArray(parsed)) throw new Error("Expected an array of samples.");

                const res = await axios.post(`${import.meta.env.VITE_REMOTE_API}/predict`, {
                    input_data: parsed,
                    return_proba: false
                }, {
                    headers: { Authorization: `Bearer ${this.$store.state.token}` }
                });

                this.jsonOutput = JSON.stringify(res.data, null, 2);
                this.parsedPredictions = res.data.predictions || [];
                } catch (err) {
                this.error = err.response?.data?.detail || "Prediction from manual input failed.";
                }
                return;
            }

            this.error = "Please upload a file or enter input samples.";
        },
        async deleteSelectedModels() {
          if (!confirm(`Are you sure you want to delete ${this.selectedModels.length} model(s)?`)) return;

          for (const name of this.selectedModels) {
            try {
              await axios.delete(`${import.meta.env.VITE_REMOTE_API}/delete-model`, {
                params: { file_name: `${name}.joblib` },  // Append extension!
                headers: { Authorization: `Bearer ${this.$store.state.token}` }
              });
            } catch {
              this.error = `Failed to delete model "${name}".`;
              return;
            }
          }

          this.modelActionResponse = `${this.selectedModels.length} model(s) deleted.`;
          this.selectedModels = [];
          this.currentModel = null;
          await this.fetchModels();
        },


      async viewDetails(modelName) {

        try {
            const res = await axios.get(`${import.meta.env.VITE_REMOTE_API}/model-metadata`, {
            params: { file_name: modelName }, 
            headers: { Authorization: `Bearer ${this.$store.state.token}` }
            });

            this.modelMetadata = res.data;
            this.modelActionResponse = `Details of "${modelName}":\n${JSON.stringify(this.modelMetadata, null, 2)}`;
            this.error = "";
        } catch (err) {
            this.error = "Failed to fetch model metadata.";
            this.modelMetadata = null;
        }
      },

      
      async renameModel(modelName) {
        const newName = prompt(`Enter a new name for "${modelName}":`);
        if (!newName || newName.trim() === "") return;

        try {
            const formData = new FormData();
            formData.append("current_name", modelName);
            formData.append("new_name", newName);

            const res = await axios.put(`${import.meta.env.VITE_REMOTE_API}/rename-model`, formData, {
            headers: {
                Authorization: `Bearer ${this.$store.state.token}`,
                "Content-Type": "multipart/form-data"
            }
            });

            this.modelActionResponse = res.data.message || `Model renamed to "${newName}"`;
            this.error = "";
            this.selectedModels = this.selectedModels.map(m => (m === modelName ? newName : m));
            this.fetchModels(); // Refresh list after rename
        } catch (err) {
            this.error = err.response?.data?.detail || "Failed to rename model.";
            this.modelActionResponse = "";
        }
        },
      handleFile(e) {
        this.csvFile = e.target.files[0];
      },
      watch: {
        inputMode(newMode) {
            if (newMode === "file") {
            this.jsonInput = "";
            } else {
            this.csvFile = null;
            if (this.$refs.fileInput) {
                this.$refs.fileInput.value = null;
            }
            }
        }
      },
      downloadCSV() {
        if (!this.parsedPredictions.length) return;

        const headers = ["Index", "Prediction"];
        const rows = this.parsedPredictions.map(row => [row.index, row.value]);

        const csvContent = [headers, ...rows]
          .map(e => e.join(","))
          .join("\n");

        const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
        const url = URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.setAttribute("href", url);
        link.setAttribute("download", this.csvFileName || "predictions.csv");
        link.style.display = "none";

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      },
    }
};
  
</script>

<style scoped>
.predict {
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

.models-section,
.prediction-section {
  margin-top: 2rem;
}

.model-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.response-box {
  border: 1px solid #ddd;
  padding: 0.75rem;
  margin-top: 0.75rem;
  background-color: #f9f9f9;
}

input[type="text"],
input[type="file"],
textarea {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.3rem;
}

button {
  margin-top: 1rem;
  padding: 0.5rem 1.2rem;
  background-color: #007acc;
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
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
.results {
  margin-top: 1.5rem;
}

.error {
  color: red;
}

.model-buttons {
  display: flex;
  flex-direction: column;
  margin-top: 0.5rem;
  gap: 0.4rem;
}

.model-list li {
  margin-bottom: 1rem;
}

.message-box {
  border: 1px solid #999;
  padding: 1rem;
  margin-top: 1rem;
  background-color: #f5f5f5;
  white-space: pre-wrap;
}

textarea {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.5rem;
}

.active {
  font-weight: bold;
  background-color: #eef;
  padding: 0.2rem;
}

.model-actions-layout {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
}

.model-list {
  flex: 1;
  list-style-type: none;
  padding: 0;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 0rem;
  min-width: 150px;
  align-self: flex-start;
}

.action-buttons button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.model-list li.active {
  font-weight: bold;
  background-color: #eef;
  padding: 0.2rem;
}

.prediction-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.prediction-table th,
.prediction-table td {
  border: 1px solid #ccc;
  padding: 0.5rem;
  text-align: left;
}

.prediction-table th {
  background-color: #f0f0f0;
}

.save-section {
  margin-top: 1.5rem;
}

.save-section input {
  width: 60%;
  padding: 0.4rem;
  margin-right: 0.5rem;
}

.model-actions-layout {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 2rem;
  min-height: 150px; 
}

.model-list.empty {
  flex: 1;
}

.model-list-box {
  flex: 1;
  border: 1px solid #ccc;
  padding: 1rem;
  border-radius: 4px;
  min-height: 150px;
  background-color: #fdfdfd;
}
</style>
  