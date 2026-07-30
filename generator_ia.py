import os
from google import genai
from google.genai import types
import requests

# Inițializăm clientul Gemini folosind cheia secretă din GitHub Actions
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def genereaza_imagine_colorat(subiect, numar_pagina):
  prompt = (
      f"A professional black and white coloring book page for kids, theme:"
      f" {subiect}, clean thick black outlines, pure white background, no"
      f" shading, no gray, vector style, high contrast, page number {numar_pagina}"
  )

  try:
    # Folosim modelul de generare imagini Imagen
    result = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            output_mime_type="image/png",
            aspect_ratio="3:4",  # Format portret potrivit pentru cărți
            person_generation="ALLOW_ADULT",
        ),
    )

    for i, generated_image in enumerate(result.generated_images):
      image_path = f"pagina_{numar_pagina}.png"
      image = generated_image.image
      # Salvăm imaginea temporar pe disc
      image.save(image_path)
      return image_path

  except Exception as e:
    print(f"Eroare la generarea imaginii {numar_pagina}: {e}")
    return None
