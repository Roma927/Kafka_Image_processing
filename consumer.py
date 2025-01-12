from confluent_kafka import Consumer
import json
import pandas as pd
import base64
import os

# Kafka Consumer Configuration
consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'img_data_consumer_group',
    'auto.offset.reset': 'earliest'  # Start reading from the beginning of the topic
}
# consumer_conf = {
#     'bootstrap.servers': 'localhost:9092',
#     'group.id': 'img_data_consumer',
#     'auto.offset.reset': 'earliest',  # Start reading from the earliest message.
#     'enable.auto.commit': False,  # Manually commit offsets for better control.
#     'fetch.max.bytes': 10485760,  # Fetch larger batches of data (10MB).
# }

consumer = Consumer(consumer_conf)

# Subscribe to the Kafka topic
topic = "new_img_data"
consumer.subscribe([topic])

# Directory to save images
output_image_dir = "received_images"
os.makedirs(output_image_dir , exist_ok=True)

# Collect messages for CSV
received_data = []

print("Consuming messages...")
try:
    while True:
        msg = consumer.poll(1.0)  # Wait for a message for up to 1 second
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Deserialize the JSON message
        message = json.loads(msg.value().decode('utf-8'))
        print(f"Consumed: {message}")

        # Extract fields
        attribute_id = message.get("attributeId")
        image_data_base64 = message.get("value")
        timestamp = message.get("timestamp")
        asset_id = message.get("assetId")

        # Decode and save the image
        image_filename = f"{attribute_id}_{asset_id}.jpg"
        image_path = os.path.join(output_image_dir, image_filename)

        with open(image_path, "wb") as img_file:
            img_file.write(base64.b64decode(image_data_base64))

        # Add data to list for CSV export
        received_data.append({
            "image_path": image_path,
            "annotation": attribute_id,
            # "timestamp": timestamp,
            # "asset_id": asset_id
        })

        # Optional: Stop after consuming a specific number of messages
        if len(received_data) >= 10000:  # Adjust this limit as needed
            break

except KeyboardInterrupt:
    print("Consumer interrupted.")
finally:
    # Close the consumer
    consumer.close()

# Save received messages to a CSV file
df = pd.DataFrame(received_data)
output_csv_path = "consumed_data.csv"
df.to_csv(output_csv_path, index=False)
print(f"Saved consumed data to {output_csv_path}")

