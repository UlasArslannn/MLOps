import requests
import json

# Sample customer data - high churn risk profile
data = {
    "gender": "Male",
    "Partner": "Yes",
    "Dependents": "No",
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "tenure": 12,
    "MonthlyCharges": 70.5,
    "TotalCharges": 846.0
}

print("🔍 Testing API with customer data...")
print(f"📊 Customer Profile: {data['Contract']}, Tenure: {data['tenure']} months, Monthly: ${data['MonthlyCharges']}")
print()

try:
    response = requests.post("http://localhost:8000/predict", json=data)
    
    print(f"✅ Status Code: {response.status_code}")
    print(f"📦 Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        result = response.json()
        if "prediction" in result:
            print(f"\n🎯 Prediction: {result['prediction']}")
        elif "error" in result:
            print(f"\n❌ Error: {result['error']}")
    else:
        print(f"\n⚠️ Unexpected status code: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ Connection Error: Make sure Docker container is running!")
    print("   Run: docker ps")
except Exception as e:
    print(f"❌ Error: {str(e)}")
