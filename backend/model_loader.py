import joblib

rf_model = joblib.load(
    "threat_detection_model.pkl"
)

anomaly_model = joblib.load(
    "anomaly_model.pkl"
)