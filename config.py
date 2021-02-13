import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://drtlrwvcgpljhf:362e08830fc1e52e765f9f5390e421e962ffd396b503a4037c73f6dc72210bd1@ec2-3-211-245-154.compute-1.amazonaws.com:5432/db0inen84vomcn'
