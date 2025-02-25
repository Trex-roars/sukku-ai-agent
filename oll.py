import ollama
import json

# Load processed WhatsApp chat dataset
with open("output/ollama_training.jsonl", "r", encoding="utf-8") as f:
    chat_history = [json.loads(line) for line in f]

# Prepare context by including previous chat messages
context = "\n".join([f"{msg['user']}: {msg['message']}" for msg in chat_history[-20:]])  # Last 20 messages

# Ask Dolphin a question using chat history
response = ollama.chat(model="dolphin3", messages=[{"role": "system", "content": "You are a helpful assistant."},
                                                           {"role": "user", "content": context + "\n\nUser: Merko ye Janna tha ki tu schl change kr rhi h ki ni?"}])

print("Dolphin Response:", response["message"]["content"])
