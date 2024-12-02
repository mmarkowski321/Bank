FROM ubuntu:20.04
# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
 python3 \
 nodejs \
 build-essential \

# Instalacja zależności aplikacji
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
# Kopiowanie kodu źródłowego
COPY . /app/
CMD ["python3", "/app/app.py"]
