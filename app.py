import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Library Usage Analysis System", page_icon="📚", layout="wide")

st.title("📚 Library Usage Analysis System")
st.write("Analyze library book issue records, popular books, categories, and monthly usage.")

SAMPLE = pd.DataFrame({
    "Date": ["2026-01-05", "2026-01-08", "2026-01-12", "2026-02-02", "2026-02-15",
             "2026-03-01", "2026-03-04", "2026-03-18", "2026-04-02", "2026-04-11"],
    "User": ["Asha", "Rohan", "Asha", "Neha", "Rohan", "Amit", "Neha", "Asha", "Amit", "Rohan"],
    "Book": ["Wings of Fire", "Python Basics", "Atomic Habits", "Python Basics", "Wings of Fire",
             "Data Science 101", "Atomic Habits", "Python Basics", "Wings of Fire", "Data Science 101"],
    "Category": ["Biography", "Programming", "Self-help", "Programming", "Biography",
                 "Technology", "Self-help", "Programming", "Biography", "Technology"]
})

uploaded = st.file_uploader("Upload your library CSV file (optional)", type=["csv"])
if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        st.success("CSV uploaded successfully.")
    except Exception as exc:
        st.error(f"Could not read this CSV file: {exc}")
        st.stop()
else:
    df = SAMPLE.copy()
    st.info("Showing sample data. Upload your own CSV to analyze your library records.")

# Match common column names to the names used by this app.
aliases = {
    "date": "Date", "issue date": "Date", "issuedate": "Date", "borrow date": "Date",
    "user": "User", "user name": "User", "username": "User", "member": "User",
    "member name": "User", "student": "User", "student name": "User",
    "book": "Book", "book name": "Book", "title": "Book",
    "category": "Category", "book category": "Category", "genre": "Category"
}
rename = {}
for col in df.columns:
    key = str(col).strip().lower().replace("_", " ")
    if key in aliases:
        rename[col] = aliases[key]
df = df.rename(columns=rename)

required = ["Date", "User", "Book", "Category"]
missing = [col for col in required if col not in df.columns]
if missing:
    st.error("Your CSV must contain these columns: Date, User, Book, Category.")
    st.write("Columns not found:", ", ".join(missing))
    st.write("Example CSV format:")
    st.code("Date,User,Book,Category\n2026-01-05,Asha,Wings of Fire,Biography")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
for col in ["User", "Book", "Category"]:
    df[col] = df[col].astype("string").str.strip()
df = df.dropna(subset=["Date", "User", "Book", "Category"])
df = df[(df["User"] != "") & (df["Book"] != "") & (df["Category"] != "")]
if df.empty:
    st.warning("No usable records found. Check the CSV data and date format.")
    st.stop()

st.sidebar.header("Filters")
categories = sorted(df["Category"].dropna().unique().tolist())
chosen = st.sidebar.multiselect("Book category", categories, default=categories)
start_date, end_date = df["Date"].min().date(), df["Date"].max().date()
date_range = st.sidebar.date_input("Date range", value=(start_date, end_date))
filtered = df[df["Category"].isin(chosen)].copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    filtered = filtered[(filtered["Date"] >= start) & (filtered["Date"] <= end)]

st.subheader("📊 Summary")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total issue records", len(filtered))
c2.metric("Unique books", filtered["Book"].nunique())
c3.metric("Active users", filtered["User"].nunique())
c4.metric("Categories", filtered["Category"].nunique())

if filtered.empty:
    st.warning("No records match these filters. Change the filters in the sidebar.")
else:
    left, right = st.columns(2)
    with left:
        st.subheader("Most borrowed books")
        popular = filtered["Book"].value_counts().head(10)
        fig, ax = plt.subplots()
        popular.sort_values().plot(kind="barh", ax=ax)
        ax.set_xlabel("Number of issue records")
        ax.set_ylabel("Book")
        st.pyplot(fig)
        plt.close(fig)
    with right:
        st.subheader("Usage by category")
        counts = filtered["Category"].value_counts()
        fig, ax = plt.subplots()
        counts.plot(kind="pie", autopct="%1.0f%%", ax=ax, ylabel="")
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Monthly usage trend")
    monthly = filtered.set_index("Date").resample("MS").size()
    fig, ax = plt.subplots()
    monthly.plot(marker="o", ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Issue records")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Most active users")
    st.bar_chart(filtered["User"].value_counts().head(10))

st.subheader("📄 Filtered records")
display_df = filtered.copy()
display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
st.dataframe(display_df, use_container_width=True)
csv_data = display_df.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered data as CSV", csv_data, "library_usage_filtered.csv", "text/csv")

st.caption("Tip: For your own data, use columns Date, User, Book, Category.")
