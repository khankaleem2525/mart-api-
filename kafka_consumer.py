from kafka import KafkaConsumer
import json

def get_kafka_consumer(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    return consumer

def consume_messages(topic):
    consumer = get_kafka_consumer(topic)
    try:
        for message in consumer:
            print(f"Received message: {message.value}")
    except KeyboardInterrupt:
        print("Consumer stopped by user.")
    except Exception as e:
        print(f"Error while consuming messages: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages('your_topic')  # Replace 'your_topic' with the actual topic name
