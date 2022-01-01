import time
from fastapi import FastAPI, Depends, HTTPException
import jwt
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from globals import description, tags_metadata
from schema import Item
from crud import (
    list_items,
    get_item_by_id,
    create_item_record,
    update_item_record,
    delete_item_record,
)
import models

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    """generated db connection object"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


security = HTTPBearer()

# global variable to store decoded token
PAYLOAD = {}


async def has_access(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Function that is used to validate the token in the case that it requires it
    """
    global PAYLOAD

    # grab the token
    token = credentials.credentials
    try:
        # decoding without using any key
        PAYLOAD = jwt.decode(
            token,
            key="secret",
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_iss": False,
            },
        )
        # checking if token has expired
        if int(time.time()) > PAYLOAD["exp"]:
            raise HTTPException(
                status_code=401, detail="Unauthorized, token has expired!"
            )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


PROTECTED = [Depends(has_access)]


app = FastAPI(
    title="Shopping Items Demo API",
    description=description,
    version="0.1",
    tags_metadata=tags_metadata,
    dependencies=PROTECTED,
)


# API ENDPOINTS #


@app.get(
    "/items/list/",
    tags=["items"],
    status_code=200,
    response_model=list[Item],
)
async def get_all(db: Session = Depends(get_db)):
    return list_items(db=db)


@app.post(
    "/items/create/",
    tags=["items"],
    status_code=201,
)
async def create_item(item: Item, db: Session = Depends(get_db)):
    return create_item_record(db=db, item=item.dict())


@app.get(
    "/items/get/{id}/",
    tags=["items"],
    status_code=200,
)
async def get_single_item(id: int, db: Session = Depends(get_db)):
    return get_item_by_id(db=db, id=id)


@app.post(
    "/items/update/{id}/",
    tags=["items"],
    status_code=202,
)
async def update_item(id: int, item: Item, db: Session = Depends(get_db)):
    return update_item_record(db=db, item=item.dict(), id=id)


@app.delete(
    "/items/delete/{id}/",
    tags=["items"],
    status_code=204,
)
async def delete_item(id: int, db: Session = Depends(get_db)):
    return delete_item_record(db=db, id=id)
