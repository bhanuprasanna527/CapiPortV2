d---
title: CapiPort
emoji: 📈
sdk: streamlit
sdk_version: 1.32.0
app_file: main.py
pinned: false
license: mit
---

# <center>CapiPort V2</center>


## Overview

Welcome to our project on portfolio management for Indian equity markets! This project aims to help individuals efficiently allocate their money between different equities, optimizing returns while managing risk.

## Features

- **Dynamic Allocation:** Our technique dynamically allocates funds among various equities based on a robust methodology.
- **Risk Management:** The project incorporates risk management strategies to enhance overall portfolio stability.
- **User-Friendly Interface:** Access the tool through our user-friendly web interface [here](https://huggingface.co/spaces/bhanuprasanna527/CapiPort).

## Getting Started

Follow these steps to get started with the project:

1. Clone the repository:

   ```bash
   git clone https://github.com/bhanuprasanna527/CapiPort/

2. Install dependencies:
   ```bash
    pip install -r requirements.txt

3. Run the project:
   ```bash
    python main.py

## Technique used (Version 2) 

1) Efficient Frontier
   - Parameters used:
     
        1.1) Maximum Sharpe Ratio\
        1.2) Efficient Risk\
        1.3) Efficient Return\
        1.4) Minimum Volatility
     
2) Hierarchical Risk Parity

# Overview

1. Implementation

   In our project, we have implemented the Mean-Variance Portfolio Optimization method with 5000 iterations. The process involves:

   Input: Historical return data for each equity in the Indian market.

   Objective: Maximize expected return while minimizing portfolio variance.

   Optimization: Utilize an iterative approach, adjusting weights to find the optimal allocation.

   Output: The final set of weights that represent the optimal portfolio allocation.

#### Contributing
We welcome contributions! If you have any ideas for improvements, open an issue or submit a pull request.
License

This project is licensed under the MIT License.

## Links
1. **[Streamlit Deployment](https://capiport2.streamlit.app/)**
2. **[HuggingFace Spaces](https://huggingface.co/spaces/bhanuprasanna527/CapiPort)**
