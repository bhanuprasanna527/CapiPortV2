import yfinance as yf
import numpy as np
import pandas as pd

import streamlit as st

from utilities.py.styling import streamlit_style
from utilities.py import plots
from utilities.py import summary_tables

from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import HRPOpt, hierarchical_portfolio

import plotly.express as px
import plotly.graph_objects as go
import argparse
from MongoConnect import MongoCon,client_conn
streamlit_style()


parser = argparse.ArgumentParser(description="SECRETS")
# Add arguments
parser.add_argument('USERNAME', type=str)
parser.add_argument('PASS', type=int)
# Parse arguments
args = parser.parse_args()
# Access parsed arguments
arg1_value = args.USERNAME
arg2_value = args.PASS

client = client_conn(arg1_value,arg2_value)

company_list_df = pd.read_csv("utilities/data/Company List.csv")

company_name = company_list_df["Name"].to_list()
company_symbol = (company_list_df["Ticker"] + ".NS").to_list()

name_to_symbol_dict = dict()
symbol_to_name_dict = dict()

for CSymbol, CName in zip(company_symbol, company_name):
    name_to_symbol_dict[CName] = CSymbol

for CSymbol, CName in zip(company_symbol, company_name):
    symbol_to_name_dict[CSymbol] = CName

streamlit_company_list_input = st.multiselect(
    "Select Multiple Companies", company_name, default=None
)

optimisation_method = st.selectbox(
    "Choose an optimization method accordingly",
    (
        "Efficient Frontier",
        "Hierarchical Risk Parity",
    ),
)

parameter_for_optimisation = 0
if optimisation_method == "Efficient Frontier":
    parameter_for_optimisation = st.selectbox(
        "Choose an optimization parameter accordingly",
        (
            "Maximum Sharpe Ratio",
            "Efficient Risk",
            "Minimum Volatility",
            "Efficient Return",
        ),
    )

company_name_to_symbol = [name_to_symbol_dict[i] for i in streamlit_company_list_input]

number_of_symbols = len(company_name_to_symbol)
MongoCon(client, company_name_to_symbol, number_of_symbols)

start_date = st.date_input(
    "Start Date",
    format="YYYY-MM-DD",
    value=pd.Timestamp("1947-08-15"),
    max_value=pd.Timestamp.now(),
)

initial_investment = st.number_input("How much would you want to invest?", value=45000)

