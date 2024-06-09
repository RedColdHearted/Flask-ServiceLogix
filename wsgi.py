import sys

from app import create_app

path = '/home/chiefbiefkief/Flask-ServiceLogix'
if path not in sys.path:
    sys.path.append(path)

application = create_app()
