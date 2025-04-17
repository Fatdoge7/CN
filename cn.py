import json
import sys
import webbrowser
import pyperclip
import os

# Plik, w którym zapisujemy dane
db_file = "notes.json"

def load_data():
    try:
        with open(db_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"notes": {}, "bookmarks": {}}

def save_data(data):
    with open(db_file, "w") as f:
        json.dump(data, f, indent=4)

def add_note(category, title, content):
    data = load_data()
    if category not in data["notes"]:
        data["notes"][category] = {}
    data["notes"][category][title] = content
    save_data(data)
    print(f"Dodano notatkę: [{category}] {title}")

def view_notes():
    data = load_data()
    if not data["notes"]:
        print("Brak zapisanych notatek.")
        return
    for category, notes in data["notes"].items():
        print(f"[{category}]")
        for title, content in notes.items():
            print(f"  {title}: {content}")

def copy_note(category, title):
    data = load_data()
    if category in data["notes"] and title in data["notes"][category]:
        pyperclip.copy(data["notes"][category][title])
        print(f"Skopiowano treść notatki: {title}")
    else:
        print(f"Nie znaleziono notatki {title} w kategorii {category}")

def remove_note(category, *title_parts):
    title = " ".join(title_parts)  # Scal tytuł, jeśli był podany w kilku argumentach
    data = load_data()

    if category in data["notes"] and title in data["notes"][category]:
        del data["notes"][category][title]  # Usuń notatkę
        if not data["notes"][category]:  # Jeśli kategoria jest pusta, usuń ją
            del data["notes"][category]
        save_data(data)
        print(f"Usunięto notatkę: {title}")
        if category not in data["notes"]:
            print(f"Usunięto pustą kategorię: {category}")
    else:
        print(f"Nie znaleziono notatki '{title}' w kategorii '{category}'")

def add_bookmark(name, url):
    data = load_data()
    data["bookmarks"][name] = url
    save_data(data)
    print(f"Dodano zakładkę: {name} -> {url}")

def open_bookmark(name):
    data = load_data()
    if name in data["bookmarks"]:
        url = data["bookmarks"][name]
        webbrowser.open(url)
        print(f"Otwieram: {url}")
    else:
        print(f"Brak zapisanego linku o nazwie '{name}'")

def copy_bookmark(name):
    data = load_data()
    if name in data["bookmarks"]:
        url = data["bookmarks"][name]
        pyperclip.copy(url)
        print(f"Skopiowano do schowka: {url}")
    else:
        print(f"Brak zapisanego linku o nazwie '{name}'")

def remove_bookmark(name):
    data = load_data()
    if name in data["bookmarks"]:
        del data["bookmarks"][name]
        save_data(data)
        print(f"Usunięto link: {name}")
    else:
        print(f"Brak zapisanego linku o nazwie '{name}'")

def list_bookmarks():
    data = load_data()
    if data["bookmarks"]:
        for name, url in data["bookmarks"].items():
            print(f"{name}: {url}")
    else:
        print("Brak zapisanych linków.")

def show_help():
    print("""
Użycie: 
  Notatki:
    cn note new <kategoria> <tytuł> <treść> - Dodaj notatkę
    cn note view - Wyświetl wszystkie notatki
    cn note copy <kategoria> <tytuł> - Skopiuj treść notatki
    cn note rm <kategoria> <tytuł> - Usuń notatkę

  Zakładki:
    cn new <nazwa> <url> - Dodaj zakładkę
    cn <nazwa> - Otwórz zakładkę
    cn copy <nazwa> - Skopiuj link do schowka
    cn rm <nazwa> - Usuń zakładkę
    cn list - Wyświetl wszystkie zakładki

  Inne:
    cn help - Pokaż pomoc
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
    elif sys.argv[1] == "note":
        if len(sys.argv) >= 5 and sys.argv[2] == "new":
            category = sys.argv[3]
            title = sys.argv[4]
            content = " ".join(sys.argv[5:])  # Zbierz resztę argumentów w jeden string
            add_note(category, title, content)
        elif sys.argv[2] == "view":
            view_notes()
        elif len(sys.argv) == 4 and sys.argv[2] == "copy":
            copy_note(sys.argv[3], sys.argv[4])
        elif len(sys.argv) >= 4 and sys.argv[2] == "rm":
            remove_note(sys.argv[3], *sys.argv[4:])
        else:
            show_help()
    elif sys.argv[1] == "new" and len(sys.argv) == 4:
        add_bookmark(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "list":
        list_bookmarks()
    elif sys.argv[1] == "copy" and len(sys.argv) == 3:
        copy_bookmark(sys.argv[2])
    elif sys.argv[1] == "rm" and len(sys.argv) == 3:
        remove_bookmark(sys.argv[2])
    elif sys.argv[1] == "help":
        show_help()
    elif len(sys.argv) == 2:
        open_bookmark(sys.argv[1])
    else:
        show_help()
