import moondream as md
from PIL import Image
import psutil
import os
import time

# Track memory usage before loading the model
pid = os.getpid()
process = psutil.Process(pid)

start_time = time.time()
model = md.vl(model="/home/alpha/Downloads/moondream-0_5b-int8.mf")
print(f"Model loaded in {time.time() - start_time:.2f} seconds")

# Check memory after loading
print(f"RAM used after loading model: {process.memory_info().rss / (1024**2):.2f} MB")

# Load and process image
image = Image.open("/home/alpha/Downloads/now1.jpeg")
encoded_image = model.encode_image(image)

# Ask a question
start_time = time.time()
answer = model.query(encoded_image, "text in the image")["answer"]
print(f"Answer: {answer}")
print(f"Query processed in {time.time() - start_time:.2f} seconds")

# Check final RAM usage
print(f"Final RAM usage: {process.memory_info().rss / (1024**2):.2f} MB")
