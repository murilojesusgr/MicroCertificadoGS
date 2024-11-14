from jinja2 import Template
import pdfkit
import logging

path_wkhtmltopdf = '/usr/bin/wkhtmltopdf' 
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

def generate_certificate(data):
    with open('templates/template.html') as file:
        template = Template(file.read())
    html_content = template.render(name=data['name'], course=data['course'], date_issued=data['date_issued'])
    return html_content

def save_pdf(html_content, file_path):
    try:
        pdfkit.from_string(html_content, file_path, configuration=config)
        logging.info(f"PDF salvo com sucesso em: {file_path}")
    except Exception as e:
        logging.error(f"Erro ao salvar PDF: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    data = {
        "name": "Murilo Rocha",
        "course": "Python na FIAP",
        "date_issued": "13/11/2024"
    }
    html_content = generate_certificate(data)

    pdf_path = 'generated_certificate.pdf'
    save_pdf(html_content, pdf_path)
