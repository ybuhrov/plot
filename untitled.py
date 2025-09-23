! pip install streamlit
! pip install pandas
! pip install plotly

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Завантаження даних (може бути CSV або Google Sheets через gspread/pandas)
df = pd.read_csv("zp_example_movements_and_echelons.csv", parse_dates=["event_date"])

st.title("Патерни мереміщень, Запоріжжя")

# Блок вибору фільтрів
split_by = st.selectbox("Split by dimension:", ["None"] + [c for c in df.columns if c not in ["event_date","devices"]])

filters = {}
for col in [c for c in df.columns if c not in ["event_date","devices"]]:
    vals = sorted(df[col].dropna().unique())
    chosen = st.multiselect(f"Filter {col}:", vals, default=vals)
    filters[col] = chosen

# Фільтрація
df_f = df.copy()
for col, chosen in filters.items():
    df_f = df_f[df_f[col].isin(chosen)]

# Агрегація
group_cols = ["event_date"] + ([split_by] if split_by != "None" else [])
df_grouped = df_f.groupby(group_cols, as_index=False)["devices"].sum()

# Графік
fig = px.line(df_grouped, x="event_date", y="devices", color=split_by if split_by!="None" else None,
              title="Сума devices за датами")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df_grouped.head(50))
