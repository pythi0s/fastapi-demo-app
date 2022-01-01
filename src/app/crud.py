from fastapi import HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session
from models import Item


def list_items(db: Session, skip: int = 0, limit: int = 100):
    """list all item table records

    Args:
        db (Session): db connection
        skip (int, optional): [description]. Defaults to 0.
        limit (int, optional): [description]. Defaults to 100.

    Returns:
        [list]: all records of item table
    """
    return db.query(Item).offset(skip).limit(limit).all()


def get_item_by_id(db: Session, id: int):
    """get item record by id

    Args:
        db (Session): db connection
        id (int): id of existing item

    Returns:
        [dict]: item data
    """
    return db.query(Item).filter(Item.id == id).first()


def create_item_record(db: Session, item: dict):
    """create a new record for an item

    Args:
        db (Session): db connection
        item (dict): item data dictionary

    Raises:
        HTTPException: in case of exceptions raised

    Returns:
        int: file id of created record
    """
    try:
        row = Item(**item)
        # add object to db and refresh
        db.add(row)
        db.commit()
        db.refresh(row)
        return {"id": row.id, "detail": "item inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def update_item_record(db: Session, item: dict, id: int):
    """update existing record of publish table

    Args:
        db (Session): db connection
        item (dict): item dictionary
        id (int): id of existing item

    Raises:
        HTTPException: in case of exceptions raised

    Returns:
        [dict]: response
    """
    try:
        row = db.query(Item).filter(Item.id == id).first()
        if row is None:
            raise HTTPException(status_code=404, detail="item not found")
        row.category = item["category"]
        row.description = item["description"]
        row.manufacturer = item["manufacturer"]
        row.name = item["name"]
        row.price = item["price"]
        row.timestamp = item["timestamp"]
        db.add(row)
        db.commit()
        db.refresh(row)
        return {"detail": "item updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def delete_item_record(db: Session, id: int):
    """delete published policy record by id

    Args:
        db (Session): db connection
        id (int): id of existing item to be deleted

    Raises:
        HTTPException: in case of exceptions raised

    Returns:
        [dict]: response
    """
    row = db.query(Item).filter(Item.id == id).first()
    if not row:
        raise HTTPException(status_code=404, detail="item not found")
    else:
        db.delete(row)
        db.commit()
        return {"detail": "item deleted successfully"}
