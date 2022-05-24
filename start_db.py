from app import db
import os

os.remove("database.db")
db.create_all()