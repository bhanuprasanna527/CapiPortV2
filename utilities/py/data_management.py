import pandas as pd
import yfinance as yf

from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import HRPOpt, hierarchical_portfolio


class CompData:
    def __init__(self, company_data):
        """
        Class that manages company and stock data
        """
        self.df = company_data
        self.company_names = self.df["Name"].to_list()
        self.company_symbols = (self.df["Ticker"] + ".NS").to_list()

        # utilities for tranlation
        name_to_id_dict = dict()
        id_to_name_dict = dict()

        for CSymbol, CName in zip(self.company_symbols, self.company_names):
            name_to_id_dict[CName] = CSymbol

        for CSymbol, CName in zip(self.company_symbols, self.company_names):
            id_to_name_dict[CSymbol] = CName

        self.name_to_id = name_to_id_dict
        self.id_to_name = id_to_name_dict

    def fetch_stock_data(self, company_ids: list, start_date: str) -> pd.DataFrame:
        """
        Use yfinance client sdk to fetch stock data from the yahoo finance api
        """
        company_data = pd.DataFrame()

        # get the stock data for the companies
        for cname in company_ids:
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

        # cleaning the data
        company_data.dropna(axis=1, how="all", inplace=True)

        company_data.dropna(inplace=True)

        for i in company_data.columns:
            company_data[i] = company_data[i].abs()

        return company_data

    def comp_id_to_name(self, list_of_ids: list):
        return [self.id_to_name[i] for i in list_of_ids]

    def comp_name_to_id(self, list_of_names: list):
        return [self.name_to_id[i] for i in list_of_names]


class PortfolioOptimizer:

    def __init__(self, comp_data: CompData, company_ids: list, start_date: str):
        self.comp_data = comp_data
        self.stock_data = self.comp_data.fetch_stock_data(
            company_ids, start_date)
        self.stock_data_returns = self.stock_data.pct_change().dropna()

    def optimize(self, method: str, ef_parameter=None):
        company_asset_weights = 0

        # Do the portfolio optimization
        if method == "Efficient Frontier":
            mu = expected_returns.mean_historical_return(self.stock_data)
            S = risk_models.sample_cov(self.stock_data)

            self.ef = EfficientFrontier(mu, S)

            if ef_parameter == "Maximum Sharpe Raio":
                self.ef.max_sharpe()
            elif ef_parameter == "Minimum Volatility":
                self.ef.min_volatility()
            elif ef_parameter == "Efficient Risk":
                self.ef.efficient_risk(0.5)
            else:
                self.ef.efficient_return(0.05)

            company_asset_weights = pd.DataFrame.from_dict(
                self.ef.clean_weights(), orient="index"
            ).reset_index()

        elif method == "Hierarchical Risk Parity":
            mu = expected_returns.returns_from_prices(self.stock_data)
            S = risk_models.sample_cov(self.stock_data)

            self.ef = HRPOpt(mu, S)

            company_asset_weights = self.ef.optimize()
            company_asset_weights = pd.DataFrame.from_dict(
                company_asset_weights, orient="index", columns=["Weight"]
            ).reset_index()

        # cleaning the returned data from the optimization
        company_asset_weights.columns = ["Ticker", "Allocation"]

        company_asset_weights["Name"] = self.comp_data.comp_id_to_name(
            company_asset_weights["Ticker"])

        company_asset_weights = company_asset_weights[[
            "Name", "Ticker", "Allocation"]]

        return company_asset_weights

    def get_portfolio_performance(self):
        if self.ef is not None:
            (
                expected_annual_return,
                annual_volatility,
                sharpe_ratio,
            ) = self.ef.portfolio_performance()

            st_portfolio_performance = pd.DataFrame.from_dict(
                {
                    "Expected annual return": (expected_annual_return * 100).round(2),
                    "Annual volatility": (annual_volatility * 100).round(2),
                    "Sharpe ratio": sharpe_ratio.round(2),
                },
                orient="index",
            ).reset_index()

            st_portfolio_performance.columns = ["Metrics", "Summary"]

            return st_portfolio_performance
        else:
            return None

    def get_portfolio_returns(self):
        return (
            self.stock_data_returns * list(self.ef.clean_weights().values())
        ).sum(axis=1)

    def get_annual_portfolio_returns(self):
        return self.get_portfolio_returns().resample("Y").apply(lambda x: (x + 1).prod() - 1)
