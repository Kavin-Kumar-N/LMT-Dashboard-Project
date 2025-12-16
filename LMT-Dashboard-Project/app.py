import streamlit as st
import pandas as pd
import os

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------------------------------------------------
# PAGE SETUP
# -------------------------------------------------------------------
def setup_page(page_title, page_icon, layout):
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout
    )
    st.title(page_title)


# -------------------------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------------------------
def upload_file(
    upload_dir,
    allowed_types=("csv", "xlsx"),
    header_text="📁 Upload a File",
    label_text="Upload CSV or Excel",
    show_success=True
):
    st.subheader(header_text)
    uploaded_file = st.file_uploader(label_text, type=list(allowed_types))

    if uploaded_file:
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if show_success:
            st.success(f"File '{uploaded_file.name}' uploaded and saved locally!")

        return uploaded_file.name

    return None


# -------------------------------------------------------------------
# FILE MANAGEMENT
# -------------------------------------------------------------------
def get_saved_files(upload_dir):
    files = os.listdir(upload_dir)
    if not files:
        st.warning("No files uploaded yet.")
        st.stop()
    return files


def choose_file(files, header_text="📂 Choose a Saved File"):
    st.subheader(header_text)
    return st.selectbox("Select a file to visualize", files)


def delete_file(upload_dir, selected_file):
    file_path = os.path.join(upload_dir, selected_file)

    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False

    if st.button("🗑️ Delete File"):
        st.session_state.confirm_delete = True

    if st.session_state.confirm_delete:
        st.warning(f"Are you sure you want to delete '{selected_file}'?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✔ Yes, Delete Permanently"):
                os.remove(file_path)
                st.session_state.confirm_delete = False
                st.success(f"File '{selected_file}' deleted successfully.")
                st.experimental_rerun()

        with col2:
            if st.button("✖ Cancel"):
                st.session_state.confirm_delete = False
                st.info("Delete cancelled.")


# -------------------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------------------
def load_file(upload_dir, filename):
    path = os.path.join(upload_dir, filename)
    if filename.endswith(".csv"):
        return pd.read_csv(path)
    return pd.read_excel(path)


# -------------------------------------------------------------------
# DATA DISPLAY
# -------------------------------------------------------------------
def show_raw_data(df, label="📄 Show Raw Data (Original File)"):
    with st.expander(label):
        st.dataframe(df.reset_index(drop=True), width='stretch')


def show_filtered_data(df, label="🔍 Show Filtered Data"):
    with st.expander(label):
        st.dataframe(df.reset_index(drop=True), width='stretch')


# -------------------------------------------------------------------
# FILTERS
# -------------------------------------------------------------------
def apply_filters(df):
    st.sidebar.header("Filter Data")
    filtered = df.copy()

    # Date filter
    date_cols = [col for col in df.columns if "date" in col.lower()]
    if date_cols:
        date_col = date_cols[0]
        filtered[date_col] = pd.to_datetime(filtered[date_col], errors="coerce")

        min_date = filtered[date_col].min().date()
        max_date = filtered[date_col].max().date()

        start, end = st.sidebar.date_input(
            "Select Date Range",
            (min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        filtered = filtered[
            (filtered[date_col].dt.date >= start) &
            (filtered[date_col].dt.date <= end)
        ]

    # Other filters
    for col in df.columns:
        if col in date_cols:
            continue

        if pd.api.types.is_numeric_dtype(df[col]):
            min_v, max_v = float(df[col].min()), float(df[col].max())
            sel_min, sel_max = st.sidebar.slider(
                f"Numeric filter: {col}", min_v, max_v, (min_v, max_v)
            )
            filtered = filtered[(filtered[col] >= sel_min) & (filtered[col] <= sel_max)]
        else:
            values = df[col].dropna().unique()
            selected = st.sidebar.multiselect(
                f"Categorical filter: {col}", values, default=values
            )
            filtered = filtered[filtered[col].isin(selected)]

    return filtered


# -------------------------------------------------------------------
# CHART PREPARATION
# -------------------------------------------------------------------
def prepare_chart_df(df, x_axis, y_axis):
    try:
        return df.set_index(x_axis)[y_axis]
    except Exception:
        temp = df.copy()
        temp[x_axis] = temp[x_axis].astype(str)
        return temp.set_index(x_axis)[y_axis]


# -------------------------------------------------------------------
# CHARTS
# -------------------------------------------------------------------
def chart_section(df):
    st.subheader("📊 Charts")

    numeric_cols = df.select_dtypes(include="number").columns
    all_cols = df.columns

    tab_line, tab_bar, tab_area, tab_scatter, tab_pie = st.tabs(
        ["📈 Line", "📊 Bar", "📉 Area", "⭕ Scatter", "🥧 Pie"]
    )

    with tab_line:
        x = st.selectbox("X-axis", all_cols, key="line_x")
        y = st.selectbox("Y-axis", numeric_cols, key="line_y")
        st.line_chart(prepare_chart_df(df, x, y))

    with tab_bar:
        x = st.selectbox("X-axis", all_cols, key="bar_x")
        y = st.selectbox("Y-axis", numeric_cols, key="bar_y")
        st.bar_chart(prepare_chart_df(df, x, y))

    with tab_area:
        x = st.selectbox("X-axis", all_cols, key="area_x")
        y = st.selectbox("Y-axis", numeric_cols, key="area_y")
        st.area_chart(prepare_chart_df(df, x, y))

    with tab_scatter:
        import altair as alt
        x = st.selectbox("X-axis", all_cols, key="scatter_x")
        y = st.selectbox("Y-axis", numeric_cols, key="scatter_y")
        chart = alt.Chart(df).mark_circle(size=60).encode(x=x, y=y).interactive()
        st.altair_chart(chart, width='stretch')

    with tab_pie:
        import plotly.express as px
        x = st.selectbox("Category", all_cols, key="pie_x")
        if x in numeric_cols:
            st.error("Pie chart requires a categorical column.")
        else:
            st.plotly_chart(px.pie(df, names=x), width='stretch')


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------
def main():
    setup_page(
        page_title="Dashboard Project",
        page_icon="📊",
        layout="wide"
    )

    upload_file(UPLOAD_DIR)

    files = get_saved_files(UPLOAD_DIR)
    selected_file = choose_file(files)
    delete_file(UPLOAD_DIR, selected_file)

    df = load_file(UPLOAD_DIR, selected_file)
    show_raw_data(df)

    filtered_df = apply_filters(df)
    show_filtered_data(filtered_df)

    chart_section(filtered_df)


if __name__ == "__main__":
    main()
