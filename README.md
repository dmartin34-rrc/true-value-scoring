# 🏀 True Value Scoring Index

A Streamlit-powered data storytelling dashboard that re-evaluates the modern era's highest-scoring NBA games. 

Rather than looking purely at total volume, this tool breaks down scoring by **Game Margin** and **Scoring Rate (PPM)** to separate high-leverage, clutch performances from late-game "stat-padding."

🔗 **[View the Live Dashboard Here](https://true-value-scoring.streamlit.app/)**

## 📊 The Breakdown
Total points don't always tell the whole story. By categorizing points based on game state necessity (Trailing, Clutch, Comfortable, or Garbage Time), this index reveals exactly how many points were scored in crucial, close-game situations versus low-pressure scenarios.

## 🛠️ Tech Stack
* **Frontend/Framework:** Streamlit
* **Data Manipulation:** Pandas (utilizing `itertuples` and `zip` iterations)
* **Data Visualization:** Plotly Express (Custom stacked bar charts, dynamic hover states, and custom HTML label injection)

## 🚀 How to Run Locally

1. **Clone the repository:**

   ```bash
   git clone https://github.com/dmartin34-rrc/true-value-scoring.git
   cd true-value-scoring
   ```

2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```
