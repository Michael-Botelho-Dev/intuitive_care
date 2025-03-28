import requests
import zipfile
import os


def download_file(url, folder):
    filename = os.path.join(folder, url.split("/")[-1])
    with requests.get(url, stream=True) as r:
        with open(filename, 'wb') as f:
            f.write(r.content)
    return filename


def main():
    url_base = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    pdf_links = [
        "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf",
        "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"
    ]

    folder = "downloads"
    os.makedirs(folder, exist_ok=True)

    files = [download_file(url, folder) for url in pdf_links]

    with zipfile.ZipFile("anexos.zip", 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))

    print("Download e compactação concluídos!")


if __name__ == "__main__":
    main()
