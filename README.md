# Rule Migration Service

This project provides a service to migrate rules from XML format to JSON format using a T5-based model.

## Features
- XML-to-JSON rule migration
- FastAPI for RESTful API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/rule-migration-service.git
cd rule-migration-service
```
2.	Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3.	Install dependencies:
pip install -r requirements.txt

Usage

Run the Service

Start the FastAPI service locally:

```bash
uvicorn app.main:app --reload
```

Access the API
	•	API documentation is available at: http://127.0.0.1:8000/docs
	•	Root endpoint to check service status: http://127.0.0.1:8000/

API Endpoints

1. Convert Rule
	•	URL: /convert_rule
	•	Method: POST
	•	Request Body:

```json
{
    "xml_rule": "<xml>your rule here</xml>"
}
```

	•	Response:
```json
{
    "json_rule": "{...}"
}
```

2. Root Endpoint
	•	URL: /
	•	Method: GET
	•	Response:

```json
{
    "message": "Rule Migration Service is running!"
}
```
License

This project is licensed under the MIT License.