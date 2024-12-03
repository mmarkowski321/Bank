# Użycie lekkiego obrazu Python
FROM python:3.9-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie pliku z zależnościami aplikacji
COPY requirements.txt /app/

# Instalacja zależności aplikacji
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie całego kodu źródłowego do kontenera
COPY . /app/

# Domyślne polecenie uruchamiające aplikację
CMD ["python", "run.py"]
