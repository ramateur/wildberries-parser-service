import json

from confluent_kafka import Consumer, KafkaError

from src.config import settings
from src.logging import setup_file_logger
from src.parser.parser import WildberriesParser


def consume_kafka_messages(broker: str, group_id: str, topic: str):
    consumer = Consumer({'bootstrap.servers': broker, 'group.id': group_id, 'auto.offset.reset': 'earliest'})

    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)  # Timeout of 1 second

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            message = msg.value().decode('utf-8')
            process_message(message)

    finally:
        consumer.close()


def process_message(message):
    try:
        data = json.loads(message)
        category_link = data['category_link']
        pages_count = data.get('pages_count', 1)
        offset_page = data.get('offset_page', 1)

        # setup logging
        setup_file_logger()

        ozon_parser = WildberriesParser()
        ozon_parser.parse_category(category_link=category_link, pages_count=pages_count, offset_page=offset_page)
    except json.JSONDecodeError:
        print('Invalid JSON message received')


def main():
    consume_kafka_messages(settings.KAFKA_BROKER, settings.KAFKA_GROUP_ID, settings.KAFKA_TOPIC)


if __name__ == '__main__':
    main()
