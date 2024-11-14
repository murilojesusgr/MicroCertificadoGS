import logging
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Certificate
import pika
import json

app = Flask(__name__)

DATABASE_URL = "postgresql://user:password@db/certs_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

logging.basicConfig(level=logging.INFO)

@app.route('/certificates', methods=['POST'])
def create_certificate():
    try:
        data = request.get_json()
        session = Session()
        new_cert = Certificate(
            name=data['name'], 
            course=data['course'], 
            date_issued=data['date_issued'],
            pdf_path=''
        )
        session.add(new_cert)
        session.commit()

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq', credentials=pika.PlainCredentials('user', 'password'))
        )
        channel = connection.channel()

        channel.queue_declare(queue='certificates')

        message = {
        'id': new_cert.id,
        'name': data['name'],
        'course': data['course'],
        'date_issued': data['date_issued']
        }

        channel.basic_publish(exchange='', routing_key='certificates', body=json.dumps(message))

        connection.close()

        return jsonify({"mensagem": "Certificado Criado!"}), 201

    except Exception as e:
        logging.error(f"Erro ao criar certificado: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
