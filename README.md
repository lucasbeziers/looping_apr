# 💹 Simplified APR Looping Simulation

This Streamlit app allows users to simulate **looping strategies** in DeFi (Decentralized Finance) by adjusting various parameters related to borrowing, lending, and leverage. The goal is to understand how different supply/borrow APRs and leverage affect the **resulting APR** and **health ratio** of the position.

You can use the app directly here:
👉 https://loopingapr.streamlit.app/

---

## 🚀 Features

- 📊 **Real-Time APR Calculation** based on user-defined parameters.
- 🔁 **Looping Simulation** to simulate supply/borrow leveraging.
- 📈 Displays **Resulting APR** and **Health Ratio**.
- ⚠️ Shows **liquidation thresholds** to assess risk.
- 🎚️ Adjustable **leverage slider** up to the maximum allowed based on LTV.

---

## 📦 How to Use

1. Run the app using Streamlit:
   ```bash
   streamlit run app.py
   ```

2. Input the relevant asset names, prices, APRs, and leverage level.

3. Observe the calculated **Resulting APR** and **Health Ratio** to evaluate the loop strategy.

---

## ⚠️ Disclaimer

This simulation is for **educational and illustrative purposes only**. It simplifies many real-world complexities in DeFi lending protocols. Do not use it as financial advice or a precise risk assessment tool.
