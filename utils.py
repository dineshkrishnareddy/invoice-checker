from opensearch_utils import client
import streamlit as st
from config import OPENSEARCH_INDEX

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
