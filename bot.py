import time
import urllib.parse
from bs4 import BeautifulSoup
from curl_cffi import requests

TELEFONO = "+393755140886"
API_KEY = "6433321"

# Link di ricerca specifici per Idealista nei tuoi comuni
COMUNI = {
    "Bordighera": "https://www.idealista.it/vendita-case/bordighera-imperia/",
    "Ospedaletti": "https://www.idealista.it/vendita-case/ospedaletti-imperia/",
    "Ventimiglia": "https://www.idealista.it/vendita-case/ventimiglia-imperia/",
    "Sanremo": "https://www.idealista.it/vendita-case/sanremo-imperia/",
    "Dolceacqua": "https://www.idealista.it/vendita-case/dolceacqua-imperia/",
    "Vallebona": "https://www.idealista.it/vendita-case/vallebona-imperia/",
    "Seborga": "https://www.idealista.it/vendita-case/seborga-imperia/",
    "San Biagio della Cima": (
        "https://www.idealista.it/vendita-case/san-biagio-della-cima-imperia/"
    ),
    "Soldano": "https://www.idealista.it/vendita-case/soldano-imperia/",
    "Apricale": "https://www.idealista.it/vendita-case/apricale-imperia/",
    "Perinaldo": "https://www.idealista.it/vendita-case/perinaldo-imperia/",
}


def invia_whatsapp(testo):
  testo_encoded = urllib.parse.quote(testo)
  url = f"https://api.callmebot.com/whatsapp.php?phone={TELEFONO}&text={testo_encoded}&apikey={API_KEY}"
  response = requests.get(url)
  return response.status_code == 200


def scansiona_annunci():
  print("🚀 Avvio scansione su Idealista...")

  for comune, url in COMUNI.items():
    print(f"Controllo in corso per: {comune}...")
    try:
      # Richiesta con emulatore Chrome per Idealista
      response = requests.get(url, impersonate="chrome", timeout=15)
      print(f"Status ricevuto per {comune}: {response.status_code}")

      if response.status_code != 200:
        print(f"⚠️ Errore {response.status_code} per {comune}")
        continue

      soup = BeautifulSoup(response.text, "html.parser")
      # Selettore degli annunci su Idealista
      item = soup.find("article", class_="item")

      if item:
        titolo_tag = item.find("a", class_="item-link")
        prezzo_tag = item.find("span", class_="item-price")

        titolo = (
            titolo_tag.text.strip()
            if titolo_tag
            else "Immobile residenziale"
        )
        prezzo = (
            prezzo_tag.text.strip() if prezzo_tag else "Prezzo su richiesta"
        )

        testo_notifica = (
            f"🚨 ALERT IMMOBILIARE 🚨\n\n"
            f"🌐 Sito: Idealista\n"
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
