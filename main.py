from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field, computed_field
from typing import Annotated, Literal, Optional
import json
app = FastAPI()

# Defining Patient model with Pydantic 
class Patient(BaseModel):
    id: Annotated[str, Field(...,description="Unique identifier for the patient", example="P12345")]
    name: Annotated[str, Field(..., description="Full name of the patient", example="John Doe")]
    city: Annotated[str, Field(..., description="City of residence", example="Springfield")]
    age: Annotated[int, Field(..., ge=0, le=120, description="Age of the patient in years", example=30)]
    gender: Annotated[Literal['Male', 'Female', 'Other'], Field(..., description="Gender of the patient", example="Male")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in centimeters", example=175.5)]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kilograms", example=70.5)]
   
    @computed_field
    @property
    def bmi(self) -> float:
        height_m = self.height / 100  # converting cm to meters
        bmi = round(self.weight / (height_m ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"
        
        
class PatientUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Full name of the patient", example="John Doe")
    city: Optional[str] = Field(None, description="City of residence", example="Springfield")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age of the patient in years", example=30)
    gender: Optional[Literal['Male', 'Female', 'Other']] = Field(None, description="Gender of the patient", example="Male")
    height: Optional[float] = Field(None, gt=0, description="Height of the patient in centimeters", example=175.5)
    weight: Optional[float] = Field(None, gt=0, description="Weight of the patient in kilograms", example=70.5)
                               
def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data, f, indent=4)
        
        
@app.get("/")
def hello():
    return {"message": "Patient Management System API "}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage patient records, appointments, and medical history."}

#endpoint to view patient data
@app.get("/view")
def view():
    data = load_data()
    return data

#endpoint to get patient by ID
#Path parameter example
@app.get("/patients/{patient_id}")
def get_patient(patient_id: str=Path(..., description="The ID of the patient to retrieve", example="P12345")):
    data = load_data()
    if patient_id in data:
        return data [patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

#endpoint to sort patients by height, weight or BMI
#Query parameter example
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Field to sort patients by height, weight or bmi"), order: str = Query("asc", description="Sort order: asc or desc")):
    valid_sort_fields = {"height", "weight", "bmi"}
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Must be one of {valid_sort_fields}")
    if order not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail="Invalid order. Must be 'asc' or 'desc'")
    data = load_data()
    sorted_ordeer = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse= sorted_ordeer)
    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    #load existing data
    data = load_data()
    #check if patient with same ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    #add new patient
    data[patient.id] = patient.model_dump(exclude=['id'])
    #save updated data back to file
    save_data(data)
    
    return JSONResponse(status_code=201, content={"message": "Patient created successfully", "patient_id": patient.id})

@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient_data = data[patient_id]
    updated_data = patient_update.model_dump(exclude_unset=True)
    
    for key, value in updated_data.items():
        existing_patient_data[key] = value
    #existing_patient_data update to pydantic object to recalculate computed fields   
    existing_patient_data['id'] = patient_id  # Ensure ID remains unchanged
    updated_patient = Patient(**existing_patient_data)
    #pydantic object to dict excluding id
    existing_patient_data = updated_patient.model_dump(exclude=['id'])
    #add back to data
    data[patient_id] = existing_patient_data
    
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    #load existing data
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    #delete patient
    del data[patient_id]
    #save updated data back to file
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})