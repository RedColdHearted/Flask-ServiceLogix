import sys
# The "/home/chiefbiefkief" below specifies your home
# directory -- the rest should be the directory you uploaded your Flask
# code to underneath the home directory.  So if you just ran
# "git clone git@github.com/myusername/myproject.git"
# ...or uploaded files to the directory "myproject", then you should
# specify "/home/chiefbiefkief/myproject"
path = '/home/chiefbiefkief/Flask-ServiceLogix'
if path not in sys.path:
    sys.path.append(path)

from app import create_app
application = create_app()
