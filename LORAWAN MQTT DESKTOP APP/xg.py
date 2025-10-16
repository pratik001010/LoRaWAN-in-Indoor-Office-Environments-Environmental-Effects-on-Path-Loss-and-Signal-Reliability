import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from math import sqrt
import joblib
import matplotlib.pyplot as plt
import os

# === 1. Load the dataset ===
file_path = r'D:\Python\Random Forest\ZENODO\3.cleaned_dataset_per_device.csv'
data = pd.read_csv(file_path)

# === 2. Define features and target ===
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

X_original = data[features]
X_onnx = X_original.copy()
X_onnx.columns = [f"f{i}" for i in range(X_onnx.shape[1])]
y = data[target]

# === 3. Split into train/test ===
X_train_orig, X_test_orig, y_train, y_test = train_test_split(X_original, y, test_size=0.2, random_state=42)
X_train_onnx, X_test_onnx = train_test_split(X_onnx, test_size=0.2, random_state=42)

# === 4. Train XGBoost Regressor ===
xgb_model = XGBRegressor(
    n_estimators=200,
    max_depth=3,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1,
    random_state=42,
    verbosity=0
)
xgb_model.fit(X_train_onnx, y_train)

# === 5. Evaluate ===
y_pred = xgb_model.predict(X_test_onnx)
rmse = sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.2f} dB")
print(f"R²: {r2:.2f}")

# === 6. Save model as .pkl ===
model_dir = r'D:\Python\Random Forest\ZENODO'
pkl_path = os.path.join(model_dir, 'xgb_exppl_model.pkl')
joblib.dump(xgb_model, pkl_path)
print(f"Model saved to {pkl_path}")
print("Checkpoint: Finished saving .pkl, starting ONNX conversion...")

# === 7. Plot Feature Importances ===
importances = xgb_model.feature_importances_
feature_names = X_original.columns
plt.figure(figsize=(10, 6))
plt.barh(feature_names, importances)
plt.xlabel('Feature Importance')
plt.title('XGBoost Feature Importance')
plt.grid(True)
plt.tight_layout()
plt.show()
# # === 8. Convert to ONNX (Verbose debug version) ===
# try:
#     print("Starting ONNX conversion...")
#     import onnxmltools
#     from skl2onnx.common.data_types import FloatTensorType
#
#     initial_type = [('float_input', FloatTensorType([None, len(X_onnx.columns)]))]
#     print("Initial type set:", initial_type)
#
#     onnx_model = onnxmltools.convert_xgboost(xgb_model, initial_types=initial_type)
#     print("ONNX model created.")
#
#     onnx_path = pkl_path.replace('.pkl', '.onnx')
#     with open(onnx_path, 'wb') as f:
#         f.write(onnx_model.SerializeToString())
#     print(f"✅ ONNX model saved to {onnx_path}")
# except Exception as e:
#     print("❌ ONNX conversion failed:", e)
#
# # === 9. Convert ONNX to TensorFlow SavedModel ===
# try:
#     print("Starting TensorFlow conversion...")
#     import onnx
#     from onnx_tf.backend import prepare
#
#     onnx_loaded = onnx.load(onnx_path)
#     print("ONNX model loaded.")
#
#     tf_model = prepare(onnx_loaded)
#     print("TensorFlow model prepared.")
#
#     tf_model_path = pkl_path.replace('.pkl', '_tf')
#     tf_model.export_graph(tf_model_path)
#     print(f"✅ TensorFlow SavedModel exported to {tf_model_path}")
# except Exception as e:
#     print("❌ TensorFlow conversion failed:", e)
#     print("❌ TensorFlow conversion failed:", e)
#
# # === 10. Convert TensorFlow → TFLite ===
# try:
#     import tensorflow as tf
#
#     converter = tf.lite.TFLiteConverter.from_saved_model(tf_model_path)
#     tflite_model = converter.convert()
#
#     tflite_path = pkl_path.replace('.pkl', '.tflite')
#     with open(tflite_path, 'wb') as f:
#         f.write(tflite_model)
#     print(f"TFLite model saved to {tflite_path}")
# except Exception as e:
#     print("❌ TFLite conversion failed:", e)


# === 11. Local test (optional) ===
def predict_exp_pl(new_input):
    model = joblib.load(pkl_path)
    df = pd.DataFrame([new_input])
    df.columns = [f"f{i}" for i in range(len(df.columns))]
    return model.predict(df)[0]


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
new_df = pd.DataFrame([new_data])
new_df.columns = [f"f{i}" for i in range(len(new_df.columns))]
pred = xgb_model.predict(new_df)[0]
print(f"Predicted exp_pl (via ONNX-trained model): {pred:.2f} dB")

print("✅ Script finished.")
