from pydantic import BaseModel, EmailStr, AnyUrl, Field, ValidationError
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    #Field allows us to add extra validation and metadata to model attributes
    #name: str = Field(..., min_length=2, max_length=50, description="Full name of the patient")
    name: Annotated[str, Field(..., min_length=2, max_length=50,title=" Name of the patient", description="Give name with at least 2 characters and at most 50 characters", examples=["John Doe", "Jane Smith"])]
    age: int = Field(..., gt=0, description="Age of the patient in years")
    
    #EmailStr will ensure that the value provided is a valid email address
    email : EmailStr
    
    #AnyUrl will ensure that the value provided is a valid URL
    linkedin_url: AnyUrl = None
    
    # Adding validation for weight to be greater than 0 with Field
    weight: float = Field(..., gt=0, description="Weight of the patient in kg")
    married: bool = Field(default = None ,description="Marital status of the patient")
    allergies: Annotated[Optional[List[str]], Field(default_factory=list, description="List of allergies the patient has")]
    contact_details: Dict[str, str]
    
def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print("inserted")
    
def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print("updated")
    
patient_info = {'name': "John Doe", 'email': 'abc@gmail.com' ,'age': 30, 'weight': 70.5, 'married': False, 'allergies': ['peanuts', 'penicillin'], 'contact_details': {'phone': '123-456-7890'}}
patient1 = Patient(**patient_info)
insert_patient(patient1)
update_patient(patient1)