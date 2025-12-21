# import pandas as pd
# import streamlit as st
#
# st.header('Hello World')
# st.title('Re-ex demo')
# name=st.text_input('Enter your name')
# if name:
#     st.write(f"Hello, {name}!")
# else:
#     st.write("Please enter your name above")
# print("Script Executed")
#
# st.title('Title')
# st.header('Header')
# st.subheader('Subheader')
#
# st.markdown("Markdown is [vist google](https://google.com)")
# st.text('Text')
# st.write('Text,`stwrite` *mix*,**bold**,_italic_,num:123',123)
# st.markdown('### Code Block Example')
# st.code("""
# #pyhton example
# def greet(name)
#     return f'Hello {name}!'
# print(greet('Streamlit'))
# """)
# st.markdown('#### Inline LaTex: $a^2 + b^2 = c^2$')
# st.latex(r"\int_0\infty edfdfsdgsdg\\34{rer}")
# st.success("success")
# st.warning("warning")
# st.error("error")
# st.info("info")
# st.markdown(">This is a tip")
# if st.button('Click'):
#     st.write('Clicked!')
# choice=st.radio('Which option?',[1,2,3,4,5])
# st.write("option ",choice)
# agree=st.checkbox('Do you agree?')
# if agree:
#     st.write('You agree!')
# select=st.selectbox("number",[1,2,3,4,5])
# st.write("selected",select)
# multiselect=st.multiselect("number",[1,2,3,4,5])
# st.write("multiselect",multiselect)
# data={
#     "name":['ram','raj','ravi'],
#     "age":[43,23,42],
#     "city":['city a','city b','city c']
# }
# tab=pd.DataFrame(data)
# st.write(tab)
# st.table(tab)
# st.dataframe(tab)
# data={
#     "name":['ram','raj','ravi'],
#     "age":[43,23,42],
#     "city":['city a','city b','city c']
# }
# tab=pd.DataFrame(data)
#
# etab=st.data_editor(tab,num_rows="dynamic")
# st.write(etab)
import streamlit as st
import pandas as pd

# --- Login security ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("You must login first!")
    st.stop()

if st.button("Logout"):
    st.session_state.logged_in = False
    st.switch_page("app.py")

# --------- 1. LOAD DATA ---------
@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv", parse_dates=["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# --------- 2. PAGE CONFIG ---------
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Sales Performance Dashboard")
st.markdown("Analyze sales performance by **date, region, and product**.")

# --------- 3. SIDEBAR FILTERS ---------
st.sidebar.header("Filter Data")

# Date range filter
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple):
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# Region filter
regions = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

# Product filter
products = st.sidebar.multiselect(
    "Product",
    options=sorted(df["Product"].unique()),
    default=sorted(df["Product"].unique())
)

# --------- 4. APPLY FILTERS ---------
filtered_df = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date) &
    (df["Region"].isin(regions)) &
    (df["Product"].isin(products))
]

st.write(f"Showing **{len(filtered_df)}** records after filtering.")

# --------- 5. TOP KPIs ---------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()

avg_order_value = total_sales / len(filtered_df) if len(filtered_df) > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")
col3.metric("Total Quantity Sold", f"{total_quantity:,}")
col4.metric("Avg. Order Value", f"₹{avg_order_value:,.2f}")

st.markdown("---")

# --------- 6. SALES OVER TIME (LINE CHART) ---------
st.subheader("📈 Sales Trend Over Time")

if not filtered_df.empty:
    sales_trend = (
        filtered_df.groupby("Date")["Sales"]
        .sum())
    st.line_chart(sales_trend)
else:
    st.info("No data available for the selected filters.")

# --------- 7. SALES BY PRODUCT (BAR CHART) ---------
st.subheader("🏷️ Sales by Product")

if not filtered_df.empty:
    sales_by_product = (
        filtered_df.groupby("Product")["Sales"]
        .sum())
    st.bar_chart(sales_by_product)
else:
    st.info("No data to display for products.")

# --------- 8. SALES BY REGION (BAR CHART) ---------
st.subheader("🌍 Sales by Region")

if not filtered_df.empty:
    sales_by_region = (
        filtered_df.groupby("Region")["Sales"]
        .sum()

    )
    st.bar_chart(sales_by_region)
else:
    st.info("No data to display for regions.")

# --------- 9. RAW DATA TABLE ---------
with st.expander("📄 Show Raw Data"):
    st.dataframe(filtered_df.reset_index(drop=True))
