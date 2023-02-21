import xmlrpc.client
from datetime import datetime

proxy = xmlrpc.client.ServerProxy("http://localhost:8000")

user_input = ""
while user_input != "quit":

    print("1. Post a new note\n")
    print("2. Get notes by topic\n")

    user_input = input("Enter a value (type 'quit' to exit): ")
    print(f"You entered: {user_input}")

    try:
        if user_input == "1":
            # Get user input for the new note
            topic_name = input("Enter the name of the topic: ")
            note_name = input("Enter the name of the note: ")
            note_text = input("Enter the text of the note: ")
            timestamp = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
            proxy.save_notes(topic_name, note_name, note_text, timestamp)
        elif user_input == "2":
            topic = input("Give note topic: \n")
            notes = proxy.get_notes(topic)
            if not notes:
                print(f"No notes found for topic '{topic}'")
            else:
                for note in notes:
                    print(note)

        elif user_input == "quit":
            pass
        else:
            print("Invalid input. Please enter a valid option.")
    except xmlrpc.client.ProtocolError as err:
        print(f"Protocol error occurred: {err}")
    except xmlrpc.client.Fault as err:
        print(f"Server error occurred: {err.faultString}")
    except ConnectionRefusedError as err:
        print(f"Connection error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
