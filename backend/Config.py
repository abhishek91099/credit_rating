
from flask_sqlalchemy import SQLAlchemy
import urllib.parse
db=SQLAlchemy()
DB_USERNAME = "root"
DB_PASSWORD = urllib.parse.quote_plus("root@123")  # URL encode the password
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "credit_rating"

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT =  '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE ='app.log'