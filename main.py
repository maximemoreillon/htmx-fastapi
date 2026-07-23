from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db import SessionDep, Fruit
from sqlmodel import select
from typing import Annotated

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=RedirectResponse)
async def index():
    return RedirectResponse(url="/fruits")


@app.post("/fruits")
async def create_fruit(
    fruit: Annotated[Fruit, Form()], session: SessionDep, request: Request
):
    session.add(fruit)
    session.commit()
    session.refresh(fruit)
    return templates.TemplateResponse(request=request, name="fruits/new/success.html")


@app.get("/fruits", response_class=HTMLResponse)
async def read_fruits(request: Request, session: SessionDep):
    fruits = session.exec(select(Fruit)).all()
    return templates.TemplateResponse(
        request=request, name="fruits/index.html", context={"fruits": fruits}
    )


@app.get("/fruits/new", response_class=HTMLResponse)
async def fruit_form(request: Request):
    return templates.TemplateResponse(request=request, name="fruits/new/index.html")


@app.get("/fruits/{id}", response_class=HTMLResponse)
async def read_fruit(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )
