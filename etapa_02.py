import openpyxl
import pdfplumber
import zipfile
import os


pdf_path = "C:\\Users\\michael\\OneDrive\\Documentos\\Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"

tables = []
wb = openpyxl.Workbook()
sheet = wb.active
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages[:10]):
        table = page.extract_table()
        if table:
            new_sheet = wb.create_sheet(title="Pagina " +str(i))
            header = [col.replace("\n", " ").strip() for col in table[0]]
            header = [col.replace("OD", "Seg. Odontológica").replace("AMB", "Seg. Ambulatorial") for col in header]

            new_sheet.append(header)
            for row in table[1:]:
                new_sheet.append(row)
            tables.extend(table)

wb.remove(sheet)

excel_filename = "anexo_01.csv"
#wb.save(excel_filename)

zip_filename = "teste_michael.zip"
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    zipf.write(excel_filename, os.path.basename(excel_filename))

