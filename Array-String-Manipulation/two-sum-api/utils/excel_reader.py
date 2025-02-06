# ===================== EXCEL FILE READER =====================
# utils/excel_reader.py
import pandas as pd
import logging

def read_excel_file(filepath):
    try:
        df = pd.read_excel(filepath)
        return df["Numbers"].tolist()
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        raise ValueError("Invalid Excel file format")