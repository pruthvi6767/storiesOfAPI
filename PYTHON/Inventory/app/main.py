from fastapi import FastAPI, Depends, Form, Path
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import items
import uuid
import uvicorn
from db import items as itemdDb

itemdDb.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Application", description="",
              template_directory="templates", version="1.0.0")

templates = Jinja2Templates(directory='templates')

item1 = itemdDb.Item(name='Apple', quantity=0, uuid=str(uuid.uuid4()))
item2 = itemdDb.Item(name='Banana', quantity=0, uuid=str(uuid.uuid4()))
item3 = itemdDb.Item(name='Mango', quantity=0, uuid=str(uuid.uuid4()))
item4 = itemdDb.Item(name='Kiwi', quantity=0, uuid=str(uuid.uuid4()))
item5 = itemdDb.Item(name='Peaches',  quantity=0, uuid=str(uuid.uuid4()))
item6 = itemdDb.Item(name='Grapes', quantity=0, uuid=str(uuid.uuid4()))


# Create DB Session
def get_db():
    """
    builds db session
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# database seed
catalog = ['Apple', 'Banana', 'Mango', 'Kiwi', 'Peaches', 'Grapes']


def build_items(name: str) -> itemdDb.Item:
    """
    creates seed items
    """
    return itemdDb.Item(name=name, quantity=0, uuid=str(uuid.uuid4()))


catalog = list(map(build_items, catalog))


def create_items(db: Session):
    """
    inserts seed into db
    """
    db.begin()
    for item in catalog:
        db.add(item)
    db.commit()


app.debug = True
@app.get("/index")
async def render_index(request: Request, db: Session = Depends(get_db), limit: int = 10):
    """
    index page that renders all items and quantities
    """
    try:
        print('begin')
        all_items = items.get_all_items(db)
        if not all_items:
            create_items(db)
            print(all_items)
            print("end")
        all_items = items.get_all_items(db)
        print(all_items)
    except Exception as e:
        print(e)
        return templates.TemplateResponse("500.html", {"request": request})
    finally:
        db.close()
    return templates.TemplateResponse("index.html", {"request": request, "items": all_items, 'error': 'hidden'})


@app.post("/index")
def update_item(request: Request, db: Session = Depends(get_db), id: int = Form(..., ge=0), quantity: int = Form(..., ge=0)):
    """
    updates items from url encode params and re-renders index page
    """
    print(id, quantity)
    all_items = items.get_all_items(db)
    message = ''
    try:
        if len(all_items) < id:
            message = "Failed"
            return templates.TemplateResponse("index.html", {'request': request, "message": message, "items": all_items, 'error': ''})

        if items.update_item_by_id(db, id, quantity):
            message = 'successfully updated!'
            all_items = items.get_all_items(db)
    except:
        return templates.TemplateResponse("500.html", {"request": request})
    return templates.TemplateResponse("index.html", {"request": request, "message": message, "items": all_items, "error": "hidden"})


@app.get("/")
def about(request: Request):
    """
    app root page
    """
    return templates.TemplateResponse("500.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0',
                debug=True, reload=True)
