import json
import pika
import threading
ROUTING_KEY = 'user.created.key'
EXCHANGE = 'user_exchange'
THREADS = 5

class UserCreatedListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #BlockingConnection abstracts its I/O loop from the application while
        # adhering to asynchronous RPC nature of the AMQP protocol,
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        #Channel multiplexes a TCP connection
        self.channel = connection.channel()
        #Creates an exchange if it does not already exist (fanout or direct or topic)
        self.channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')
        #queue_declare() Creates or checks a queue
        #queue='' will cause RabbitMQ to create a unique queue
        #exclusive=True : Only allow access by the current connection
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        #Bind the queue to the specified exchange
        self.channel.queue_bind(queue=queue_name, exchange=EXCHANGE, routing_key=ROUTING_KEY)
        #Specify quality of service. 
        #prefetch_count specifies a prefetch window size
        self.channel.basic_qos(prefetch_count=THREADS*10)
        # When ever a new message arrives on queue
        # callback method will be self.callback
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback)
        
    # channel: Channel used for communication
    # method : Message delivery details (if curious, print it to see the result)
    # property: user-defined properties on the message
    # body : contains message
    def callback(self, channel, method, properties, body):
        if(properties.content_type=="user_created_method"):
            message = json.loads(body)
            # Do What ever with message, In real world we should be
            # sending an Email asynchronously to user
            print(message)
        #send acknowledgement back (Good practice)    
        channel.basic_ack(delivery_tag=method.delivery_tag)
        
    def run(self):
        print ('Inside EmailService :  Created Listener ')
        self.channel.start_consuming()
    
   