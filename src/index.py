from ui.text_ui import TextUI
from initialize_database import initialize_database

def main():
    initialize_database()
    text_ui = TextUI()
    text_ui.start()

if __name__ == "__main__":
    main()