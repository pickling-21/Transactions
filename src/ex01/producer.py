import redis
import json
import random
import time
import logging

logging.basicConfig(level=logging.INFO)


def get_account() -> int:
    # return random.randrange(pow(10, 9), pow(10, 10)-1)
    return int(str(random.randint(1, 9)) * 10)


def create_json() -> str:
    receiver = get_account()
    sender = get_account()
    amount = random.randrange(-100000, 100000)
    transaction = {
        "metadata": {
            "from": sender,
            "to": receiver
        },
        "amount": amount
    }
    return json.dumps(transaction)


if __name__ == "__main__":
    # initializing the redis instance
    r = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True  # <-- this will ensure that binary data is decoded
    )

    while True:
        message = create_json()
        r.publish("transactions", message)
        logging.info(message)
        time.sleep(1)

    # tests = [{"metadata": {"from": 1111111111, "to": 2222222222}, "amount": 10000},
    #          {"metadata": {"from": 1111111111, "to": 4444444444}, "amount": -3000},
    #          {"metadata": {"from": 2222222222, "to": 5555555555}, "amount": 5000}]

    # for test in tests:
    #     message = json.dumps(test)
    #     r.publish("transactions", message)
    #     print(message)
    #     time.sleep(1)

    # Additional points can be earned if the code uses builtin logging module (instead of print function) to write produced messages to stdout for manual testing.
