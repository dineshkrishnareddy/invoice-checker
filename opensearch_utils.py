from opensearchpy import OpenSearch, AWSV4SignerAuth, RequestsHttpConnection
import boto3
import os
import streamlit as st
from config import OPENSEARCH_HOST, OPENSEARCH_INDEX

# Configure OpenSearch client
region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region, service)

client = OpenSearch(
    hosts=[{'host': OPENSEARCH_INDEX, 'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    pool_maxsize=20
)

def store_invoice_data(invoice_data):
    # Store invoice data in OpenSearch, using VIN as primary key
    vin_number = invoice_data['vin']
    index_name = OPENSEARCH_HOST

    document = {
        "vin": invoice_data['vin'],
        "invoiceNumber": invoice_data['invoiceNumber'],
        "date": invoice_data['date'],
        "bulb_replacement_count": invoice_data['bulb'],
    }

    response = client.index(index=index_name, id=vin_number, body=document)
    st.write("Invoice Data saved",)
    return response

