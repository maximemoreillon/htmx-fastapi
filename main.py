from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from db import SessionDep, Fruit, create_db_and_tables
from sqlmodel import select
from typing import Annotated

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=RedirectResponse)
async def index():
    return RedirectResponse(url="/fruits")


@app.post("/fruits", response_class=HTMLResponse)
async def create_fruit(
    fruit: Annotated[Fruit, Form()], session: SessionDep, request: Request
):
    session.add(fruit)
    session.commit()
    session.refresh(fruit)
    return templates.TemplateResponse(
        request=request, name="partials/fruit.html", context={"fruit": fruit}
    )


@app.get("/fruits", response_class=HTMLResponse)
async def read_fruits(request: Request, session: SessionDep):
    fruits = session.exec(select(Fruit)).all()
    return templates.TemplateResponse(
        request=request, name="fruits/index.html", context={"fruits": fruits}
    )


@app.delete("/fruits/{id}", response_class=HTMLResponse)
async def delete_fruit(session: SessionDep, id: int):
    fruit = session.get(Fruit, id)
    if not fruit:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(fruit)
    session.commit()
    return ""


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
