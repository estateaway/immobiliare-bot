import time
import urllib.parse
from bs4 import BeautifulSoup
from curl_cffi import requests  # Emula un browser reale per bypassare Cloudflare

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


def invia_whatsapp(testo):
  testo_encoded = urllib.parse.quote(testo)
  url = f"https://api.callmebot.com/whatsapp.php?phone={TELEFONO}&text={testo_encoded}&apikey={API_KEY}"
  response = requests.get(url)
  return response.status_code == 200


def scansiona_annunci():
  print("🚀 Avvio scansione con emulatore browser anti-blocco...")

  for comune, url in COMUNI.items():
    print(f"Controllo in corso per: {comune}...")
    try:
      # impersonate="chrome" inganna i controlli di sicurezza del sito
      response = requests.get(url, impersonate="chrome", timeout=15)
      print(f"Status ricevuto per {comune}: {response.status_code}")

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
      print(f"❌ Errore di connessione per {comune}: {e}")


if __name__ == "__main__":
  scansiona_annunci()
