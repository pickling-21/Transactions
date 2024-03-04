import redis
import argparse
import json
import time
import logging

logging.basicConfig(level=logging.INFO)


def parse_bad_accounts():
    parser = argparse.ArgumentParser(
        description='Process some bad guys accounts.')
    parser.add_argument('-e',
                        help='<Required> Bad Guys Accounts separated by commas (length of number must be 10). Example "-e 7134456234,3476371234"', required=True)
    args = parser.parse_args()
    bad_accounts = []
    for item in args.e.split(','):
        if len(item) == 10:
            bad_accounts.append(int(item))
        else:
            parser.error("Wrong number lenght (must be 10)")
    return bad_accounts


def hack_message(message: str, bad_accounts: list) -> str:
    data = json.loads(message)

    if data["amount"] > 0 and data["metadata"]["to"] in bad_accounts:  # if reciever is bad guy
        data["metadata"]["to"], data["metadata"]["from"] = data["metadata"]["from"], data["metadata"]["to"]
        # swap sender and reciver

    return json.dumps(data)


if __name__ == "__main__":
    bad_accounts = parse_bad_accounts()

    r = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )

    # pubsub() the waki taki that listens for incomming messages
    mobile = r.pubsub()

    mobile.subscribe('transactions')

    # get_message() better then listen
    while True:
        message = mobile.get_message()
        if message and message['type'] == 'message':
            logging.info(hack_message(message["data"], bad_accounts))
            time.sleep(0.01)


# 1 терминал -
# redis-server

# 2 терминал -
# python producer.py

# 3 терминал -
# python consumer.py -e 1111111111,2222222222