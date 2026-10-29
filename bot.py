import time
import urllib.parse
import requests
from bs4 import BeautifulSoup

TELEFONO = "+393755140886"
API_KEY = "6433321"

COMUNI = {
    "Bordighera": "https://www.immobiliare.it/vendita-case/bordighera/",
    "Ospedaletti": "https://www.immobiliare.it/vendita-case/ospedaletti/",
    "Ventimiglia": "https://www.immobiliare.it/vendita-case/ventimiglia/",
    "Sanremo": "https://www.immobiliare.it/vendita-case/sanremo/",
    "Dolceacqua": "https://www.immobiliare.it/vendita-case/dolceacqua/",
    "Vallebona": "https://www.immobiliare.it/vendita-case/vallebona/",
    "Seborga": "https://www.immobiliare.it/vendita-case/seborga/",
    "San Biagio della Cima": (
        "https://www.immobiliare.it/vendita-case/san-biagio-della-cima/"
    ),
    "Soldano": "https://www.immobiliare.it/vendita-case/soldano/",
    "Apricale": "https://www.immobiliare.it/vendita-case/apricale/",
    "Perinaldo": "https://www.immobiliare.it/vendita-case/perinaldo/",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.9",
}


def invia_whatsapp(testo):
  testo_encoded = urllib.parse.quote(testo)
  url = f"https://api.callmebot.com/whatsapp.php?phone={TELEFONO}&text={testo_encoded}&apikey={API_KEY}"
  response = requests.get(url)
  return response.status_code == 200


def scansiona_annunci():
  print("🚀 Avvio scansione di tutti i comuni su GitHub Actions...")

  for comune, url in COMUNI.items():
    print(f"Controllo in corso per: {comune}...")
    try:
      response = requests.get(url, headers=HEADERS, timeout=15)
      if response.status_code != 200:
        print(f"⚠️ Errore {response.status_code} per {comune}")
        continue

      soup = BeautifulSoup(response.text, "html.parser")
      item = soup.find("div", class_="nd-list__item")

      if item:
        titolo_tag = item.find("a", class_="in-realEstateList__title")
        prezzo_tag = item.find("div", class_="in-realEstateList__price")

        titolo = titolo_tag.text.strip() if titolo_tag else "Immobile residenziale"
        prezzo = prezzo_tag.text.strip() if prezzo_tag else "Prezzo su richiesta"

        testo_notifica = (
            f"🚨 ALERT IMMOBILIARE 🚨\n\n"
            f"🌐 Sito: Immobiliare.it\n"
            f"📍 Zona: {comune}\n"
            f"🏠 Titolo: {titolo}\n"
            f"💰 Prezzo: {prezzo}"
        )

        if invia_whatsapp(testo_notifica):
          print(f"✅ Notificata novità per {comune}")

      time.sleep(3)
    except Exception as e:
      print(f"❌ Errore per {comune}: {e}")


if __name__ == "__main__":
  scansiona_annunci()
