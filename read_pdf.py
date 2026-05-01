from pypdf import PdfReader

reader = PdfReader(r"c:\Users\ROBERT\Documents\sipan\IX\lenguaje taller\Sesion_02\Sesion 04. Componentes en Django.pdf")
with open("pdf_text.txt", "w", encoding="utf-8") as f:
    for i, page in enumerate(reader.pages):
        f.write(f"--- Page {i + 1} ---\n")
        f.write(page.extract_text() + "\n")
