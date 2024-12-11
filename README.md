# invoice-checker

### Prerequisites
- pip install -r requirements.txt
- AWS account setup
    1) Create Opensearch domain in your AWS account and get the domain URL
    2) Configure aws credentials locally with `aws configure` with 410627604197 account credentials

### Exports to terminal
```
export profile_name=<profile-name>
export opensearch_host=<opensearch_domain> // without http://
export region=<region>
```

### Run
streamlit run app.py

