import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from math import sqrt
import joblib
# import numpy as np
import matplotlib.pyplot as plt

# 1. Load the dataset and compute exp_pl
file_path = r'D:\Python\Random Forest\ZENODO\3.cleaned_dataset_per_device.csv'
data = pd.read_csv(file_path)

# Assuming TPTX=14 dBm, CLTX=0.14 dB, GTX=0.4 dBi, GRX=3 dBi: <From Table 6>
# data['exp_pl'] = (14 - 0.14 + 0.4 + 3) - data['rssi']

# 2. Define features (no rssi) and target
features = [
    'distance',
    'c_walls',
    'w_walls',
    'co2',
    'humidity',
    'pm25',
    'pressure',
    'temperature',
    'frequency',
    'snr'
]

target = 'exp_pl'

X = data[features]
y = data[target]

# 3. Split into train/test (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Train Random Forest on exp_pl
rf_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    min_samples_split=4,
    min_samples_leaf=2,
    max_features='sqrt',
    random_state=42,
    oob_score=True,
    bootstrap=True
)
rf_model.fit(X_train, y_train)

# 5. Predict and evaluate
y_pred = rf_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.2f} dB")
print(f"R²: {r2:.2f}")

# 6️. Save the trained model
model_path = r'D:\Python\Random Forest\ZENODO\random_forest_exppl_model.pkl'
joblib.dump(rf_model, model_path)
print(f"Model saved to {model_path}")

# 7. Importance Visualization of the required features
importances = rf_model.feature_importances_
feature_names = X.columns
plt.figure(figsize=(10, 6))
plt.barh(feature_names, importances)
plt.xlabel('Feature Importance')
plt.title('Random Forest Feature Importance')
# plt.scatter(y_test, y_pred)
# plt.xlabel('True exp_pl')
# plt.ylabel('Predicted exp_pl')
# plt.title('True vs Predicted exp_pl')
plt.grid(True)
plt.show()


# 8. Function to load & predict exp_pl on new input
def predict_exp_pl(new_input):
    loaded = joblib.load(model_path)
    df_in = pd.DataFrame([new_input])
    return loaded.predict(df_in)[0]


# 9. Example usage:
new_data = {
    'distance': 15,
    'c_walls': 2,
    'w_walls': 1,
    'co2': 550,
    'humidity': 45.0,
    'pm25': 0.5,
    'pressure': 1013.25,
    'temperature': 22.5,
    'frequency': 868.0,  # keep within 867–868 MHz
    'snr': 10.5
}

pred_exp_pl = predict_exp_pl(new_data)
print(f"Predicted exp_pl: {pred_exp_pl:.2f} dB")

