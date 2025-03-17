import moondream as md
import cv2
from PIL import Image
import numpy as np

# Initialize the model
model = md.vl(model="/home/alpha/Downloads/moondream-2b-int8.mf")

# Open the video file
video_path = "/home/alpha/Downloads/alpha.mp4"
cap = cv2.VideoCapture(video_path)

# Get the frame rate (fps) to capture one frame per second
fps = int(cap.get(cv2.CAP_PROP_FPS))

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Exit when video ends

    # Process every `fps` frame (1 frame per second)
    if frame_count % fps == 0:
        # Convert OpenCV frame (BGR) to PIL image (RGB)
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Encode image
        encoded_image = model.encode_image(image)

        # Generate caption
        caption = model.caption(encoded_image)["caption"]
        print(f"Time {frame_count//fps} sec - Caption:", caption)

        # Ask question
        answer = model.query(encoded_image, "What's in this image?")["answer"]
        print(f"Time {frame_count//fps} sec - Answer:", answer)

    frame_count += 1

# Release resources
cap.release()
cv2.destroyAllWindows()

