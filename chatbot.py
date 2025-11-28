# Simple Rule-Based Chatbot
# Task 8: Python Developer Internship

def chatbot():
    print("🤖 Chatbot: Hello! I'm your friendly Python chatbot.")
    print("🤖 Chatbot: Type 'exit' anytime to end the chat.\n")

    while True:
        # take input
        user_input = input("You: ").lower().strip()

        # exit condition
        if user_input in ["exit", "quit", "bye"]:
            print("🤖 Chatbot: Goodbye! Have a nice day! 👋")
            break

        # greetings
        elif user_input in ["hi", "hello", "hey"]:
            print("🤖 Chatbot: Hi there! How can I help you today?")

        # asking bot name
        elif "name" in user_input:
            print("🤖 Chatbot: I'm a simple Python chatbot built with if-else rules.")

        # asking about help
        elif "help" in user_input:
            print("🤖 Chatbot: You can say 'hello', ask my 'name', or type 'exit' to leave.")

        # multiple intents handling
        elif "how are you" in user_input:
            print("🤖 Chatbot: I'm doing great, thank you! How are you?")

        elif "weather" in user_input:
            print("🤖 Chatbot: I can’t check the weather yet, but you can look outside! 🌤")

        elif "time" in user_input:
            from datetime import datetime
            now = datetime.now().strftime("%H:%M:%S")
            print(f"🤖 Chatbot: The current time is {now} ⏰")

        # default response
        else:
            print("🤖 Chatbot: Sorry, I don’t understand that yet.")

# run the chatbot
if __name__ == "__main__":
    chatbot()
