import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://vbwccsquyasyen:f82af006421a30f5060dd692b9b5b464a92d989890a9dabd192342a3fb977e75@ec2-34-230-167-186.compute-1.amazonaws.com:5432/d2450biv42t6po'
