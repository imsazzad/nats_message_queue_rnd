"""This module is a nat publisher file."""
import argparse
import asyncio
import sys

from nats.aio.client import Client as NATS

from app.nats_package import config


def show_usage():
    usage = """
nats-pub SUBJECT [-d DATA] [-s SERVER]
Example:
nats-pub hello -d world -s nats://127.0.0.1:4222 -s nats://127.0.0.1:4223
"""
    print(usage)


def show_usage_and_die():
    show_usage()
    sys.exit(1)


async def run(loop, msg = None):
    parser = argparse.ArgumentParser()

    # e.g. nats-pub hello -d "world" -s nats://127.0.0.1:4222 -s nats://127.0.0.1:4223
    parser.add_argument('subject', default=config.NAT_CONF["oos_msg_subj"], nargs='?')
    parser.add_argument('-d', '--data', default="oos happened")
    # parser.add_argument('-s', '--servers', default="192.168.0.106", action='append')
    parser.add_argument('-s', '--servers', default=config.NAT_CONF['message_q_ip2'], action='append')
    parser.add_argument('--creds', default="")
    args = parser.parse_args()

    nc = NATS()

    async def error_cb(e):
        print("Error:", e)

    async def closed_cb():
        print("Connection to NATS is closed.")

    async def reconnected_cb():
        print(f"Connected to NATS at {nc.connected_url.netloc}...")

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
    for i in range(1):
        data = args.data + str(i)
        if msg != None:
            data = msg.decode()
        await nc.publish(args.subject, data.encode())
        await nc.flush()
    await nc.close()


def run_event_loop():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run(loop))
    finally:
        loop.close()

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete(run(loop))
    # finally:
    #     loop.close()
    run_event_loop()

# python app/nats_package/nats_pub.py
#  python -m app.nats_package.nats_pub or export PYTHONPATH=. &&  python app/nats_package/nats_pub.py
# https://stackoverflow.com/questions/40304117/import-statement-works-on-pycharm-but-not-from-terminal
