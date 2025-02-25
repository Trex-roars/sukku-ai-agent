import cv2
from PIL import Image
import moondream as md

# Initialize Moondream model
model = md.vl(model="/home/alpha/Downloads/moondream-0_5b-int8.mf")

# Load the video
video_path = "/home/alpha/Downloads/test.mp4"
cap = cv2.VideoCapture(video_path)

frame_rate = 1  # Extract 1 frame per second
frame_count = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break  # Stop if the video ends

    # Process every `frame_rate` seconds
    if frame_count % int(cap.get(cv2.CAP_PROP_FPS)) == 0:
        # Convert frame (BGR to RGB for PIL)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)

        # Encode and caption
        encoded_image = model.encode_image(image)
        caption = model.caption(encoded_image)["caption"]
        print(f"Frame {frame_count}: {caption}")

    frame_count += 1

cap.release()
