import re
import PyPDF2
import pandas as pd
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from django.http import HttpResponse
from collections import namedtuple

from csv_convertor.serializers import FileSerializer


class GenerateCSV(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            pdf_file = request.FILES["file"]
            table_data = r"^05-"
            split_regex = r"(?:\d{2}-\d+\sY\s[A-Z\d]+\.[A-Z\d]+|CURSEUR\s\d\sY\s[A-Z\d]+)"
            table_lines = []

            Line = namedtuple("List", "Code RéfDescription DimColoris Quant Unité PrixUnit Total")

            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pages = len(pdf_reader.pages)

            for page_num in range(pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()

                for line in page_text.split("\n"):
                    if re.search(table_data, line):
                        if re.search(split_regex, line):
                            all_matches = re.findall(split_regex, line)
                            split_line = "-".join(all_matches[0].split()) + " " + "-".join(
                                all_matches[1].split()) + " " + " ".join(
                                line.split()[7:])
                            table_lines.append(Line(*split_line.split()))
                        else:
                            table_lines.append(Line(*line.split()))

            if len(table_lines):
                df = pd.DataFrame(table_lines)
                csv_file = df.to_csv(index=False)
                response = HttpResponse(csv_file, content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="output.csv"'
                return response
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
