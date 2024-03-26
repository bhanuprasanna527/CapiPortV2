import pandas as pd
import streamlit as st

from utilities.py.data_management import CompData, PortfolioOptimizer
from utilities.py.ui_elements import UserInput
from utilities.py import plots, summary_tables


class Composer:
    def __init__(self, company_df):
        """
        Class for composing the apps UI on a high level. Is meant to provide a readable overview, of what happens inside the app, without being concerned with unnecessary details.

        Uppon initializing the composer fetches the data within the apps source code (for now) and let's a dedicated class handle the raw data.
        """
        self.comp_data = CompData(company_df)

        # get all the necessary ui elements
        self.user_input = UserInput(self.comp_data)

    def render_user_input(self):
        self.user_input.company_selection()
        self.user_input.opt_method_selection()
        self.user_input.start_date()
        self.user_input.initial_investment()

    def render_results(self):
        """
        CAUTION: the composer assumes, that the user has given all the necessary data.

        NECESSARY DATA:
            - at least two companies
            - an optimization method
            - a start date
            - initial investment

        Check the conditions the necessary conditions beforehand :)
        """
        # fetch user input
        user_input_data = self.user_input.get_user_input_data()

        # optimize the chosen portfolio according to the specifications
        portfolio_opt = PortfolioOptimizer(self.comp_data,
                                           self.user_input.get_selected_comp_ids(),
                                           user_input_data.start_date)

        company_asset_weights = portfolio_opt.optimize(user_input_data.opt_method,
                                                       user_input_data.ef_parameter)

        # show first the stock data...
        st.dataframe(portfolio_opt.stock_data, use_container_width=True)

        # print disclaimer
        first_date_available = portfolio_opt.stock_data.index[0]

        st.write(
            f"Note: Due to unavailability of full data, this Analysis uses data from the date: {first_date_available}")

        # show asset weights, portfolio performance and the pie chart
        st.dataframe(company_asset_weights, use_container_width=True)

        st.dataframe(portfolio_opt.get_portfolio_performance(),
                     use_container_width=True)

        plots.pie_chart_company_asset_weights(company_asset_weights)

        # summarize the resulting data
        portfolio_returns = portfolio_opt.get_portfolio_returns()
        annual_portfolio_returns = portfolio_opt.get_annual_portfolio_returns()

        cumulative_returns = (portfolio_returns +
                              1).cumprod() * user_input_data.init_invest

        # render the tabs
        tab1, tab2, tab3 = st.tabs(
            ["Plots", "Annual Returns", "Montly Returns"])

        with tab1:
            plots.plot_annual_returns(annual_portfolio_returns)
            plots.plot_cummulative_returns(cumulative_returns)

        with tab2:
            annual_portfolio_returns = summary_tables.annual_returns_dataframe(
                annual_portfolio_returns
            )
            annual_cumulative_returns = (
                summary_tables.annual_cumulative_returns_dataframe(
                    cumulative_returns)
            )
            annual_stock_returns = summary_tables.company_wise_annual_return(
                portfolio_opt.stock_data_returns, company_asset_weights
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
                portfolio_opt.stock_data_returns, company_asset_weights
            )
            monthly_cumulative_returns = (
                summary_tables.monthly_cumulative_returns_dataframe(
                    cumulative_returns)
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
