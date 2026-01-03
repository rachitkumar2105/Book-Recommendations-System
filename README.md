# 📚 Book Recommendation System

A sophisticated content-based recommendation system capable of suggesting books based on user interests. This application features a **Premium Dark Blue UI**, **Mobile Responsiveness**, and a **Multi-View Single Page Architecture**.

## 🚀 Features

- **Premium UI/UX**: A modern "Deep Navy & White" theme with glassmorphism effects and animations.
- **Multi-View Architecture**:
    - **Home View**:Showcases top Trending Books.
    - **Recommendations View**: Dedicated search interface for personalized suggestions.
- **Interactive Discovery**: Click on any book card to instantly pivot and find similar reads.
- **Mobile Responsive**: Fully adaptive layout (Stacked Navigation, Single-Column Grid) optimized for mobile devices.
- **Fast Performance**: Backend powered by **FastAPI** for low-latency responses.

## 🛠️ Tech Stack

- **Frontend**: HTML5, Vanilla CSS3 (Custom Variables & Animations), Vanilla JavaScript
- **Backend**: FastAPI (Python)
- **Data Processing**: Pandas, NumPy, Scikit-learn (Cosine Similarity)
- **Deployment**: Render

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

3.  **Run the application:**
    ```bash
    uvicorn backend.main:app --reload
    ```

4.  Open your browser at `http://127.0.0.1:8000`.

## 🌐 Deployment

### Deploy on Render

This repository includes a `render.yaml` for automatic deployment.

1.  Create a new **Web Service** on [Render](https://render.com).
2.  Connect this repository.
3.  Set the **Build Command** to: `pip install -r requirements.txt`
4.  Set the **Start Command** to: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

## 📝 Author

Created by **Rachit Kumar Singh**.
