# 🚀 Investment Project Recommendation System

A full-stack data science graduation project that builds an intelligent recommendation system for an investment platform where:

* 🧑‍💼 Project owners showcase startup ideas
* 💰 Investors browse and invest in promising projects
* 🤖 The system recommends projects to investors using multiple recommendation approaches

---

## 📌 Project Overview

This project simulates a real-world investment platform and applies multiple recommendation system techniques to match investors with suitable projects.

The system answers:

* Which projects should be recommended to each investor?
* How can we personalize recommendations?
* What is the best recommendation technique for this platform?

---

## 🏗️ System Architecture

1. **Database Layer**

   * Stores users, projects, interactions, categories
   * Used to query training data dynamically

2. **Data Processing Layer**

   * Data cleaning
   * Feature engineering
   * Interaction matrix construction

3. **Recommendation Engine**

   * Rule-Based Model
   * Collaborative Filtering
   * Content-Based Filtering

4. **Visualization Layer**

   * Power BI dashboard for insights and KPIs

5. **Deployment Layer**

   * Model served using FastAPI
   * API endpoints for recommendation retrieval

---

## 📊 Dataset

Since no public dataset exists for this exact problem, we created a **synthetic dataset** that simulates:

* Investors
* Startup projects
* Investment history
* Project categories
* Risk levels
* Funding amount
* Interaction logs

---

## 🤖 Recommendation Models

### 1️⃣ Rule-Based Recommendation

* Recommends projects based on:

  * Investor preferred categories
  * Risk appetite
  * Budget range
* Simple, interpretable baseline model

---

### 2️⃣ Collaborative Filtering

* Based on investor-project interaction matrix
* Learns patterns between similar investors
* Techniques used:

  * User-based similarity
  * Matrix operations

Advantages:

* Personalized
* Learns hidden behavior patterns

Challenges:

* Cold start problem

---

### 3️⃣ Content-Based Filtering

* Based on project features:

  * Category
  * Funding stage
  * Risk level
  * Description embeddings
* Uses similarity measures (e.g., cosine similarity)

Advantages:

* Works for new investors
* No dependency on other users

---

## 📈 Dashboard (Power BI)

The dashboard provides:

* Investment trends
* Most funded categories
* Investor activity
* Funding distribution
* Risk analysis

Built using Microsoft Power BI.

---

## 🛠️ Technologies Used

* Python
* Pandas
* Scikit-learn
* NumPy
* FastAPI
* SQL
* Power BI
* Git & GitHub

---

## 🔌 API Example

Example endpoint:

```
GET /recommend/{investor_id}
```

Response:

```json
{
  "investor_id": 12,
  "recommended_projects": [101, 205, 333]
}
```

---

## 🧠 Key Challenges Solved

* Cold start problem
* Sparse interaction matrix
* Model evaluation for implicit feedback
* Deciding between real-time vs precomputed recommendations
* Integration between database and ML model

---

## 📏 Evaluation Metrics

* Precision@K
* Recall@K
* Cosine similarity scores
* Manual validation for business relevance

---

## 🚀 Future Improvements

* Hybrid recommendation model
* Deep learning embeddings
* Real-time retraining pipeline
* A/B testing system
* Full cloud deployment

---

## 👨‍💻 Author

**Youssef Alaraby**
Data Science & Software Engineering Student
Graduation Project – Recommendation Systems


