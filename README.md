# FastAPI & Pydantic Practice
This repository contains practice examples demonstrating core concepts of **FastAPI** and **Pydantic**.
It is focused on understanding API design, data validation, schema modeling, and Swagger UI usage.

## Topics Covered
- Pydantic field validation and constraints  
- Custom field and model validators  
- Nested Pydantic models  
- Serialization and deserialization (`model_dump`, JSON)  
- FastAPI CRUD operations  
- Path and query parameters  
- Computed fields  
- Swagger UI for API testing  

## Files Overview
- `fieldValid.py` – Pydantic field and model validation examples  
- `nested_models.py` – Nested Pydantic models  
- `serialization.py` – Model serialization and JSON conversion  
- `test_pydantic.py` – Testing Pydantic features  
- `main.py` – FastAPI CRUD API for patient management  
- `patients.json` – Sample data storage  


## How to Run the API
Install dependencies:
```
pip install fastapi uvicorn pydantic
```
Run the FastAPI server:
```
uvicorn main:app --reload
```
Open Swagger UI:
```
http://127.0.0.1:8000/docs
```
## Purpose
This repository is intended for **learning and practicing backend development concepts** using FastAPI and Pydantic.
