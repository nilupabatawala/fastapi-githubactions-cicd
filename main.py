from fastapi import FastAPI
import pika
from fastapi.responses import HTMLResponse

app = FastAPI()

credentials= pika.PlainCredentials('guest','guest')

#publish message to the queue
@app.post("/publish")
def publish_message(message: str ):
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq-service', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='testqueue')

    channel.basic_publish(exchange='', routing_key='testqueue',
                      body=message)
    
    return {"Published sucessfully to the queue": message}


def get_rabbitmq_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq-service', credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue='testqueue')
    return channel

# #consume message from the queue
@app.get("/consume")
def consume_message():
    channel = get_rabbitmq_channel()
    method_frame, header_frame, body = channel.basic_get(queue='testqueue', auto_ack=True)
    if method_frame:
        print(f"Received {body.decode()}")
        return {"Consumed message": body.decode()}
    else:
        print("No message in queue")
        return {"message": "No message available"}
     
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", 'r') as f:
        return f.read()