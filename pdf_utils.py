import camelot
import io
import re
from datetime import datetime
import tempfile
import os
import streamlit as st
import PyPDF2
import json
from bedrock_utils import summarize


def extract_invoice_data(uploaded_pdf):
    # Extract text from the PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    summary = summarize(text)
    contents = json.loads(summary)

    return {
        "invoiceNumber": contents["invoiceNumber"],
        "vin": contents["vin"],
        "date": contents["date"],
        "bulb": contents["bulb"],
        "raw_text": text
    }
