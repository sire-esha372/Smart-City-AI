from ultralytics import YOLO

# Load the trained model
model = YOLO("app/ml_models/emergency.pt")

print("✅ Model loaded successfully!")
print("Classes:", model.names)