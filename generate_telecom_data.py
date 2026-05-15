import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)
n_samples = 1000

# Generate features commonly found in telecom churn datasets (already numerically encoded)
data = {
    'tenure_months': np.random.randint(1, 73, n_samples),         # 1 to 72 months
    'monthly_charges': np.round(np.random.uniform(20.0, 120.0, n_samples), 2),
    'internet_service_fiber': np.random.randint(0, 2, n_samples), # 1 if Fiber optic, 0 otherwise
    'has_device_protection': np.random.randint(0, 2, n_samples),  # 1 if possesses, 0 otherwise
    'has_tech_support': np.random.randint(0, 2, n_samples),       # 1 if possesses, 0 otherwise
    'is_contract_one_year': np.random.randint(0, 2, n_samples), 
    'is_contract_two_year': np.random.randint(0, 2, n_samples),
    'paperless_billing': np.random.randint(0, 2, n_samples),
}

df = pd.DataFrame(data)

# Derive total charges
df['total_charges'] = df['tenure_months'] * df['monthly_charges']

# Inject some realistic logic so the machine learning model can find patterns:
# - High monthly charges increase churn risk
# - High tenure decreases churn risk
# - Having tech support or a 2-year contract decreases churn risk
churn_risk = (
    (df['monthly_charges'] / 120.0 * 2) - 
    (df['tenure_months'] / 72.0 * 2) - 
    (df['has_tech_support'] * 1.5) -
    (df['is_contract_two_year'] * 2.0) +
    np.random.normal(0, 0.5, n_samples) # add some noise
)

# Convert to 0 (No Churn) and 1 (Churn) based on a threshold
df['target'] = (churn_risk > -0.5).astype(int)

# Save to CSV
output_file = 'telecom_churn_data.csv'
df.to_csv(output_file, index=False)
print(f"Successfully generated {output_file} with {n_samples} rows.")
print(df.head())
