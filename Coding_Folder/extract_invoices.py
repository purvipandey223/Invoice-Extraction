import os
import fitz  # PyMuPDF
import camelot
import pandas as pd
import re

script_dir = os.path.dirname(__file__)
input_folder = os.path.join(script_dir, '..', 'Input_Folder')
output_folder = os.path.join(script_dir, '..', 'Output_Folder')
os.makedirs(output_folder, exist_ok=True)

def extract_metadata(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    patterns = {
        "Order ID": r"Order\s*ID[:\s]*([A-Z0-9-]{6,})",
        "Invoice Date": r"Invoice\s*Date[:\s]*([0-9]{2}-[0-9]{2}-[0-9]{4})",
        "Invoice Number": r"Invoice\s*Number[:\s]*([A-Z0-9\-\/]+)",
        "Seller": r"Sold\s+by[:\s]*([\w\s&.-]+)",
        "GSTIN": r"GSTIN[:\s]*([0-9A-Z]{15})"
    }

    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        extracted[key] = match.group(1).strip() if match else "Not Found"

    return extracted


def standardize_columns(df):
    rename_map = {
        "Description": "Product",
        "Qty": "Quantity",
        "Qty Gross Amount ₹": "Quantity",
        "Taxable Value ₹": "Taxable Value",
        "Total Amount": "Total",
        "HSN": "HSN/SAC",
    }
    df.columns = [rename_map.get(col.strip(), col.strip()) for col in df.columns]
    return df


def choose_best_table(tables):
    for table in tables:
        df = table.df
        first_row = df.iloc[0].str.lower().tolist()
        if any("product" in col or "description" in col for col in first_row):
            return df
    return tables[0].df  # fallback


def clean_table(df):
    # Use first row as header
    df.columns = df.iloc[0]
    df = df.drop(index=0).reset_index(drop=True)

  
    df = df.dropna(how="all", axis=1)

    
    try:
        first_col = df.columns[0]
    except IndexError:
        print("⚠️ No columns found in table.")
        return df  

    
    if first_col in df.columns:
        try:
            if pd.api.types.is_string_dtype(df[first_col]):
                df = df[df[first_col].astype(str).str.strip() != str(first_col)]
        except Exception as e:
            print(f"⚠️ Skipping row clean due to error: {e}")

    df = standardize_columns(df)
    return df




def extract_tables(pdf_path):
    try:
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
        if len(tables) == 0:
            tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream', edge_tol=500)
    except Exception as e:
        print(f"Error reading tables from {pdf_path}: {e}")
        return []
    return tables


def process_invoice(pdf_file):
    pdf_path = os.path.join(input_folder, pdf_file)
    metadata = extract_metadata(pdf_path)
    tables = extract_tables(pdf_path)

    if not tables:
        print(f"⚠️ No tables found in {pdf_file}")
        return

    raw_df = choose_best_table(tables)
    df = clean_table(raw_df)

 
    for key, val in metadata.items():
        df[key] = val
    df["Platform"] = "Amazon" if "amazon" in pdf_file.lower() else "Flipkart"

    output_filename = f"{os.path.splitext(pdf_file)[0]}_cleaned.xlsx"
    output_path = os.path.join(output_folder, output_filename)
    df.to_excel(output_path, index=False)
    print(f"✅ Saved cleaned data to {output_path}")


def run_all():
    files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    if not files:
        print("No PDF files found in Input_Folder.")
        return

    print(f"🔎 Found {len(files)} PDF(s) to process...\n")
    for f in files:
        print(f"🧾 Processing: {f}")
        process_invoice(f)
    print("\n✅ All invoices processed.")

if __name__ == "__main__":
    run_all()
