import boto3
import json
import streamlit as st
from config import CLAUDE_BEDROCK_MODEL_ARN, AWS_REGION

bedrock_client = boto3.client('bedrock-runtime', AWS_REGION, endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com')


def bedrock_summarizer(prompt_data) -> str:
    """
    This function creates the summary of each individual chunk as well as the final summary.
    :param prompt_data: This is the prompt along with the respective chunk of text, at the end it contains all summary chunks combined.
    :return: A summary of the respective chunk of data passed in or the final summary that is a summary of all summary chunks.
    """
    # setting the key parameters to invoke Amazon Bedrock
    # body of data with parameters that is passed into the bedrock invoke model request
    # TODO: TUNE THESE PARAMETERS AS YOU SEE FIT
    prompt = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_data
                    }
                ]
            }
        ]
    }
    # formatting the prompt as a json string
    json_prompt = json.dumps(prompt)
    # invoking Claude3, passing in our prompt
    response = bedrock_client.invoke_model(body=json_prompt, modelId=CLAUDE_BEDROCK_MODEL_ARN,
                                    accept="application/json", contentType="application/json")
    # getting the response from Claude3 and parsing it to return to the end user
    response_body = json.loads(response.get('body').read())
    # the final string returned to the end user
    answer = response_body['content'][0]['text']
    # returning the final string to the end user
    return answer

def summarize_invoice(invoice_data):
    # Create a prompt with invoice details to summarize
    
    prompt_data = f"""\n\nHuman: 
    Summarize the following invoice by extracting key information such as the invoice number, date, 
    total amount due, subtotal, list of items or services provided (with descriptions, quantity and prices), 
    applicable taxes or discounts, and payment terms. Ensure to verify that the subtotal of all the items and the main total match. 
    If the subtotal of all items and total match, mention that they align. 
    If they do not match, note the discrepancy and indicate if there are any additional fees, taxes, or adjustments 
    that explain the difference as shown in the example.

    Example 1:
    Subtotal sum: $160.00
    Invoice Total: $160.00
    Summary: "The subtotal sum is $150.00 matches the final total of $160.00, after adding taxes of $15.00 and applying a discount of $5.00."
    
    Example 2:
    Subtotal sum: $200.00
    Invoice Total: $240.00
    Summary: "The subtotal sum is $200.00 does not match the final total of $240.00. The difference is $20."

    Example 3:
    Subtotal sum: $1,375.00
    Invoice Total: $1,385.00
    Summary: "The subtotal of $1,375.00 does not match the final total of $1,385.00. The difference is $10."

    Provide a concise summary with all essential details for easy reference with human readable format with proper spacing in wording.
    Please do start with the info provided and don't hallucinate.
    Summaries: {invoice_data}
            \n\nAssistant:"""
    
    return bedrock_summarizer(prompt_data)



def summarize(text) -> str:
    final_summary_prompt = f"""\n\nHuman: 
    You will be given a data from a document extract details like Invoice number, date, total amount, Vehicle VIN, bulb

    Output 1:
    {{
        "date": "2024-02-29",
        "invoiceNumber": "1234",
        "total": "$160.00",
        "vin": "1234567890",
        "bulb": 2,
    }}

    Output 2:
    {{
        "date": "2024-01-29",
        "invoice": "124",
        "total": "$10.00",
        "vin": "123467890",
        "bulb": 0,
        "bumper": 2
    }}

    Please do start with the info provided and don't hallucinate.
    Just give only one json which is appropriate as output and nothing else.
    If you are not sure about any value, just make it "unknown".
    If you are not sure about the number of bulbs, just make it 0.
    If you are not sure about the date, just make it "unknown".
    If you are not sure about the invoice number, just make it "unknown".
    If you are not sure about the total amount, just make it "unknown".
    If you are not sure about the vehicle VIN, just make it "unknown".
    If you are not sure about the bulb count, just make it 0.

    Here is the data: {text}
    data: {text}
            \n\nAssistant:"""
    # generating the final summary of all the summaries we have previously generated.
    return bedrock_summarizer(final_summary_prompt)