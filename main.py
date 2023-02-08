from src.whatsup import Whatsup
import sys

if __name__ == "__main__":
    config_file_path = sys.argv[1]
    whatsup = Whatsup(config_file_path)
    whatsup.send_messages()
