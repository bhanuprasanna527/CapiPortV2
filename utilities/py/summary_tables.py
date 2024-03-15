import streamlit as st
import pandas as pd
import numpy as np


def annual_returns_dataframe(annual_portfolio_returns):

    annual_portfolio_returns = annual_portfolio_returns * 100

    annual_portfolio_returns = annual_portfolio_returns.to_frame().reset_index()

    annual_portfolio_returns.columns = ["Year", "Return"]

    annual_portfolio_returns["Year"] = annual_portfolio_returns.Year.dt.year.astype(str)

    return annual_portfolio_returns


def annual_cumulative_returns_dataframe(cumulative_returns):

    cumulative_returns = cumulative_returns.to_frame().reset_index()

    cumulative_returns.columns = ["Year", "Balance"]

    cumulative_returns["Year"] = cumulative_returns["Year"].dt.year.astype(str)

    cumulative_returns = (
        cumulative_returns.groupby("Year").tail(1).reset_index().drop("index", axis=1)
    )

    return cumulative_returns


def company_wise_annual_return(company_stock_returns_data, company_asset_weights):
    # Create an empty DataFrame to store annual returns for each stock
    annual_stock_returns = pd.DataFrame(
        index=company_stock_returns_data.index.year.unique(),
        columns=company_asset_weights["Ticker"],
    )

    # Iterate over each year
    for year in annual_stock_returns.index:
        # Filter returns data for the current year
        year_returns = company_stock_returns_data.loc[
            company_stock_returns_data.index.year == year
        ]
        # Iterate over each stock
        for ticker, weight in zip(
            company_asset_weights["Ticker"], company_asset_weights["Allocation"]
        ):
            # Calculate the weighted sum of returns for the current stock in the current year
            weighted_sum_returns = (year_returns[ticker] * weight).sum() * 100
            # Store the weighted average return for the current stock in the current year
            annual_stock_returns.loc[year, ticker] = weighted_sum_returns

    # Display annual returns for each stock
    annual_stock_returns.reset_index(inplace=True)
    annual_stock_returns["Date"] = annual_stock_returns["Date"].astype(str)
    annual_stock_returns.rename(columns={"Date": "Year"}, inplace=True)

    return annual_stock_returns


def company_wise_monthly_return(company_stock_returns_data, company_asset_weights):
    # Resample daily returns to monthly returns for each stock
    monthly_stock_returns = company_stock_returns_data.resample("M").mean()

    # Iterate over each stock
    for ticker, weight in zip(
        company_asset_weights["Ticker"], company_asset_weights["Allocation"]
    ):
        # Calculate the weighted monthly returns for the current stock
        weighted_monthly_returns = monthly_stock_returns[ticker] * weight
        # Fill missing values with 0
        weighted_monthly_returns.fillna(0, inplace=True)
        # Store the weighted monthly returns in the DataFrame
        monthly_stock_returns[ticker] = weighted_monthly_returns

    # Reset the index and add new columns for year and month
    monthly_stock_returns.reset_index(inplace=True)
    monthly_stock_returns["Year"] = monthly_stock_returns["Date"].dt.year.astype(str)
    monthly_stock_returns["Month"] = monthly_stock_returns["Date"].dt.month.astype(str)

    # Rearrange the columns
    columns_order = ["Year", "Month"] + [
        col for col in monthly_stock_returns.columns if col not in ["Year", "Month"]
    ]
    monthly_stock_returns = monthly_stock_returns[columns_order]

    # Drop the original date index column
    monthly_stock_returns.drop(columns=["Date"], inplace=True)

    # Display monthly returns for each stock
    # st.write("Monthly Returns for Individual Stocks:")
    # st.dataframe(monthly_stock_returns, use_container_width=True)

    return monthly_stock_returns


def monthly_returns_dataframe(portfolio_returns):
    monthly_portfolio_returns = (
        (portfolio_returns.resample("M").mean() * 100).to_frame().reset_index()
    )

    monthly_portfolio_returns.columns = ["Date", "Return"]

    monthly_portfolio_returns["Year"] = monthly_portfolio_returns.Date.dt.year.astype(
        str
    )
    monthly_portfolio_returns["Month"] = monthly_portfolio_returns.Date.dt.month.astype(
        str
    )

    monthly_portfolio_returns.drop(columns=["Date"], inplace=True)

    monthly_portfolio_returns = monthly_portfolio_returns[["Year", "Month", "Return"]]

    return monthly_portfolio_returns


def monthly_cumulative_returns_dataframe(cumulative_returns):

    monthly_cumulative_returns = (
        cumulative_returns.resample("M").last().to_frame().reset_index()
    )

    monthly_cumulative_returns.columns = ["Date", "Balance"]

    monthly_cumulative_returns["Year"] = monthly_cumulative_returns.Date.dt.year.astype(
        str
    )
    monthly_cumulative_returns["Month"] = (
        monthly_cumulative_returns.Date.dt.month.astype(str)
    )

    monthly_cumulative_returns.drop(columns=["Date"], inplace=True)

    monthly_cumulative_returns = monthly_cumulative_returns[
        ["Year", "Month", "Balance"]
    ]

    return monthly_cumulative_returns
