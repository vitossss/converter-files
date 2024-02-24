from django.views import View
from django.http import HttpResponse
from django.conf import settings
import os

import PyPDF2


class GenerateCSV(View):
    def get(self, request):
        pdf_path = os.path.join(settings.STATIC_ROOT, "COMMANDE STOCK BRUXELLES.pdf")

        with open(pdf_path, "rb") as pdf:
            reader = PyPDF2.PdfReader(pdf, strict=False)
            pdf_text = []

            for page in reader.pages:
                content = page.extract_text()
                pdf_text.append(content)

        if len(pdf_text):
            response = HttpResponse(pdf_text, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="output.csv"'
            return response
        else:
            return HttpResponse("Your pdf file is empty")
