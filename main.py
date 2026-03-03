from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from . import models, schemas, database, crud, utils

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Address Book API")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/addresses", response_model=schemas.AddressResponse)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    logger.info("Creating new address")
    return crud.create_address(db, address)


@app.get("/addresses", response_model=list[schemas.AddressResponse])
def get_all_addresses(db: Session = Depends(get_db)):
    return crud.get_addresses(db)


@app.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    address = crud.delete_address(db, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted successfully"}


@app.get("/addresses/nearby/")
def get_nearby_addresses(
    latitude: float,
    longitude: float,
    distance_km: float,
    db: Session = Depends(get_db)
):
    addresses = crud.get_addresses(db)
    nearby = []

    for addr in addresses:
        dist = utils.calculate_distance(
            latitude, longitude, addr.latitude, addr.longitude
        )
        if dist <= distance_km:
            nearby.append(addr)

    return nearby