from pathlib import Path
import openpyxl
import pdfplumber

def extract_tables_from_pdf(pdf_path: Path, max_pages: int = 10):
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages[:max_pages]):
                table = page.extract_table()
                if table:
                    tables.append((page_number, table))
        return tables
    except Exception as e:
        print(f"Erro ao extrair tabelas do PDF: {e}")
        return []


def clean_header(header: list) -> list:
    header = [col.replace("\n", " ").strip() for col in header]
    header = [col.replace("OD", "Seg. Odontológica").replace("AMB", "Seg. Ambulatorial") for col in header]
    return header


def save_to_excel(tables: list, output_path: Path):
    workbook = openpyxl.Workbook()
    sheet_placeholder = workbook.active

    for page_number, table in tables:
        sheet_name = f"Pagina {page_number}"
        new_sheet = workbook.create_sheet(title=sheet_name)

        header = clean_header(table[0])
        new_sheet.append(header)

        for row in table[1:]:
            new_sheet.append(row)

    workbook.remove(sheet_placeholder)
    workbook.save(output_path)
    print(f"Arquivo salvo com sucesso: {output_path}")


def main():
    pdf_path = Path("C:\\Users\\michael\\OneDrive\\Documentos\\Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")
    output_path = Path("meu_arquivo.csv")

    tables = extract_tables_from_pdf(pdf_path)
    if tables:
        save_to_excel(tables, output_path)
    else:
        print("Nenhuma tabela encontrada no PDF.")


if __name__ == "__main__":
    main()
