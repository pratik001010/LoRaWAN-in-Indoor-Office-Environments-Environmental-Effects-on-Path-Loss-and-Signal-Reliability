import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt
import joblib
import matplotlib.pyplot as plt

# 1. Load the dataset
file_path = r'D:\Python\Random Forest\ZENODO\3.cleaned_dataset_per_device.csv'
data = pd.read_csv(file_path)

# 2. Define features and target
features = [
    'distance', 'c_walls', 'w_walls', 'co2',
    'humidity', 'pm25', 'pressure', 'temperature',
    'frequency', 'snr'
]
target = 'exp_pl'

X = data[features]
y = data[target]

# 3. Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Define parameter grid for tuning
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7, 10],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0],
    'reg_alpha': [0, 0.1, 1.0],
    'reg_lambda': [1.0, 1.5, 2.0]
}

# 5. Set up RandomizedSearchCV
xgb_model = XGBRegressor(objective='reg:squarederror', random_state=42)

random_search = RandomizedSearchCV(
    estimator=xgb_model,
    param_distributions=param_grid,
    n_iter=20,
    scoring='neg_root_mean_squared_error',
    cv=5,
    verbose=1,
    n_jobs=-1
)

# 6. Run the tuning
random_search.fit(X_train, y_train)

# 7. Display the best parameters
print("Best Parameters Found:")
print(random_search.best_params_)

# 8. Use best model to evaluate
best_model = random_search.best_estimator_
y_pred = best_model.predict(X_test)

rmse = sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"Test RMSE: {rmse:.2f} dB")
print(f"Test R²: {r2:.2f}")

# 9. Save the tuned model
model_path = r'D:\Python\Random Forest\ZENODO\xgb_tuned_model.pkl'
joblib.dump(best_model, model_path)
print(f"Model saved to {model_path}")

# 10. Feature importance visualization
importances = best_model.feature_importances_
plt.figure(figsize=(10, 6))
plt.barh(features, importances)
plt.xlabel("Feature Importance")
plt.title("XGBoost Feature Importance")
plt.grid(True)
plt.show()

# 11. Predict on new example
def predict_exp_pl(new_input):
    loaded_model = joblib.load(model_path)
    df_in = pd.DataFrame([new_input])
    return loaded_model.predict(df_in)[0]

# Example prediction
new_data = {
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

predicted_pl = predict_exp_pl(new_data)
print(f"Predicted exp_pl: {predicted_pl:.2f} dB")
