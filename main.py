import pandas as pd

from utilities.py.styling import streamlit_style
from utilities.py.composer import Composer


streamlit_style()
# data import
company_list_df = pd.read_csv("utilities/data/Company List.csv")

composer = Composer(company_list_df)

composer.render_user_input()

ready_to_render_results = len(composer.user_input.get_selected_comp_ids()) > 1

if ready_to_render_results:
    composer.render_results()
