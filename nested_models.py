from pydantic import BaseModel, EmailStr, AnyUrl, Field, ValidationError, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Address(BaseModel):
    street: str
    city: str
    zip_code: str
    
class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address
    
address_dict = {
    "street": "123 Main St",
    "city": "Springfield",
    "zip_code": "12345"
}
patient_dict = {
    "name": "John Doe",
    "gender": "Male",
    "age": 30,
    "address": address_dict
}

address1 = Address(**address_dict)
patient1 = Patient(**patient_dict)
print(patient1)
print(patient1.address.city)  # Accessing nested model field

#Better organization of related data using nested models
#Reusability: Address model can be reused in other models like Hospital, Clinic, etc.
#Validation: Each model can have its own validation logic
#Readability: Clear structure of complex data