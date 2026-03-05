---
title: CapiPort
emoji: 📈
sdk: streamlit
sdk_version: 1.32.0
app_file: main.py
pinned: false
license: mit
---

<div align="center">

# 📈 CapiPort V2
### *Quantitative Portfolio Optimisation for Indian Equity Markets*

[![Build Status](https://github.com/bhanuprasanna527/CapiPortV2/actions/workflows/HF_sync_space.yml/badge.svg)](https://github.com/bhanuprasanna527/CapiPortV2/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/bhanuprasanna527/CapiPortV2/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-Spaces-yellow)](https://huggingface.co/spaces/bhanuprasanna527/CapiPort)

**[🚀 Live Demo — Streamlit Cloud](https://capiport2.streamlit.app/) &nbsp;|&nbsp; [🤗 HuggingFace Spaces](https://huggingface.co/spaces/bhanuprasanna527/CapiPort)**

</div>

---

## 📌 Table of Contents

1. [Overview](#-overview)
2. [Why CapiPort?](#-why-capiport)
3. [Quantitative Methodology](#-quantitative-methodology)
4. [Key Features](#-key-features)
5. [Tech Stack](#-tech-stack)
6. [Architecture](#-architecture)
7. [Getting Started](#-getting-started)
8. [Usage](#-usage)
9. [Output & Analytics](#-output--analytics)
10. [Deployment](#-deployment)
11. [Contributing](#-contributing)
12. [License](#-license)

---

## 🔭 Overview

**CapiPort V2** is an end-to-end, web-based **quantitative portfolio optimisation platform** focused on the **National Stock Exchange (NSE) of India**. Given a user-defined basket of NSE-listed equities, a historical look-back window, and an investment amount, CapiPort computes the mathematically optimal capital allocation across assets — maximising risk-adjusted returns while rigorously controlling for portfolio volatility.

The application is built on battle-tested financial theory (Modern Portfolio Theory & Graph-based Risk Parity) and delivers institutional-grade analytics through a clean, interactive Streamlit UI — accessible to anyone with a browser.

---

## 💡 Why CapiPort?

| Challenge | CapiPort's Solution |
|---|---|
| Indian retail investors lack access to quant tools | Browser-based app — no coding required |
| Manual stock selection is noisy and biased | Data-driven allocation via mathematical optimisation |
| Ignoring correlations leads to concentrated risk | Covariance-aware EF & HRP methods account for cross-asset correlation |
| No visibility into historical performance | Full annual & monthly return breakdown with interactive charts |
| Opaque black-box tools | Open-source, fully auditable Python codebase |

---

## 📐 Quantitative Methodology

CapiPort V2 implements **two complementary optimisation frameworks**, giving users control over the risk-return trade-off:

### 1. 🔷 Efficient Frontier (Modern Portfolio Theory)

Based on Harry Markowitz's seminal 1952 framework, the Efficient Frontier identifies the set of portfolios that maximise expected return for a given level of risk (variance).

$$\min_{\mathbf{w}} \; \mathbf{w}^T \Sigma \mathbf{w} \quad \text{subject to} \quad \mathbf{w}^T \boldsymbol{\mu} \geq \mu^*, \; \mathbf{w}^T \mathbf{1} = 1, \; w_i \geq 0$$

Four parametric objectives are supported:

| Parameter | Description | Best For |
|---|---|---|
| **Maximum Sharpe Ratio** | Maximises the reward-to-risk ratio: $\frac{\mu_p - r_f}{\sigma_p}$ | Growth-oriented investors |
| **Minimum Volatility** | Minimises portfolio variance regardless of return | Conservative / risk-averse investors |
| **Efficient Risk** | Maximises return subject to a target volatility constraint | Investors with a defined risk budget |
| **Efficient Return** | Minimises risk subject to a target return constraint | Investors with a return target |

> **Inputs to EF:** Mean historical returns vector **μ** and sample covariance matrix **Σ**, both estimated from adjusted closing prices sourced via Yahoo Finance.

---

### 2. 🔶 Hierarchical Risk Parity (HRP)

HRP, introduced by Marcos López de Prado (2016), overcomes a key weakness of the classical EF — sensitivity to estimation error in the covariance matrix — by using **graph theory and hierarchical clustering** instead of matrix inversion.

The algorithm proceeds in three steps:

```
1. Tree Clustering   → Build a dendrogram of assets via correlation-based linkage
2. Quasi-Diagonalisation → Reorder the covariance matrix so correlated assets sit together
3. Recursive Bisection  → Allocate capital top-down through the tree proportional to cluster-level inverse-variance
```

HRP produces **more stable, diversified portfolios** that are robust to covariance estimation noise, making it particularly suitable for volatile or illiquid segments of the NSE.

---

## ✨ Key Features

- 🏦 **1,000+ NSE-listed equities** — comprehensive universe covering large-, mid-, and small-cap stocks
- ⚙️ **Dual optimisation engines** — Efficient Frontier (4 objectives) and Hierarchical Risk Parity
- 📊 **Interactive visualisations** — asset allocation pie chart, annual bar chart, cumulative return time-series (all powered by Plotly)
- 📅 **Flexible look-back window** — set any historical start date from 1947-08-15 onward
- 💰 **Investment simulation** — enter an initial capital amount and track portfolio value evolution over time
- 📋 **Granular analytics tables** — annual returns, monthly returns, and per-stock weighted contribution breakdowns
- ⚡ **Zero-install access** — fully deployed on Streamlit Cloud and HuggingFace Spaces
- 🔓 **Open-source** — MIT licensed; inspectable and extendable

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / UI** | [Streamlit](https://streamlit.io/) |
| **Data Ingestion** | [yfinance](https://github.com/ranaroussi/yfinance) (Yahoo Finance API) |
| **Optimisation** | [PyPortfolioOpt](https://github.com/robertmartin8/PyPortfolioOpt) |
| **Visualisation** | [Plotly](https://plotly.com/python/) |
| **Data Wrangling** | [pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) |
| **Database** | [MongoDB](https://www.mongodb.com/) via [PyMongo](https://pymongo.readthedocs.io/) |
| **CI/CD** | GitHub Actions → HuggingFace Spaces sync |
| **Language** | Python 3.10+ |

---

## 🏗️ Architecture

```
CapiPortV2/
├── main.py                        # App entry point — wires together UI & logic
├── requirements.txt               # Pinned Python dependencies
│
└── utilities/
    ├── data/
    │   └── Company List.csv       # NSE universe: company names & ticker symbols
    ├── style/
    │   └── style.css              # Custom Streamlit CSS styling
    ├── Notebooks/
    │   └── Experiment.ipynb       # Research & prototyping notebook
    └── py/
        ├── composer.py            # High-level app orchestration (MVC controller)
        ├── ui_elements.py         # Streamlit widget definitions (view layer)
        ├── data_management.py     # Stock data fetching & portfolio optimisation (model)
        ├── plots.py               # Plotly chart builders
        ├── summary_tables.py      # Return aggregation & table formatting
        ├── styling.py             # Page-level Streamlit styling helpers
        └── mongodb.py             # MongoDB integration utilities
```

**Data flow:**

```
User selects stocks + params
        ↓
yfinance fetches adjusted close prices (Yahoo Finance)
        ↓
PyPortfolioOpt computes μ (mean returns) & Σ (covariance matrix)
        ↓
EF / HRP solver → optimal weight vector w*
        ↓
Portfolio returns & metrics computed → rendered via Plotly + Streamlit
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- `pip` package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/bhanuprasanna527/CapiPortV2.git
cd CapiPortV2

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Run locally

```bash
streamlit run main.py
```

The app will open at `http://localhost:8501` in your default browser.

---

## 📖 Usage

1. **Select companies** — pick two or more NSE-listed stocks from the multi-select dropdown (1,000+ available)
2. **Choose an optimisation method** — `Efficient Frontier` or `Hierarchical Risk Parity`
3. **Set an EF parameter** *(Efficient Frontier only)* — Maximum Sharpe Ratio, Minimum Volatility, Efficient Risk, or Efficient Return
4. **Pick a start date** — defines the historical window used to estimate returns and covariance
5. **Enter initial investment (₹)** — used to simulate the absolute portfolio value trajectory
6. **Click Run** — CapiPort fetches live data, optimises, and renders all results

---

## 📊 Output & Analytics

After optimisation, CapiPort presents a rich set of outputs:

| Output | Description |
|---|---|
| **Stock Price Table** | Adjusted closing prices for the selected basket over the chosen period |
| **Asset Allocation Table** | Optimal weight (%) assigned to each stock |
| **Portfolio Performance** | Expected annual return (%), annual volatility (%), Sharpe ratio |
| **Allocation Pie Chart** | Interactive donut chart of capital distribution |
| **Annual Returns Bar Chart** | Year-by-year portfolio return visualisation |
| **Cumulative Returns Chart** | Portfolio value growth over time (₹) with range slider |
| **Annual Returns Table** | Year-level return, cumulative balance, and per-stock weighted contribution |
| **Monthly Returns Table** | Month-level return, cumulative balance, and per-stock weighted contribution |

---

## 🌐 Deployment

| Platform | URL |
|---|---|
| **Streamlit Cloud** | [https://capiport2.streamlit.app/](https://capiport2.streamlit.app/) |
| **HuggingFace Spaces (V2)** | [https://huggingface.co/spaces/bhanuprasanna527/CapiPort](https://huggingface.co/spaces/bhanuprasanna527/CapiPort) |
| **Version 1 — GitHub** | [https://github.com/bhanuprasanna527/CapiPort](https://github.com/bhanuprasanna527/CapiPort) |
| **Version 1 — HuggingFace Spaces** | [https://huggingface.co/spaces/sankhyikii/CapiPort](https://huggingface.co/spaces/sankhyikii/CapiPort) |

Continuous deployment is handled via a **GitHub Actions workflow** (`.github/workflows/HF_sync_space.yml`) that automatically syncs the `main` branch to HuggingFace Spaces on every push.

---

## 🤝 Contributing

Contributions are warmly welcome! Here's how to get involved:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request — describe your changes and the problem they solve

**Ideas for contribution:**
- Add Monte Carlo simulation for forward-looking risk analysis
- Integrate Black-Litterman model for view-adjusted returns
- Add factor exposure analysis (Fama-French)
- Support BSE (Bombay Stock Exchange) tickers

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

*Built with ❤️ and rigorous quantitative finance by [bhanuprasanna527](https://github.com/bhanuprasanna527)*

⭐ **Star this repo if you find it useful!** ⭐

</div>
