# MicroCertificadoGS
Global Solution de microserviço - Gerador de certificado.

Professor, somos a dupla que não tava criando o banco de dados na sala porém em casa funcionou, deixamos alguns pdfs gerados criados na pasta.

Instruções para rodar:
Instale as bibliotecas nos requirements

Rodar o docker pra conectar com o Rabbitmq:
docker compose up --build

após subir o container, acessar o postman com:
método POST
https//localhost:/5000/certificates
authorization
user
password

headers
content-type
application/json

raw - json
{
    "name": "Murilo Rocha",
    "course": "Python",
    "date_issued": "13/11/2024"
}

O PDF será criado na pasta pdfs dentro do código.
