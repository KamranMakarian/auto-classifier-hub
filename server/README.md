# AutoClassifier Hub: Backend

---

### 📌 1. **Project Overview**

**AutoClassifier Hub** is a no-code backend API platform that allows users to train, manage, and use machine learning classification models through a user-friendly frontend interface.

This backend, built using **FastAPI**, handles core services including:

*  **User Authentication** via JSON Web Tokens (JWT)
*  **Model Training** using scikit-learn and Keras (Logistic Regression, Random Forest, Neural Networks)
*  **Prediction APIs** for batch and manual input
*  **Model Persistence** with PostgreSQL metadata storage and joblib/keras model files
*  **Admin Tools** to manage users and models via protected endpoints

This project enables both casual users and admins to interact with ML models without writing code.

👉 **This is a demo full-stack project** showcasing how to build a secure website for no-code training and deployment of ML models for classification.  

---

### 2. **Tech Stack**

| Layer                         | Tech Used                                                                                                      |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Framework**                 | [FastAPI](https://fastapi.tiangolo.com/) - for building RESTful APIs                                           |
| **ORM**                       | [SQLAlchemy](https://www.sqlalchemy.org/) - for database modeling                                              |
| **Database**                  | [PostgreSQL](https://www.postgresql.org/) - for user/model storage                                             |
| **Authentication**            | [JWT (JSON Web Token)](https://jwt.io/) - for secure user sessions                                             |
| **Machine Learning**          | [scikit-learn](https://scikit-learn.org/) and [Keras](https://keras.io/)                                       |
| **Environment Configuration** | [Pydantic Settings](https://pydantic-docs.helpmanual.io/usage/settings/) - for environment variable management |

---

### 3. **Installation & Setup**

To get the backend running locally:

#### Clone the Project

```bash
git clone https://github.com/KamranMakarian/auto-classifier-hub.git
cd auto-classifier-hub/server
```


#### Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

> This installs FastAPI, SQLAlchemy, scikit-learn, Keras, and other required packages.

---

### 🔐 4. **Environment Variables**

The backend reads secrets and configuration from a `.env` file using Pydantic’s `BaseSettings`.

Create a `.env` file in your `server/` directory:

```ini
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://postgres:yourpassword@localhost/ml_models
```

**Descriptions:**

| Variable       | Purpose                      |
| -------------- | ---------------------------- |
| `SECRET_KEY`   | Used for signing JWTs        |
| `DATABASE_URL` | PostgreSQL connection string |

> ⚠️ Don’t commit this file to version control — it's meant to store secrets!

---


### 5. **Database Initialization**

Before running the backend, ensure that:

* PostgreSQL is installed and running locally.
* A database named `ml_models` is created.

You can create the database using `psql`:

```bash
createdb ml_models
```

Once the database exists, initialize the required tables:

```bash
python create_db.py
```

> This uses SQLAlchemy’s `Base.metadata.create_all()` to auto-generate the `users` and `trained_models` tables based on the ORM models.

---

### 🚀 6. **Running the Server**

To start the FastAPI development server:

```bash
uvicorn main:app --reload
```

* Server runs on: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Swagger API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc Docs (alternative): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### 📋 7. **API Endpoints**

Key public and protected endpoints:

#### Auth & Users

| Method | Endpoint           | Description                   |
| ------ | ------------------ | ----------------------------- |
| POST   | `/register`        | Register a new user           |
| POST   | `/login`           | Log in and receive JWT token  |
| POST   | `/admin/register`  | Admin-only: create admin/user |
| GET    | `/admin/users`     | Admin: list all users         |
| DELETE | `/admin/user/{id}` | Admin: delete a user          |

#### Model Training & Prediction

| Method | Endpoint         | Description                |
| ------ | ---------------- | -------------------------- |
| POST   | `/fit/`          | Train a new model          |
| POST   | `/predict/`      | Predict with input samples |
| POST   | `/predict-file/` | Predict from uploaded CSV  |

#### Model Management

| Method | Endpoint              | Description                      |
| ------ | --------------------- | -------------------------------- |
| GET    | `/list-models/`       | List all models (admin sees all) |
| POST   | `/load-model/`        | Load a saved model               |
| DELETE | `/delete-model/`      | Delete specific model            |
| DELETE | `/delete-all-models/` | Delete all models (with confirm) |
| PUT    | `/rename-model/`      | Rename a model                   |
| GET    | `/model-metadata/`    | Get details about a saved model  |

> Full usage documentation available via Swagger UI at `/docs`.

---

### 🔐 8. **Authentication**

Authentication is handled via **JWT (JSON Web Tokens)**.

Upon successful login, the API returns:

```json
{
  "access_token": "<JWT_token>",
  "token_type": "bearer"
}
```

Include this token in the `Authorization` header for all protected endpoints:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...
```

> Admin-only endpoints will return `403 Forbidden` if the user's role is not `"admin"`.

---

### 📁 9. **Project Structure**

```
server/
├── config/                 # Database and app-level configuration
│   ├── db.py
│   └── settings.py
├── dependencies/           # FastAPI dependency overrides (e.g., current_user)
│   └── auth_dependencies.py
├── models/                 # SQLAlchemy database models
│   ├── base_model.py
│   ├── logistic.py
│   ├── neural_net.py
│   ├── random_forest.py
│   ├── trained_model.py
│   ├── user.py
│   └── __init__.py
├── routes/                 # API route definitions
│   ├── admin.py
│   └── auth.py
├── saved_models/           # Persisted model files (.joblib / .keras etc.)
├── schemas/                # Pydantic request/response models
│   ├── request_response.py
│   ├── token.py
│   └── user.py
├── services/               # Business logic layer (auth, training, ops)
│   ├── auth.py
│   ├── db_ops.py
│   ├── trainer.py
│   └── utils.py
├── utils/                  # Utility helpers (JWT, CSV loaders, etc.)
│   ├── data.py
│   └── jwt.py
├── venv/                   # Virtual environment (ignored in Git)
├── .env                    # Environment variables
├── create_db.py            # Script to create tables
├── main.py                 # FastAPI app entry point
└── README.md
```

---

### 10. **Troubleshooting**

**❌ Issue:** `psycopg2.OperationalError: could not connect to server`

* Ensure PostgreSQL is installed and running
* Check that `DATABASE_URL` in `.env` is correct
* Use `pgadmin` or `psql` to verify DB connectivity

**❌ Issue:** `relation "trained_models" does not exist`

* You likely forgot to run:

  ```bash
  python create_db.py
  ```

**❌ Issue:** `JWT decode error` or `Unauthorized`

* Ensure token is passed in `Authorization` header
* Check the `SECRET_KEY` consistency between `.env` and `utils/jwt.py` (or load both from `settings.py`)

---

### 🚧 11. **Future Improvements**

This backend is designed to be extendable. Here are potential upgrades and features that could enhance functionality, usability, and ML capabilities:

#### Model Evaluation Enhancements

* **Classification Report API**
  Return `precision`, `recall`, `F1-score`, and `support` alongside accuracy after training or prediction.

*  **Confusion Matrix Visualization**
  Provide an image or JSON array representing the model’s confusion matrix for interpretation.

#### Model Management

* **Model Versioning**
  Allow users to train and store multiple versions of the same model with timestamps or tags.

* **Model Export**
  Add ability to export models for offline use (e.g., download `.joblib` or `.h5` file).

---

### 📌 12. **License / Attribution**

This backend was developed as part of the **AutoClassifier Hub** project. You may adapt or reuse the code with proper attribution. For licensing beyond academic use, please contact the author.

* **GitHub**: [KamranMakarian](https://github.com/KamranMakarian) 
---







