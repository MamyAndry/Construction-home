from xhtml2pdf import pisa

class Pdf_handler():
    pdf_name = ""
    html_string = ""

    def __init__(self, pdf_name, html_string):
        self.pdf_name = pdf_name
        self.html_string = html_string

    def toPdf(self):
        try:
            with open(self.pdf_name, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(self.html_string, dest = pdf_file)
                if not pisa_status.err:
                    pass
                else:
                    print("Error creating PDF:", pisa_status.err)
                    return None
            with open(self.pdf_name, "rb") as pdf_file_2:
                pdf_content = pdf_file_2.read()
            return pdf_content
        except Exception as e:
            print("Error:", e)
            return None