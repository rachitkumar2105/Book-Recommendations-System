# 📚 Book Recommendation System

A sophisticated content-based recommendation system capable of suggesting books based on user interests. This application features a **Premium Dark UI**, **Mobile Responsiveness**, and **Interactive Recommendations**.

## 🚀 Features

- **Premium UI/UX**: A modern, "Slate & Indigo" dark theme with glassmorphism effects and Inter typography.
- **Interactive Discovery**: Click on any book card to instantly find similar reads.
- **Mobile Responsive**: Fully adaptive grid layout that looks great on Desktops, Tablets, and Mobile phones.
- **Hybrid Recommendation Engine**: (Mention if it uses hybrid, otherwise specify Content-Based using Cosine Similarity).

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend/Logic**: Python (Pandas, NumPy, Scikit-learn)
- **Deployment**: Render / Streamlit Cloud

## 💻 Running Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rachitkumar2105/Book-Recommendations-System.git
    cd Book-Recommendations-System
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

4.  Open your browser at `http://localhost:8501`.

## 🌐 Deployment

### Deploy on Render

This repository includes a `render.yaml` for automatic deployment.

1.  Create a new **Web Service** on [Render](https://render.com).
2.  Connect this repository.
3.  Render will automatically use the configuration to build and start the app.

> **Note**: The `artifacts/cosine_sim.npy` file is efficiently managed using **Git LFS** due to its size (>100MB).

## 📝 Author

Created by **Rachit Kumar Singh**.
