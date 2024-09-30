from kafka import KafkaProducer
import json

def get_kafka_producer():
    producer = KafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer

def send_message(topic, message):
    producer = get_kafka_producer()
    try:
        producer.send(topic, value=message)  # Ensure message is sent as value
        producer.flush()
        print(f"Sent message to {topic}: {message}")
    except Exception as e:
        print(f"Error sending message to {topic}: {e}")
    finally:
        producer.close()

if __name__ == "__main__":
    # Example usage
    topic = 'your_topic'  # Replace with your topic name
    message = {"key": "value"}  # Replace with your message
    send_message(topic, message)