if number_of_symbols > 1:
    company_data = pd.DataFrame()

    for cname in company_name_to_symbol:
        stock_data_temp = yf.download(
            cname, start=start_date, end=pd.Timestamp.now().strftime("%Y-%m-%d")
        )["Adj Close"]
        stock_data_temp.name = cname
        company_data = pd.merge(
            company_data,
            stock_data_temp,
            how="outer",
            right_index=True,
            left_index=True,
        )

    company_data.dropna(axis=1, how="all", inplace=True)

    company_data.dropna(inplace=True)

    for i in company_data.columns:
        company_data[i] = company_data[i].abs()

    st.write(
        f"Note: Due to unavailability of full data, this Analysis uses data from the date: {company_data.index[0]}"
    )

    number_of_symbols = len(company_data.columns)

    st.dataframe(company_data, use_container_width=True)

    if number_of_symbols > 1:
        company_stock_returns_data = company_data.pct_change().dropna()

        mu = 0
        S = 0
        ef = 0
        company_asset_weights = 0

        if optimisation_method == "Efficient Frontier":
            mu = expected_returns.mean_historical_return(company_data)
            S = risk_models.sample_cov(company_data)

            ef = EfficientFrontier(mu, S)

            if parameter_for_optimisation == "Maximum Sharpe Raio":
                ef.max_sharpe()
            elif parameter_for_optimisation == "Minimum Volatility":
                ef.min_volatility()
            elif parameter_for_optimisation == "Efficient Risk":
                ef.efficient_risk(0.5)
            else:
                ef.efficient_return(0.05)

            company_asset_weights = pd.DataFrame.from_dict(
                ef.clean_weights(), orient="index"
            ).reset_index()
        elif optimisation_method == "Hierarchical Risk Parity":
            mu = expected_returns.returns_from_prices(company_data)
            S = risk_models.sample_cov(company_data)

            ef = HRPOpt(mu, S)

            company_asset_weights = ef.optimize()
            company_asset_weights = pd.DataFrame.from_dict(
                company_asset_weights, orient="index", columns=["Weight"]
            ).reset_index()

        company_asset_weights.columns = ["Ticker", "Allocation"]

        company_asset_weights_copy = company_asset_weights

        company_asset_weights["Name"] = [
            symbol_to_name_dict[i] for i in company_asset_weights["Ticker"]
        ]

        company_asset_weights = company_asset_weights[["Name", "Ticker", "Allocation"]]

        st.dataframe(company_asset_weights, use_container_width=True)

        ef.portfolio_performance()

        (
            expected_annual_return,
            annual_volatility,
            sharpe_ratio,
        ) = ef.portfolio_performance()

        st_portfolio_performance = pd.DataFrame.from_dict(
            {
                "Expected annual return": (expected_annual_return * 100).round(2),
                "Annual volatility": (annual_volatility * 100).round(2),
                "Sharpe ratio": sharpe_ratio.round(2),
            },
            orient="index",
        ).reset_index()

        st_portfolio_performance.columns = ["Metrics", "Summary"]

        if optimisation_method == "Efficient Frontier":
            st.write(
                "Optimization Method - ",
                optimisation_method,
                "---- Parameter - ",
                parameter_for_optimisation,
            )
        else:
            st.write("Optimization Method - ", optimisation_method)

        st.dataframe(st_portfolio_performance, use_container_width=True)

        plots.pie_chart_company_asset_weights(company_asset_weights)

        portfolio_returns = (
            company_stock_returns_data * list(ef.clean_weights().values())
        ).sum(axis=1)

        annual_portfolio_returns = portfolio_returns.resample("Y").apply(
            lambda x: (x + 1).prod() - 1
        )

        cumulative_returns = (portfolio_returns + 1).cumprod() * initial_investment

        tab1, tab2, tab3 = st.tabs(["Plots", "Annual Returns", "Montly Returns"])

        with tab1:
            plots.plot_annual_returns(annual_portfolio_returns)
            plots.plot_cummulative_returns(cumulative_returns)

        with tab2:
            annual_portfolio_returns = summary_tables.annual_returns_dataframe(
                annual_portfolio_returns
            )
            annual_cumulative_returns = (
                summary_tables.annual_cumulative_returns_dataframe(cumulative_returns)
            )
            annual_stock_returns = summary_tables.company_wise_annual_return(
                company_stock_returns_data, company_asset_weights
            )

            merged_annual_returns_data = pd.merge(
                annual_portfolio_returns,
                annual_cumulative_returns,
                on="Year",
                suffixes=("_portfolio", "_cumulative"),
            )

            merged_annual_returns_data = pd.merge(
                merged_annual_returns_data, annual_stock_returns, on="Year"
            )

            st.write("Annual Returns")
            st.dataframe(merged_annual_returns_data, use_container_width=True)

        with tab3:
            monthly_portfolio_return = summary_tables.monthly_returns_dataframe(
                portfolio_returns
            )
            monthly_stock_return = summary_tables.company_wise_monthly_return(
                company_stock_returns_data, company_asset_weights
            )
            monthly_cumulative_returns = (
                summary_tables.monthly_cumulative_returns_dataframe(cumulative_returns)
            )

            merged_monthly_returns_data = pd.merge(
                monthly_portfolio_return,
                monthly_cumulative_returns,
                on=["Year", "Month"],
                how="inner",
            )

            merged_monthly_returns_data = pd.merge(
                merged_monthly_returns_data,
                monthly_stock_return,
                on=["Year", "Month"],
                how="inner",
            )

            st.write("Montly Return")
            st.dataframe(merged_monthly_returns_data, use_container_width=True)
