import os
import pdfkit

WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

def to_pdf():
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    html_path = os.path.abspath("output/report.html")
    pdf_path = os.path.abspath("output/report.pdf")
    options = {
        "enable-local-file-access": None,
        "quiet": "",             
    }
    pdfkit.from_file(html_path, pdf_path, configuration=config, options=options)
    print("Saved:", pdf_path)

if __name__ == "__main__":
    to_pdf()