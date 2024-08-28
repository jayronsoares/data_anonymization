import pandas as pd
import hashlib
import streamlit as st
from typing import List, Optional
from io import BytesIO
from itertools import islice

def anonymize_data(df: pd.DataFrame, columns: List[str], method: str) -> pd.DataFrame:
    """Anonymize data based on the chosen method."""
    methods = {
        'Hash': lambda x: hashlib.sha256(str(x).encode()).hexdigest() if pd.notna(x) else x,
        'Mask': lambda x: '****' if pd.notna(x) else x,
        'Generalize': lambda x: 'Generalized' if pd.notna(x) else x
    }
    
    if method not in methods:
        st.error("Unsupported anonymization method.")
        return df

    df[columns] = df[columns].applymap(methods[method])
    return df

def process_file_upload(file) -> Optional[pd.DataFrame]:
    """Process uploaded CSV or Excel files."""
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            return pd.read_excel(file)
        else:
            st.error("Unsupported file format.")
            return None
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None

def paginate_dataframe(df: pd.DataFrame, page_size: int) -> pd.DataFrame:
    """Paginate a dataframe to handle large datasets."""
    return (df.iloc[start:start + page_size] for start in range(0, df.shape[0], page_size))

def display_data_preview(df: pd.DataFrame, page_size: int = 10) -> None:
    """Display data preview with pagination."""
    page_gen = paginate_dataframe(df, page_size)
    page_number = st.number_input("Page number", min_value=1, max_value=len(page_gen), step=1)

    # Display the selected page
    st.write(next(islice(page_gen, page_number - 1, page_number), df))

def main():
    st.title("Data Anonymization Tool")

    st.markdown(
        """
        **Data anonymization** is a critical process for protecting sensitive information and ensuring compliance with regulations such as the **Health Insurance Portability and Accountability Act** and the **General Data Protection Regulation**.

        - **HIPAA**: In the United States, HIPAA requires that personal health information (PHI) is protected and anonymized to safeguard patient privacy.
        - **GDPR**: In Europe, GDPR mandates that personal data must be anonymized to prevent the identification of individuals and to comply with data protection standards.
        - **LGPD**: In Brazil, LGPD (Lei Geral de Proteção de Dados) also requires that personal data be anonymized to ensure data protection and privacy in compliance with regulations
        
        """
    )

    # File upload option
    file = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])

    if file:
        df = process_file_upload(file)

        if df is not None:
            columns_to_anonymize = st.multiselect("Columns to Anonymize", df.columns.tolist())
            method = st.selectbox("Select Anonymization Method", ["Hash", "Mask", "Generalize"])

            if st.button("Anonymize Data"):
                if columns_to_anonymize:
                    df = anonymize_data(df, columns_to_anonymize, method)
                    display_data_preview(df)  # Show a preview of the anonymized data
                    
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
                    st.warning("Please select columns to anonymize.")

if __name__ == "__main__":
    main()
