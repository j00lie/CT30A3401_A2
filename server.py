from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import requests
from socketserver import ThreadingMixIn
import xml.etree.ElementTree as ET


class NoteServer:
    def __init__(self):
        self.xml_file = "notes.xml"

    def get_notes(self, topic_name):
        # Read the XML file
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            matching_elements = root.findall(f".//topic[@name='{topic_name.lower()}']")

            if len(matching_elements) > 0:
                return [ET.tostring(element).decode() for element in matching_elements]

            else:
                return []

        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
            return []
        except Exception as e:
            print(f"Error in get_notes: {e}")
            return []

    def save_notes(self, topic_name, note_name, note_text, timestamp):
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            # Check if the topic already exists
            existing_topic = root.find(f"./topic[@name='{topic_name.lower()}']")
            if existing_topic is None:
                # If the topic doesn't exist, create a new element
                new_topic = ET.Element("topic", {"name": topic_name.lower()})
                root.append(new_topic)
            else:
                new_topic = existing_topic

            # Create a new note element and add it to the topic

            new_note = ET.Element("note", {"name": note_name})
            new_text = ET.Element("text")
            new_text.text = note_text
            new_note.append(new_text)
            new_timestamp = ET.Element("timestamp")
            new_timestamp.text = timestamp
            new_note.append(new_timestamp)

            new_topic.append(new_note)

            # Write the updated XML to the file
            tree.write(self.xml_file, xml_declaration=True)

        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
        except Exception as e:
            print(f"Error in save_notes: {e}")

    def append_to_topic(self, topic_name, link):
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        # Check if the topic already exists
        existing_topic = root.find(f"./topic[@name='{topic_name.lower()}']")
        if existing_topic is None:
            return None
        else:
            # Add Wikipedia information to the topic
            wikipedia = ET.Element("wikipedia")
            # wikipedia_summary = ET.Element("summary")
            # wikipedia_summary.text = summary
            wikipedia_link = ET.Element("link")
            wikipedia_link.text = link
            # wikipedia.append(wikipedia_summary)
            wikipedia.append(wikipedia_link)
            existing_topic.append(wikipedia)
            tree.write(self.xml_file, xml_declaration=True)

            return link

    def get_wikipedia_info(self, topic_name):
        # Send a GET request to the Wikipedia API

        URL = "https://en.wikipedia.org/w/api.php"

        PARAMS = {
            "action": "opensearch",
            "search": topic_name.lower(),
            "limit": "1",
            "format": "json",
        }

        response = requests.get(url=URL, params=PARAMS)

        # Check if the response was successful
        if response.status_code == 200:
            data = response.json()
            print(data)
            # summary = data["extract"]
            if data[-1]:
                full_link = data[-1][0]
                return full_link
            else:
                return None
        else:
            return response.status_code


class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    def __init__(self, addr, requestHandler=SimpleXMLRPCRequestHandler):
        SimpleXMLRPCServer.__init__(
            self, addr, requestHandler=requestHandler, allow_none=True
        )
        self.allow_reuse_address = True


if __name__ == "__main__":
    server = ThreadedXMLRPCServer(("localhost", 8000))
    server.register_instance(NoteServer())

    try:
        print("Serving...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        server.shutdown()
        server.server_close()
    except Exception as e:
        print(f"Error in main: {e}")

# if __name__ == "__main__":
#     server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
#     server.register_instance(NoteServer())
#     try:
#         print("Serving...")
#         server.serve_forever()
#     except KeyboardInterrupt:
#         print("Shutting down...")
