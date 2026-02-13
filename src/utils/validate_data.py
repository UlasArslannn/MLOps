import pandas as pd
from typing import Tuple, List


def validate_telco_data(df) -> Tuple[bool, List[str]]:
    """
    Simple data validation for Telco Customer Churn dataset.
    
    NOTE: This is a simplified version that bypasses Great Expectations
    due to API compatibility issues. For production, consider updating
    to Great Expectations v1.0+ API or using a different validation framework.
    """
    print("🔍 Starting data validation...")
    
    failed_checks = []
    
    # === SCHEMA VALIDATION ===
    print("   📋 Validating schema and required columns...")
    required_columns = [
        "customerID", "gender", "Partner", "Dependents",
        "PhoneService", "InternetService", "Contract",
        "tenure", "MonthlyCharges", "TotalCharges"
    ]
    
    for col in required_columns:
        if col not in df.columns:
            failed_checks.append(f"Missing column: {col}")
    
    if failed_checks:
        print(f"❌ Schema validation FAILED: {len(failed_checks)} issues")
        return False, failed_checks
    
    # === BUSINESS LOGIC VALIDATION ===
    print("   💼 Validating business logic constraints...")
    
    # Check gender values
    if not df["gender"].isin(["Male", "Female"]).all():
        failed_checks.append("Invalid gender values")
    
    # Check Yes/No fields
    yes_no_fields = ["Partner", "Dependents", "PhoneService"]
    for field in yes_no_fields:
        if field in df.columns and not df[field].isin(["Yes", "No"]).all():
            failed_checks.append(f"Invalid {field} values")
    
    # === NUMERIC RANGE VALIDATION ===
    print("   📊 Validating numeric ranges...")
    
    # Tenure should be non-negative
    if (df["tenure"] < 0).any():
        failed_checks.append("Negative tenure values found")
    
    # Monthly charges should be positive
    if (df["MonthlyCharges"] <= 0).any():
        failed_checks.append("Non-positive MonthlyCharges found")
    
    # === MISSING VALUES CHECK ===
    print("   🔍 Checking for missing values in critical columns...")
    critical_cols = ["customerID", "tenure", "MonthlyCharges"]
    for col in critical_cols:
        if df[col].isna().any():
            failed_checks.append(f"Missing values in {col}")
    
    # === RESULTS ===
    if failed_checks:
        print(f"❌ Data validation FAILED: {len(failed_checks)} checks failed")
        print(f"   Failed checks: {failed_checks}")
        return False, failed_checks
    else:
        print(f"✅ Data validation PASSED: All checks successful")
        return True, []
