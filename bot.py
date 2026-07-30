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
  c.setFont("Helvetica", 18)
  c.drawCentredString(latime / 2, inaltime - 280, f"Subiect: {titlu}")
  c.setFont("Helvetica", 12)
  c.drawCentredString(latime / 2, 100, "Ediție Specială • KDP Ready")
  c.showPage()


def main():
  if not TOKEN or not CHAT_ID:
    print("Eroare: Lipsesc token-ul sau chat ID-ul din secrete!")
    return

  bot = telegram.Bot(token=TOKEN)
  subiect = "Animale mitice și dragoni prietenoși"  # Poți schimba subiectul oricând de aici

  print("Încep generarea cărții KDP (40 pagini + pagini libere + copertă)...")
  nume_pdf = "carte_kdp_40_pagini.pdf"
  imagini_generate = []

  # Generăm cele 40 de pagini
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

  # Adăugăm paginile de colorat alternate cu pagini libere
  for img in imagini_generate:
    c.drawImage(img, 36, 36, width=latime - 72, height=inaltime - 72)
    c.showPage()  # Pagina de colorat
    c.showPage()  # Pagină goală (albă) următoare

  c.save()

  # Trimitem PDF-ul pe Telegram
  async def trimite():
    with open(nume_pdf, "rb") as f:
      await bot.send_document(
          chat_id=CHAT_ID,
          document=f,
          filename="carte_colorat_kdp.pdf",
          caption=(
              "Iată cartea ta de colorat cu 40 de pagini, pagini libere și"
              " copertă, gata pentru Amazon KDP!"
          ),
      )

  asyncio.run(trimite())

  # Curățăm imaginile temporare
  for img in imagini_generate:
    if os.path.exists(img):
      os.remove(img)

  print("Gata! Totul a fost trimis cu succes pe Telegram.")


if __name__ == "__main__":
  main()
