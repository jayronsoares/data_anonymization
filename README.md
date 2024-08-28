# Data Anonymization Tool

## Overview

A web app built with Streamlit to anonymize data from databases or uploaded files. It supports MySQL, PostgreSQL, SQL Server, CSV, and Excel formats. 

## Features

- **Connect to Databases**: MySQL, PostgreSQL, SQL Server.
- **Upload Files**: CSV and Excel.
- **Anonymization Methods**: Hash, Mask, Generalize.
- **Download Options**: CSV and Excel.

## Installation

1. **Install Dependencies**:
    ```bash
    pip install pandas sqlalchemy streamlit pymysql psycopg2-binary pyodbc openpyxl
    ```

2. **Set Up Environment Variables**:
    Create a `.env` file with:
    ```text
    DB_TYPE=MySQL
    DB_USERNAME=your_username
    DB_PASSWORD=your_password
    DB_HOST=your_host
    DB_PORT=your_port
    DB_NAME=your_database
    ```

## Usage

1. **Run the App**:
    ```bash
    streamlit run app.py
    ```

2. **Use the Tool**:
    - **Database**: Select database type, enter credentials, choose a table, select columns, and anonymize.
    - **File**: Upload a CSV or Excel file, choose columns to anonymize, and process the file.

3. **Download Data**:
    - After anonymizing, use the download buttons to save the data as CSV or Excel.

## Troubleshooting

- Check environment variables and library installations.
- Ensure correct database credentials and file formats.

## License

MIT License.

---

This version is concise and focuses on the essential information users need to get started quickly.
