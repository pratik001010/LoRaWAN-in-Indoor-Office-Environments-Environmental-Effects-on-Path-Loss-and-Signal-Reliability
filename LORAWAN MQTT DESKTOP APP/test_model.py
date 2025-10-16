import pandas as pd
import joblib
import os

# === 1. Load the trained model ===
model_path = r'D:\Python\Random Forest\ZENODO\xgb_exppl_model.pkl'
model = joblib.load(model_path)

# === 2. Define new input (same order of features as used in training) ===
test_data = {
    'distance': 15,
    'c_walls': 2,
    'w_walls': 1,
    'co2': 550,
    'humidity': 45.0,
    'pm25': 0.5,
    'pressure': 1013.25,
    'temperature': 22.5,
    'frequency': 868.0,
    'snr': 10.5
}

# === 3. Prepare DataFrame and rename columns to match training format ===
new_df = pd.DataFrame([test_data])
new_df.columns = [f"f{i}" for i in range(len(new_df.columns))]  # rename to f0, f1, ...

# === 4. Predict ===
prediction = model.predict(new_df)[0]
print(f" Predicted exp_pl: {prediction:.2f} dB")
