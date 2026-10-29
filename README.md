# Library Usage Analysis System

A beginner-friendly Python project built with Streamlit, Pandas, and Matplotlib.

## Run on a computer
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Run: `pip install -r requirements.txt`
4. Run: `streamlit run app.py`
5. Open the local address printed in the terminal.

## Deploy for free from an Android phone
1. Download and extract this ZIP file.
2. Create or sign in to a GitHub account at https://github.com/
3. Create a new public repository, for example `library-usage-analysis`.
4. Upload these four files from the extracted folder: `app.py`, `library_data.csv`, `requirements.txt`, `README.md`.
5. Visit https://share.streamlit.io/ and sign in with GitHub.
6. Choose **Create app**, select your repository and branch, enter `app.py` as the main file path, then deploy.
7. Wait for the app to build. Streamlit will provide a website link.

## CSV format
Your CSV needs these columns:
- `Date` — issue date, for example `2026-01-05`
- `User` — borrower or member name
- `Book` — book title
- `Category` — book category

The app includes sample data, so it can be opened before you upload your own CSV.
