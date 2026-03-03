from sqlalchemy.orm import Session
from . import models

def create_address(db: Session, address):
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_addresses(db: Session):
    return db.query(models.Address).all()

def get_address(db: Session, address_id: int):
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def delete_address(db: Session, address_id: int):
    address = get_address(db, address_id)
    if address:
        db.delete(address)
        db.commit()
    return address