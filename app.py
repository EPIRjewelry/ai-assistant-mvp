import os
import google.generativeai as genai
from flask import Flask, jsonify, request
from flask_cors import CORS # Do obsługi żądań z innego źródła (Twojego sklepu)

# --- Konfiguracja ---

# Inicjalizacja aplikacji Flask
app = Flask(__name__)
CORS(app) # Umożliwia żądania z Twojego sklepu Shopify do tej aplikacji

# Wczytaj klucz API Google Gemini z zmiennej środowiskowej
# (Musisz ustawić zmienną GOOGLE_API_KEY na platformie hostingowej, np. Railway)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if not GOOGLE_API_KEY:
    print("BŁĄD: Zmienna środowiskowa GOOGLE_API_KEY nie jest ustawiona!")
    # W prawdziwej aplikacji lepiej obsłużyć ten błąd bardziej elegancko
    exit() # Zakończ, jeśli nie ma klucza

# Konfiguracja klienta Google Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Lub inny model Gemini, np. gemini-1.5-pro

# --- Dane dla MVP ---

# Lista alternatywnych kamieni (przechowywana bezpośrednio w kodzie dla MVP)
lista_kamieni_json = """
[
  { "nazwa_kamienia": "Granat", "cena_koncowa_pln": 290 },
  { "nazwa_kamienia": "Cytryn", "cena_koncowa_pln": 290 },
  { "nazwa_kamienia": "Ametyst", "cena_koncowa_pln": 290 },
  { "nazwa_kamienia": "Topaz Sky Blue", "cena_koncowa_pln": 290 },
  { "nazwa_kamienia": "Topaz London Blue", "cena_koncowa_pln": 340 },
  { "nazwa_kamienia": "Topaz Swiss Blue", "cena_koncowa_pln": 310 }
]
"""

# Nasz proaktywny prompt (Wersja 2)
prompt_template = f"""
# Rola i Kontekst
Jesteś proaktywnym, przyjaznym i kompetentnym asystentem AI w sklepie jubilerskim Epir Biżuteria... (itd. - cała treść promptu Wersja 2)

# Dane Wejściowe (Dostępne Alternatywy)
... (itd.)
{lista_kamieni_json}

# Zadanie dla AI
... (itd.)

# Przykład Oczekiwanej Odpowiedzi (Proaktywna Wiadomość Początkowa)
... (itd.)
"""

# --- Logika Aplikacji (Endpoint API) ---

# Definicja endpointu, który będzie wywoływany przez JavaScript z Twojego sklepu
@app.route('/get-proactive-message', methods=['GET']) # Używamy GET dla prostoty MVP
def get_ai_message():
    try:
        # W tym MVP prompt jest statyczny, więc po prostu go używamy
        final_prompt = prompt_template

        # Wywołanie API Gemini
        print("Wysyłanie promptu do Gemini API...") # Logowanie dla debugowania
        response = model.generate_content(final_prompt)
        print("Otrzymano odpowiedź od Gemini API.") # Logowanie

        # Pobranie wygenerowanego tekstu
        ai_message = response.text

        # Zwrócenie odpowiedzi AI w formacie JSON do frontendu
        return jsonify({"message": ai_message})

    except Exception as e:
        # Podstawowa obsługa błędów
        print(f"Wystąpił błąd: {e}")
        # Zwróć informację o błędzie do frontendu
        return jsonify({"error": "Przepraszamy, wystąpił błąd podczas generowania odpowiedzi."}), 500

# --- Uruchomienie Aplikacji ---

# Ten fragment pozwala uruchomić aplikację lokalnie do testów
# Na platformie jak Railway, sposób uruchomienia może być inny (np. przez Gunicorn)
if __name__ == '__main__':
    app.run(debug=True, port=5000) # Uruchom na porcie 5000 w trybie debugowania