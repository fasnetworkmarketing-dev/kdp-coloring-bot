import asyncio
import os
import telegram
from generator_ia import genereaza_imagine_colorat
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def deseneaza_coperta(c, latime, inaltime, titlu):
  c.setFont("Helvetica-Bold", 30)
  c.drawCentredString(latime / 2, inaltime - 220, "CARTE DE COLORAT")
  c.setFont("Helvetica", 16)
  c.drawCentredString(latime / 2, inaltime - 280, f"Subiect: {titlu}")
  c.setFont("Helvetica", 12)
  c.drawCentredString(latime / 2, 100, "Ediție Specială • KDP Ready")
  c.showPage()


def main():
  if not TOKEN or not CHAT_ID:
    print("Eroare: Lipsesc token-ul sau chat ID-ul din secrete!")
    return

  bot = telegram.Bot(token=TOKEN)

  # AICI poți schimba subiectul oricând vrei tu pentru următoarea carte!
  subiect = "Robotelul aventurier in spatiu si planete misterioase"

  print(
      f"Încep generarea cărții KDP pentru subiectul: '{subiect}' (40 pagini +"
      f" pagini libere + copertă)..."
  )
  nume_pdf = "carte_kdp_40_pagini.pdf"
  imagini_generate = []

  # Generăm cele 40 de pagini de colorat
  for i in range(1, 41):
    print(f"Generez pagina de colorat {i}/40...")
    img_path = genereaza_imagine_colorat(subiect, i)
    if img_path and os.path.exists(img_path):
      imagini_generate.append(img_path)

  if not imagini_generate:
    print("Nu s-a putut genera nicio imagine.")
    return

  # Construim PDF-ul
  c = canvas.Canvas(nume_pdf, pagesize=letter)
  latime, inaltime = letter

  # Adăugăm coperta
  deseneaza_coperta(c, latime, inaltime, subiect)

  # Adăugăm paginile de colorat alternate cu pagini libere (albe)
  for img in imagini_generate:
    c.drawImage(img, 36, 36, width=latime - 72, height=inaltime - 72)
    c.showPage()  # Pagina de colorat
    c.showPage()  # Pagină albă de protecție

  c.save()

  # Trimitem PDF-ul pe Telegram
  async def trimite():
    with open(nume_pdf, "rb") as f:
      await bot.send_document(
          chat_id=CHAT_ID,
          document=f,
          filename="carte_colorat_robotel_spatiu.pdf",
          caption=(
              f"Iată cartea ta de colorat cu subiectul: *{subiect}*! Conține 40 de"
              " pagini, pagini libere și copertă, gata pentru Amazon KDP."
          ),
          parse_mode="Markdown",
      )

  asyncio.run(trimite())

  # Curățăm imaginile temporare de pe disc
  for img in imagini_generate:
    if os.path.exists(img):
      os.remove(img)
  if os.path.exists(nume_pdf):
    os.remove(nume_pdf)

  print("Gata! Cartea a fost trimisă cu succes pe Telegram.")


if __name__ == "__main__":
  main()
