from sqlalchemy.orm import Session
from db.session import get_db
from app.models.customer import Customer
from utils.security import hash_password,