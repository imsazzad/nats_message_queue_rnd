"""This module is a nat consumer file."""
import argparse
import asyncio
import logging
import signal
import sys

from nats.aio.client import Client as NATS

from app.nats_package import config
from app.nats_package.nats_exception import NatsException

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


"""
nats-sub SUBJECT [-s SERVER] [-q QUEUE]
Example:
nats-sub help -q workers -s nats://127.0.0.1:4222 -s nats://127.0.0.1:4223
"""


def show_usage():
    usage = """
nats-sub SUBJECT [-s SERVER] [-q QUEUE]
Example:
nats-sub help -q workers -s nats://127.0.0.1:4222 -s nats://127.0.0.1:4223
"""
    print(usage)


def show_usage_and_die():
    show_usage()
    sys.exit(1)


async def run(loop):
    parser = argparse.ArgumentParser()

    # e.g. nats-sub hello -s nats://127.0.0.1:4222
    parser.add_argument('subject', default=config.NAT_CONF["message_subject"], nargs='?')
    # parser.add_argument('-s', '--servers', default="192.168.0.106", action='append')
    parser.add_argument('-s', '--servers', default=config.NAT_CONF['message_q_ip'], action='append')
    # parser.add_argument('-s', '--servers', default=config.NAT_CONF['message_servers'], action='append')
    parser.add_argument('-q', '--queue', default=config.NAT_CONF["queue_group_name"])
    parser.add_argument('--creds', default="")
    args = parser.parse_args()

    nc = NATS()

    async def error_cb(e):
        print("Error:", e)
        logging.error(e)
        raise NatsException("Got Exception from nats.io service") from e

    async def closed_cb():
        print("Connection to NATS is closed.")
        logging.info("Connection to NATS is closed.")
        await asyncio.sleep(0.1, loop=loop)
        loop.stop()

    async def reconnected_cb():
        print(f"Connected to NATS at {nc.connected_url.netloc}...")
        logging.info(f"Connected to NATS at {nc.connected_url.netloc}...")

    async def subscribe_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()

        logging.info("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

        from app.nats_rnd.OOS_Prodcuer_PS import run as run_p
        current_loop = asyncio.get_event_loop()
        # print(current_loop.getnameinfo())
        # current_loop.run_until_complete(run_p(current_loop))
        current_loop.create_task(run_p(current_loop))

    options = {
        "loop": loop,
        "error_cb": error_cb,
        "closed_cb": closed_cb,
        "reconnected_cb": reconnected_cb
    }

    if len(args.creds) > 0:
        options["user_credentials"] = args.creds

    try:
        if len(args.servers) > 0:
            options['servers'] = args.servers

        await nc.connect(**options)
    except Exception as e:
        print(e)
        show_usage_and_die()

    print(f"Connected to NATS at {nc.connected_url.netloc}...")
    logging.info(f"Connected to NATS at {nc.connected_url.netloc}...")

    def signal_handler():
        if nc.is_closed:
            return
        print("Disconnecting...")
        logging.warning("Disconnecting...")
        loop.create_task(nc.close())

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)

    await nc.subscribe(args.subject, args.queue, subscribe_handler)


def run_subscriber():
    print(" nats subscriber opens successfully. \n")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()


if __name__ == '__main__':
    try:
        run_subscriber()
    except NatsException as e:
        logging.error(e)
    else:
        logging.info(" This will execute if server stops and exception not happened")
    finally:
        logging.info("same as java finally")

# python app/nats_package/nats_sub.py
