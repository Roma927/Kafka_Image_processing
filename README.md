# Kafka_Image_processing
 
This project is a **Kafka-based image processing system** that allows you to produce and consume image data using Apache Kafka. The system includes a **producer** that sends image data to a Kafka topic and a **consumer** that processes and saves the images to a local directory. The project is containerized using Docker for easy setup and deployment.

---

## About

This project demonstrates how to use **Apache Kafka** for real-time image processing. It includes:
- A **Kafka producer** that reads images from a directory, encodes them in Base64, and sends them to a Kafka topic.
- A **Kafka consumer** that listens to the topic, decodes the images, and saves them to a local directory.
- A **Docker Compose** setup to run Kafka and related services (broker, control center) in containers.

The system is designed to handle large volumes of image data efficiently and can be extended for various use cases, such as image recognition, data pipelines, or real-time analytics.

---

## Features

- **Kafka Producer**:
  - Reads images from a specified directory.
  - Encodes images in Base64 and sends them to a Kafka topic.
  - Supports large batch sizes and compression for efficient data transfer.

- **Kafka Consumer**:
  - Listens to the Kafka topic for incoming image data.
  - Decodes Base64 images and saves them to a local directory.
  - Logs metadata (e.g., image path, annotation) to a CSV file.

- **Dockerized Kafka Setup**:
  - Includes Kafka broker and Confluent Control Center.
  - Easy to set up and run using Docker Compose.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** and **Docker Compose**
- **Python 3.8 or higher**
- **Confluent Kafka Python Client** (`confluent-kafka`)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Roma927/Kafka_Image_processing
   cd Kafka_Image_processing
   ```

2. **Set up Kafka using Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Run the Kafka producer**:
   ```bash
   python producer.py
   ```

4. **Run the Kafka consumer**:
   ```bash
   python consumer.py
   ```

---

## Usage

### Kafka Producer
The producer reads images from the `Stamps` directory, encodes them in Base64, and sends them to the `new_img_data` Kafka topic. You can modify the `image_dir` variable in `producer.py` to point to your image directory.

### Kafka Consumer
The consumer listens to the `new_img_data` topic, decodes the images, and saves them to the `received_images` directory. It also logs metadata (e.g., image path, annotation) to a CSV file (`consumed_data.csv`).

### Docker Compose
The `docker-compose.yml` file sets up the following services:
- **Kafka Broker**: Handles message queuing and distribution.
- **Confluent Control Center**: Provides a web UI for monitoring Kafka clusters.

To access the Confluent Control Center, navigate to `http://localhost:9021`.

---

## Project Structure

```
Kpi_simulator_AirFlow/
├──received_images
├──Stamps
├── consumer.py            
├── producer.py           
├── docker-compose.yml     
├── requirements.txt       
├── received_images/       
├── consumed_data.csv      
└── README.md              
```

---

## Example Output

### Consumed Data (CSV)
The `consumed_data.csv` file contains metadata about the consumed images:
```csv
image_path,annotation
received_images/٠١-مارس-٢٠٢٤_5.jpg,٠١-مارس-٢٠٢٤
received_images/٠١-يونيو-٢٠٢٤_6.jpg,٠١-يونيو-٢٠٢٤
```

### Saved Images
Images are saved in the `received_images` directory with filenames based on their metadata (e.g., `attributeId_assetId.jpg`).
