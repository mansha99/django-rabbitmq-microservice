import threading
import pika
from django.conf import settings


class AMQPConsuming(threading.Thread):
    def callback(self, ch, method, properties, body):
        # do something
        pass

    @staticmethod
    def _get_connection():
        parameters = pika.URLParameters(settings.RABBIT_URL)
        return pika.BlockingConnection(parameters)

    def run(self):
        connection = self._get_connection()
        channel = connection.channel()

        channel.queue_declare(queue='task_queue6')
        print('Hello world! :)')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.callback, queue='queue')

        channel.start_consuming()

class AMQPCProducer:
    @staticmethod
    def sendMessage():
        connection = pika.BlockingConnection()
        channel = connection.channel()
        channel.basic_publish(exchange='test', routing_key='test',
                      body=b'Test message.')
        connection.close()        