import pandas as pd

from utilities.py.styling import streamlit_style
from utilities.py.composer import CapiPortApp


streamlit_style()
# data import
company_list_df = pd.read_csv("utilities/data/Company List.csv")

capi_port = CapiPortApp(company_list_df)

capi_port.render_user_input()

ready_to_render_results = len(capi_port.user_input.get_selected_comp_ids()) > 1

if ready_to_render_results:
    capi_port.render_results()
