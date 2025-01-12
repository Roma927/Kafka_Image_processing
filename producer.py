from confluent_kafka import Producer
import json
import os
import time
import base64

# Kafka Producer Configuration
# producer_conf = {
#     'bootstrap.servers': 'localhost:9092',
#     'client.id': 'img_data_producer'
# }
producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'img_data_producer',
    'acks': 'all',  # Wait for all in-sync replicas to acknowledge the message (more reliable but slower).
    'batch.num.messages': 1000,  # Increase batch size for better throughput.
    'linger.ms': 5,  # Time to wait before sending a batch if not filled.
    'compression.codec': 'snappy',  # Use compression to reduce the size of messages.
    # 'buffer.memory': 33554432,  # Adjust memory buffer size (32MB).
    # 'queue.buffering.max.messages': 10000,  # Increase message queue size.
    # 'queue.buffering.max.kbytes': 10240,  # Max buffer in KB.
    'max.in.flight.requests.per.connection': 5  # Control the number of unacknowledged requests per connection.
}


producer = Producer(producer_conf)

# # Delivery callback for producer
# def delivery_callback(err, msg):
#     if err:
#         print(f"Delivery failed for record {msg.key()}: {err}")
#     else:
#         print(f"Record successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# # Directory containing images
# image_dir = "/mnt/e/Kafka_Task/Stamps"
# images = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith(('.png', '.jpg', '.jpeg'))]

# # Topic to produce to
# topic = "new_img_data"

# # Produce messages
# for index, image_path in enumerate(images):
#     with open(image_path, "rb") as img_file:
#         image_data = base64.b64encode(img_file.read()).decode('utf-8') 

#     label = os.path.splitext(os.path.basename(image_path))[0]

#     message = {
#         "attributeId": label,       
#         "value": image_data,       
#         "timestamp": int(time.time()),
#         "assetId": index + 1        
#     }

#     producer.produce(
#         topic,
#         key=str(index),
#         value=json.dumps(message),
#         callback=delivery_callback
#     )
#     producer.flush()  
#     print(f"Produced: {message}")
#     time.sleep(0.5) 

# producer.flush()

# Delivery callback for producer
def delivery_callback(err, msg):
    if err:
        print(f"Delivery failed for record {msg.key()}: {err}")
    else:
        print(f"Record successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# Directory containing images
image_dir = "/mnt/e/Kafka_Task/Stamps"

try:
    images = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not images:
        print("No images found in the directory.")
        exit()
except Exception as e:
    print(f"Error reading image directory: {e}")
    exit()

# Topic to produce to
topic = "new_img_data"

# Produce messages
for index, image_path in enumerate(images):
    try:
        with open(image_path, "rb") as img_file:
            image_data = base64.b64encode(img_file.read()).decode('utf-8') 

        label = os.path.splitext(os.path.basename(image_path))[0]

        message = {
            "attributeId": label,       
            "value": image_data,       
            "timestamp": int(time.time()),
            "assetId": index + 1        
        }

        producer.produce(
            topic,
            key=str(index),
            value=json.dumps(message),
            callback=delivery_callback
        )

        print(f"Queued: {message}")
        
    except Exception as e:
        print(f"Failed to process image {image_path}: {e}")

# Wait for all messages to be delivered
producer.flush()
print("All messages have been delivered.")
