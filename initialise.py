#!/usr/local/bin/python

import argparse

from models import init_db, drop_db


def create_all():
    init_db()


def delete_all():
    drop_db()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Build Database Tables")
    parser.add_argument("-d", "--drop", help="Drop all tables", required=False, dest="delete")

    args = parser.parse_args()

    if args.delete:
        delete_all()
    else:
        create_all()
