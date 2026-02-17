import requests
import json

# API endpoint
API_URL = "http://localhost:8000/predict"

# Test scenarios with expected predictions
scenarios = [
    {
        "name": "🔴 HIGH RISK CHURN #1 - New customer, expensive, no loyalty",
        "expected": "Likely to churn",
        "data": {
            "gender": "Female",
            "Partner": "No",
            "Dependents": "No",
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "Fiber optic",
            "OnlineSecurity": "No",
            "OnlineBackup": "No",
            "DeviceProtection": "No",
            "TechSupport": "No",
            "StreamingTV": "No",
            "StreamingMovies": "No",
            "Contract": "Month-to-month",  # ❌ No commitment
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check",  # ❌ Not auto-pay
            "tenure": 1,  # ❌ Brand new customer
            "MonthlyCharges": 89.95,  # ❌ Very expensive
            "TotalCharges": 89.95
        }
    },
    {
        "name": "🔴 HIGH RISK CHURN #2 - Short tenure, no services, high cost",
        "expected": "Likely to churn",
        "data": {
            "gender": "Male",
            "Partner": "No",
            "Dependents": "No",
            "PhoneService": "Yes",
            "MultipleLines": "Yes",
            "InternetService": "Fiber optic",
            "OnlineSecurity": "No",  # ❌ No security
            "OnlineBackup": "No",  # ❌ No backup
            "DeviceProtection": "No",  # ❌ No protection
            "TechSupport": "No",  # ❌ No support
            "StreamingTV": "Yes",
            "StreamingMovies": "Yes",
            "Contract": "Month-to-month",  # ❌ No commitment
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check",
            "tenure": 3,  # ❌ Very short tenure
            "MonthlyCharges": 95.50,  # ❌ Highest charges
            "TotalCharges": 286.50
        }
    },
    {
        "name": "🟢 LOW RISK - Loyal customer, long contract, many services",
        "expected": "Not likely to churn",
        "data": {
            "gender": "Female",
            "Partner": "Yes",
            "Dependents": "Yes",
            "PhoneService": "Yes",
            "MultipleLines": "Yes",
            "InternetService": "Fiber optic",
            "OnlineSecurity": "Yes",  # ✅ Has security
            "OnlineBackup": "Yes",  # ✅ Has backup
            "DeviceProtection": "Yes",  # ✅ Has protection
            "TechSupport": "Yes",  # ✅ Has support
            "StreamingTV": "Yes",
            "StreamingMovies": "Yes",
            "Contract": "Two year",  # ✅ Long commitment
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Credit card (automatic)",  # ✅ Auto-pay
            "tenure": 72,  # ✅ 6 years loyal customer
            "MonthlyCharges": 105.50,
            "TotalCharges": 7596.00
        }
    },
    {
        "name": "🟢 LOW RISK - Senior customer, DSL, one year contract",
        "expected": "Not likely to churn",
        "data": {
            "gender": "Male",
            "Partner": "Yes",
            "Dependents": "Yes",
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "DSL",  # ✅ Cheaper, stable
            "OnlineSecurity": "Yes",
            "OnlineBackup": "Yes",
            "DeviceProtection": "No",
            "TechSupport": "Yes",
            "StreamingTV": "No",
            "StreamingMovies": "No",
            "Contract": "One year",  # ✅ Some commitment
            "PaperlessBilling": "No",
            "PaymentMethod": "Bank transfer (automatic)",  # ✅ Auto-pay
            "tenure": 48,  # ✅ 4 years loyal
            "MonthlyCharges": 55.20,  # ✅ Reasonable price
            "TotalCharges": 2649.60
        }
    },
    {
        "name": "🟡 BORDERLINE - Mixed signals",
        "expected": "Could go either way",
        "data": {
            "gender": "Female",
            "Partner": "Yes",  # ✅ Has partner
            "Dependents": "No",
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "Fiber optic",
            "OnlineSecurity": "No",  # ❌ No security
            "OnlineBackup": "Yes",  # ✅ Has backup
            "DeviceProtection": "No",
            "TechSupport": "No",  # ❌ No support
            "StreamingTV": "Yes",
            "StreamingMovies": "No",
            "Contract": "One year",  # ⚠️ Medium commitment
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check",  # ❌ Not auto-pay
            "tenure": 24,  # ⚠️ Medium tenure (2 years)
            "MonthlyCharges": 70.35,
            "TotalCharges": 1688.40
        }
    }
]

print("=" * 80)
print("🧪 TESTING CHURN PREDICTION API - 5 SCENARIOS")
print("=" * 80)
print()

for i, scenario in enumerate(scenarios, 1):
    print(f"\n{'='*80}")
    print(f"Test #{i}: {scenario['name']}")
    print(f"Expected: {scenario['expected']}")
    print(f"{'='*80}")
    
    # Show key features
    data = scenario['data']
    print(f"📊 Key Features:")
    print(f"   - Contract: {data['Contract']}")
    print(f"   - Tenure: {data['tenure']} months")
    print(f"   - Monthly Charges: ${data['MonthlyCharges']}")
    print(f"   - Internet: {data['InternetService']}")
    print(f"   - Tech Support: {data['TechSupport']}")
    print(f"   - Payment: {data['PaymentMethod']}")
    
    try:
        response = requests.post(API_URL, json=data)
        
        if response.status_code == 200:
            result = response.json()
            prediction = result.get("prediction", "Unknown")
            
            # Check if prediction matches expectation
            if scenario['expected'] == "Could go either way":
                match_emoji = "🟡"
            elif prediction in scenario['expected']:
                match_emoji = "✅"
            else:
                match_emoji = "❌"
            
            print(f"\n{match_emoji} API Response: {prediction}")
            
            if "error" in result:
                print(f"   ⚠️ Error: {result['error']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Docker container not running!")
        break
    except Exception as e:
        print(f"❌ Error: {str(e)}")

print("\n" + "=" * 80)
print("✅ Testing Complete!")
print("=" * 80)
