import ollama

# Load the prompt from a file
def load_prompt(file_path="prompt.txt"):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Function to communicate with Ollama
def chat_with_ai(model="dolphin3"):
    prompt = load_prompt()

    print(f"\n🔹 Using Model: {model}")
    print("💬 Start chatting! (Type 'exit' to stop)\n")

    # Initial system message
    messages = [{"role": "system", "content": prompt}]

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("🔻 Chat ended. Have a great day!")
            break

        # Add user input to messages
        messages.append({"role": "user", "content": user_input})

        # Stream response from Ollama
        print("AI: ", end="", flush=True)  # Print AI label first

        streamed_message = ""  # To store the full response

        for part in ollama.chat(model=model, messages=messages, stream=True):
            chunk = part["message"]["content"]
            streamed_message += chunk
            print(chunk, end="", flush=True)  # Print in real-time

        print("\n")  # Newline after response

        # Add AI response to chat history
        messages.append({"role": "assistant", "content": streamed_message})

# Run the chat with a model of your choice
if __name__ == "__main__":
    chat_with_ai()
