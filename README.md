# Command Notes (cn.py)

Prosta aplikacja CLI do zarządzania notatkami i zakładkami.

## Funkcje

📓 Notatki:
- Dodawanie notatek z kategoriami
- Przeglądanie notatek
- Kopiowanie treści notatek do schowka
- Usuwanie notatek

🔖 Zakładki:
- Dodawanie zakładek (nazwa + URL)
- Otwarcie zapisanych zakładek w przeglądarce
- Kopiowanie linków do schowka
- Usuwanie zakładek
- Lista wszystkich zapisanych linków

## Użycie

```bash
python cn.py note new <kategoria> <tytuł> <treść>
python cn.py note view
python cn.py note copy <kategoria> <tytuł>
python cn.py note rm <kategoria> <tytuł>

python cn.py new <nazwa> <url>
python cn.py <nazwa>
python cn.py copy <nazwa>
python cn.py rm <nazwa>
python cn.py list
