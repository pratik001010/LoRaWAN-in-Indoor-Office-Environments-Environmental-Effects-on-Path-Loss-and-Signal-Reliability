import paho.mqtt.client as mqtt
import pandas as pd
import joblib
import json
import time

# MQTT Broker Configuration
MQTT_BROKER = 'eu1.cloud.thethings.network'
MQTT_PORT = 1883
MQTT_USERNAME = "pilot-test@ttn"
MQTT_PASSWORD = "NNSXS.X2UFOARVOCV2LY4ZQZU4MXJP4J6ITYVBOWWXM3Y.KJYOCGZJSOPSNVS6JFMYMTIQN4FPNOFKXHUGDOAYZECNWZ6YJNEQ"
MQTT_TOPIC = "v3/pilot-test@ttn/devices/+/up"

# Load the ML Model
MODEL_PATH = r'D:\Python\Random Forest\ZENODO\xgb_exppl_model.pkl'
xgb_model = joblib.load(MODEL_PATH)

# Callback: Handle incoming MQTT messages
def on_message(client, userdata, message):
    try:
        payload = message.payload.decode('utf-8')
        data = json.loads(payload)

        decoded = data.get("uplink_message", {}).get("decoded_payload", {})
        rx_metadata = data.get("uplink_message", {}).get("rx_metadata", [{}])[0]
        settings = data.get("uplink_message", {}).get("settings", {})
        topic = message.topic
        device_id = extract_device_id(topic)

        # todo decode data to a class
        # Extract features for ML model
        input_data = {
            'distance': 15,
            'c_walls': 2,
            'w_walls': 1,
            'co2': decoded.get('co2', 0),
            'humidity': decoded.get('humidity', 0.0),
            'pm25': decoded.get('pm25', 0.0),
            'pressure': decoded.get('pressure', 0.0),
            'temperature': decoded.get('temperature', 0.0),
            'frequency': float(settings.get('frequency', 868000000)) / 1e6,
            'snr': rx_metadata.get('snr', 0.0)
        }

        # Prepare input DataFrame
        df = pd.DataFrame([input_data])
        df.columns = [f"f{i}" for i in range(len(df.columns))]

        # Predict path loss
        pred = xgb_model.predict(df)[0]
        print(f"Predicted exp_pl for {device_id}: {pred:.2f} dB")

        # Publish result
        result_topic = f"predictions/{device_id}"
        result_payload = json.dumps({
            "device_id": device_id,
            "predicted_exp_pl": round(pred, 2)
        })
        client.publish(result_topic, result_payload)
        print(f"Published to {result_topic}: {result_payload}")

    except Exception as e:
        print("Error in on_message:", e)

# Extract Device ID from MQTT topic
def extract_device_id(topic):
    return topic.split('/')[4] if len(topic.split('/')) > 4 else "unknown_device"

# Connect to MQTT Broker
def connect_mqtt():
    while True:
        try:
            mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
            mqtt_client.subscribe(MQTT_TOPIC)
            print("Connected to MQTT broker and subscribed to topic.")
            break
        except Exception as e:
            print("Reconnecting in 5 seconds (connection failed):", e)
            time.sleep(5)

# MQTT Client Setup
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
mqtt_client.reconnect_delay_set(min_delay=1, max_delay=10)
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = lambda client, userdata, rc: connect_mqtt()
mqtt_client.on_publish = lambda client, userdata, mid: print(f"Published message ID: {mid}")

# Start connection and run loop
connect_mqtt()
mqtt_client.loop_forever()
