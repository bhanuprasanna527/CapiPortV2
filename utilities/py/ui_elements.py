import pandas as pd

import streamlit as st
from utilities.py.data_management import CompData

class UserInputData:
    def __init__(self, company_list, opt_method, start_date, init_invest, ef_parameter = None):
        self.company_list = company_list
        self.opt_method = opt_method
        self.ef_parameter = ef_parameter
        self.start_date = start_date
        self.init_invest = init_invest


class UserInput:

    def __init__(self, company_data: CompData):
        """
        Class that renders the user selection (company, optimization technique, etc.)
        """
        self.comp_data = company_data
        self.ef_parameter_input = None
        self.company_list_input = None
        self.opt_method_input = None
        self.start_date_input = None
        self.initial_investment_input = None

    def company_selection(self):
        self.company_list_input = st.multiselect(
            "Select Multiple Companies", self.comp_data.company_names, default=None
        )

    def opt_method_selection(self):
        self.opt_method_input = st.selectbox(
            "Choose an optimization method accordingly",
            (
                "Efficient Frontier",
                "Hierarchical Risk Parity",
            ),
        )
        
        if self.opt_method_input == "Efficient Frontier":
            self.ef_parameter_input = st.selectbox(
                "Choose an optimization parameter accordingly",
                (
                    "Maximum Sharpe Ratio",
                    "Efficient Risk",
                    "Minimum Volatility",
                    "Efficient Return",
                ),
            )

    def start_date(self):
        self.start_date_input = st.date_input(
            "Start Date",
            format="YYYY-MM-DD",
            value=pd.Timestamp("1947-08-15"),
            max_value=pd.Timestamp.now(),
        )

    def initial_investment(self):
        self.innit_invest_input = st.number_input("How much would you want to invest?", value=45000)

    def get_selected_comp_ids(self):
        if self.company_list_input is not None:
            return self.comp_data.comp_name_to_id(self.company_list_input)
        print("WARINING: Selected company ids accessed, eventhough company not yet rendered in UI")
        return None

    def get_user_input_data(self) -> UserInputData:
        return UserInputData(self.company_list_input,
                             self.opt_method_input,
                             self.start_date_input,
                             self.innit_invest_input,
                             self.ef_parameter_input)
