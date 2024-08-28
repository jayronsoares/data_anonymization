import pandas as pd
import hashlib
import streamlit as st
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine
from typing import List
import os
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

def connect_to_database(db_type: str, username: str, password: str, host: str, port: str, dbname: str) -> Engine:
    """Establish a connection to the database."""
    if db_type == "MySQL":
        db_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}"
    elif db_type == "PostgreSQL":
        db_url = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
    elif db_type == "SQL Server":
        db_url = f"mssql+pyodbc://{username}:{password}@{host}:{port}/{dbname}?driver=ODBC+Driver+17+for+SQL+Server"
    else:
        st.error("Unsupported database type.")
        return None

    engine = create_engine(db_url)
    return engine

def get_tables(engine: Engine) -> List[str]:
    """Retrieve table names from the database."""
    inspector = inspect(engine)
    return inspector.get_table_names()

def get_columns(engine: Engine, table_name: str) -> List[str]:
    """Retrieve column names from the specified table."""
    inspector = inspect(engine)
    return [column['name'] for column in inspector.get_columns(table_name)]

def get_table_data(engine: Engine, table_name: str) -> pd.DataFrame:
    """Retrieve data from the specified table."""
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

def anonymize_data(df: pd.DataFrame, columns: List[str], method: str) -> pd.DataFrame:
    """Anonymize data based on the chosen method."""
    for column in columns:
        if column in df.columns:
            if method == 'Hash':
                df[column] = df[column].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest() if pd.notna(x) else x)
            elif method == 'Mask':
                df[column] = df[column].apply(lambda x: '****' if pd.notna(x) else x)
            elif method == 'Generalize':
                df[column] = df[column].apply(lambda x: 'Generalized' if pd.notna(x) else x)
    return df

def process_file_upload(file) -> pd.DataFrame:
    """Process uploaded CSV or Excel files."""
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    else:
        st.error("Unsupported file format.")
        return None

def main():
    st.title("Data Anonymization Tool")

    # Selection for data source type
    data_source_type = st.radio("Choose the data source type:", ('Database', 'File'))

    if data_source_type == 'Database':
        # Database credentials input
        db_type = st.selectbox("Select Database Type", ["MySQL", "PostgreSQL", "SQL Server"])
        username = st.text_input("Database Username")
        password = st.text_input("Database Password", type="password")
        host = st.text_input("Database Host")
        port = st.text_input("Database Port")
        dbname = st.text_input("Database Name")

        if db_type and username and password and host and port and dbname:
            engine = connect_to_database(db_type, username, password, host, port, dbname)

            if engine:
                # Retrieve and display table names
                tables = get_tables(engine)
                table_name = st.selectbox("Select Table", tables)
                
                if table_name:
                    # Retrieve and display column names
                    columns = get_columns(engine, table_name)
                    columns_to_anonymize = st.multiselect("Columns to Anonymize", columns)
                    
                    # Anonymization method
                    method = st.selectbox("Select Anonymization Method", ["Hash", "Mask", "Generalize"])
                    
                    if st.button("Load Data"):
                        df = get_table_data(engine, table_name)
                        df = anonymize_data(df, columns_to_anonymize, method)
                        st.write(df.head())  # Show a preview of the anonymized data

                        # Provide download buttons
                        csv_data = df.to_csv(index=False)
                        excel_buffer = BytesIO()
                        df.to_excel(excel_buffer, index=False)
                        excel_data = excel_buffer.getvalue()

                        st.download_button(
                            label="Download Anonymized Data as CSV",
                            data=csv_data,
                            file_name="anonymized_data.csv",
                            mime="text/csv"
                        )
                        st.download_button(
                            label="Download Anonymized Data as Excel",
                            data=excel_data,
                            file_name="anonymized_data.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            else:
                st.error("Failed to connect to the database.")
        else:
            st.warning("Please fill out all database connection details.")

    elif data_source_type == 'File':
        # File upload option
        file = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])

        if file is not None:
            df = process_file_upload(file)

            if df is not None:
                # Display column names and select columns for anonymization
                columns_to_anonymize = st.multiselect("Columns to Anonymize", df.columns.tolist())
                
                # Anonymization method
                method = st.selectbox("Select Anonymization Method", ["Hash", "Mask", "Generalize"])
                
                if st.button("Anonymize Data"):
                    df = anonymize_data(df, columns_to_anonymize, method)
                    st.write(df.head())  # Show a preview of the anonymized data

                    # Provide download buttons
                    csv_data = df.to_csv(index=False)
                    excel_buffer = BytesIO()
                    df.to_excel(excel_buffer, index=False)
                    excel_data = excel_buffer.getvalue()

                    st.download_button(
                        label="Download Anonymized Data as CSV",
                        data=csv_data,
                        file_name="anonymized_data.csv",
                        mime="text/csv"
                    )
                    st.download_button(
                        label="Download Anonymized Data as Excel",
                        data=excel_data,
                        file_name="anonymized_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

if __name__ == "__main__":
    main()
