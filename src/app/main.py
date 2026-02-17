from fastapi import FastAPI
from pydantic import BaseModel
import os 
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# For imorting predict method from serving, it is necessary to add the path to the sys.path

from serving.inference import predict


app = FastAPI(version="1.0.0")

@app.get("/")
def read_root():
    return {"Hello": "World"}


# Define the input schema for prediction model 
class CustomerData(BaseModel):
    gender: str
    Partner: str
    Dependents: str
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    tenure: int
    MonthlyCharges: float
    TotalCharges: float


@app.post('/predict')
def predict_customer(data:CustomerData):

    try:
        output = predict(data.dict())
        return {"prediction": output}
    except Exception as e:
        return {"error": str(e)}
