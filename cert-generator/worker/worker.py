import time
import pika
import json
import logging
from generate_certificate import generate_certificate, save_pdf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Certificate

time.sleep(10)

DATABASE_URL = "postgresql://user:password@db/certs_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

logging.basicConfig(level=logging.INFO)

def process_message(ch, method, properties, body):
    data = json.loads(body)
    
    session = Session()
    cert = session.query(Certificate).filter_by(id=data['id']).first()
    
    if cert is None:
        ch.basic_ack(delivery_tag=method.delivery_tag) 
        return

    html_content = generate_certificate(data)
    
    pdf_path = f'/app/pdfs/{cert.id}.pdf'
    
    try:
        save_pdf(html_content, pdf_path)
        cert.pdf_path = pdf_path
        session.commit() 
        logging.info(f"PDF salvo em: {pdf_path}")
        
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logging.error(f"Erro ao salvar PDF: {e}")

def start_worker():
    while True: 
        try:
            credentials = pika.PlainCredentials('user', 'password')
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
            channel = connection.channel()
            channel.queue_declare(queue='certificates')
            channel.basic_consume(queue='certificates', on_message_callback=process_message)
            logging.info("Worker conectado ao RabbitMQ, pronto para consumir mensagens.")
            channel.start_consuming()
        except Exception as e:
            logging.error(f"Erro ao conectar ao RabbitMQ: {e}")
            time.sleep(5)

if __name__ == "__main__":
    start_worker()
