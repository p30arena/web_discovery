import argparse
from peewee_migrate import Router
from models import db

router = Router(db, migrate_dir='ig_vendor_py/migrations')

parser = argparse.ArgumentParser(description='Peewee migrations manager')
parser.add_argument('action', choices=['create', 'migrate'], help='Action to perform')
parser.add_argument('name', nargs='?', help='Migration name')
args = parser.parse_args()

if args.action == 'create':
    if not args.name:
        parser.error('Migration name is required for create action')
    router.create(args.name)
elif args.action == 'migrate':
    if args.name:
        router.run(args.name)
    else:
        router.run()
