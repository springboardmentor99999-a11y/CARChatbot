from pdfminer.high_level import extract_text
def extract_text_from_pdf(file):
    
  try:
    return extract_text(file)
  except:
   return ""