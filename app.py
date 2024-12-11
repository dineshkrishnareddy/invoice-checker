import streamlit as st
from pdf_utils import extract_invoice_data
from opensearch_utils import store_invoice_data, check_duplicates, check_bulb_count
from bedrock_utils import summarize_invoice

def main():
    st.title("Invoice Discrepancy Checker")
    
    # File upload
    uploaded_file = st.file_uploader("Upload Invoice PDF", type="pdf")
    
    if uploaded_file is not None:
        invoice_data = extract_invoice_data(uploaded_file)
        st.write("Invoice Data Extracted")
        
        # Check for discrepancies
        vin_number = invoice_data['vin']
        invoice_number = invoice_data['invoiceNumber']
        # date = invoice_data['date'].strftime("%d/%m/%Y")
        
        # Check for duplicate invoice number
        duplicate_incoice = check_duplicates(invoice_number, vin_number)
        if duplicate_incoice:
            st.warning("Duplicate invoice found!")
        
        # Check for bulb count discrepancies
        bulb_discrepancy = check_bulb_count(invoice_data)
        if bulb_discrepancy:
            st.warning(f"More than 1 bulbs replaced in this month.")
        
        # # Store new invoice in OpenSearch
        if not duplicate_incoice and not bulb_discrepancy:
            store_invoice_data(invoice_data)
        
        # Summarize invoice using Bedrock
        summary = summarize_invoice(invoice_data["raw_text"])
        st.write("Invoice Summary:", summary)
        
if __name__ == "__main__":
    main()
