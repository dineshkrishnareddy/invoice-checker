from opensearchpy import OpenSearch, AWSV4SignerAuth, RequestsHttpConnection
import boto3
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

def check_duplicates(invoice_number, vin_number):
    # Check if the invoice number already exists in OpenSearch
    existing_invoice = client.search(index=OPENSEARCH_INDEX, body={
        "query": {
            "bool": {
                "must": [
                    {"match": {"invoiceNumber": invoice_number}},
                    {"match": {"vin": vin_number}}
                ]
            }
        }
    })
    return len(existing_invoice['hits']['hits']) > 0

def check_bulb_count(invoice_data):
    response = client.search(index=OPENSEARCH_INDEX, body={
        "query": {
            "bool": {
                "must": [
                    {
                    "match": {
                        "vin": invoice_data['vin']
                    }
                    },
                    {
                    "range": {
                        "date": {
                        "gte": "now/M-1M",
                        "lte": "now/M+1M",
                        "format": "yyyy-MM-dd"
                        }
                    }
                    }
                ]
                }
            },
            "aggs": {
                "total_bulb_replacement_count": {
                "sum": {
                    "field": "bulb_replacement_count"
                }
                }
            }
            })
    bulb_count = response['aggregations']['total_bulb_replacement_count']['value'] + invoice_data['bulb']
    
    return bulb_count > 1