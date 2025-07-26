from agent.main import chat, rag_setup

# main
rag_setup()

user_query = input("Chat with AI: ")
chat(user_query)