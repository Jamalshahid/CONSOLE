from ultralytics import YOLO

model = YOLO('yolov8_model.pt')  # load a custom model

# Predict with the model
results = model.predict('output.jpg', save=True)  # predict on an image
print("names: ", model.names)
print("Result:", results)
for r in results:
    print("R: ", r.boxes)
    print("R-boxes:", r.boxes.cls)
    for c in r.boxes.cls:
        print("C: ", model.names[int(c)])