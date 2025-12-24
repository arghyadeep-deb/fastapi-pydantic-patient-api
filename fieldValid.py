from pydantic import BaseModel, EmailStr, AnyUrl, Field, ValidationError, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    age: int
    email : EmailStr
    weight: float
    married: bool = None
    allergies: Optional[List[str]]
    contact_details: Dict[str, str]
            
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        valid_domains = ['gmail.com', 'yahoo.com', 'outlook.com']
        domain = v.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError('Email domain is not allowed')
        
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        return v.upper()
    
    @model_validator(mode='before')
    @classmethod
    def check_age_weight(cls, values):
        age = values.get('age')
        weight = values.get('weight')
        if age is not None and weight is not None:
            if age < 0 or weight < 0:
                raise ValueError('Age and Weight must be non-negative')
        return values
    
    @computed_field
    @property
    def bmi(self) -> float:
        height_m = 1.75  # assuming a fixed height for demonstration
        bmi = round(self.weight / (height_m ** 2), 2)
        return bmi
    
def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print(patient.bmi)
    print("inserted")
    
def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print(patient.bmi)
    print("updated")
    
    
patient_info = {'name': "John Doe", 'email': 'abc@gmail.com' ,'age': 30, 'weight': 70.5, 'married': False, 'allergies': ['peanuts', 'penicillin'], 'contact_details': {'phone': '123-456-7890'}}
patient1 = Patient(**patient_info)
insert_patient(patient1)
update_patient(patient1)