from opensearchpy import OpenSearch, AWSV4SignerAuth, RequestsHttpConnection
import boto3
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Configure OpenSearch client
region = 'us-east-1'
service = 'es'
credentials = boto3.Session(profile_name=os.getenv('profile_name')).get_credentials()
auth = AWSV4SignerAuth(credentials, region, service)
host = "search-dkrp-llm-example-ewed7oi2fgyuhyvpvnbqdgr4iq.aos.us-east-1.on.aws"

client = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    pool_maxsize=20
)

def store_invoice_data(invoice_data):
    # Store invoice data in OpenSearch, using VIN as primary key
    vin_number = invoice_data['vin']
    index_name = "invoices"

    document = {
        "vin": invoice_data['vin'],
        "invoiceNumber": invoice_data['invoiceNumber'],
        "date": invoice_data['date'],
        "bulb_replacement_count": invoice_data['bulb'],
    }

    response = client.index(index=index_name, id=vin_number, body=document)
    st.write("Invoice Data saved",)
    return response

