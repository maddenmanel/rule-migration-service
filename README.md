# Rule Migration Service

This project provides a service to migrate rules from XML format to JSON format using a T5-based model.

## Features

- XML-to-JSON rule migration
- FastAPI for RESTful API

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/rule-migration-service.git
cd rule-migration-service
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the Service

First run the trunning script trunning your model.

```bash
python app/train_model.py    
```

Second, Start the FastAPI service locally:

```bash
uvicorn app.main:app --reload
```

## Access the API

- API documentation is available at: <http://127.0.0.1:8000/docs>
- Root endpoint to check service status: <http://127.0.0.1:8000/>

## API Endpoints

Convert Rule

- URL: /convert_rule
- Method: POST
- Request Body:

```json
{
    "xml_rule": "<xml>your rule here</xml>"
}
```

- Response:

```json
{
    "json_rule": "{...}"
}
```

## License

This project is licensed under the MIT License.
