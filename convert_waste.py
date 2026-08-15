import tensorflow as tf
import tf2onnx


MODEL_PATH = "backend/app/ml_models/best_waste_model.keras"
OUTPUT_PATH = "backend/app/ml_models/waste.onnx"


print("Loading Waste Keras model...")

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

print("Waste Keras model loaded.")

print("Model input shape:")
print(model.input_shape)

print("Model output shape:")
print(model.output_shape)


input_signature = (
    tf.TensorSpec(
        model.inputs[0].shape,
        tf.float32,
        name="images"
    ),
)


print("Converting Waste model to ONNX...")

model_proto, _ = tf2onnx.convert.from_keras(
    model,
    input_signature=input_signature,
    opset=13,
    output_path=OUTPUT_PATH
)

print("Waste ONNX model created successfully!")
print(
    f"Saved to: {OUTPUT_PATH}"
)