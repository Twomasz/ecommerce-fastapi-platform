from contextlib import asynccontextmanager

from fastapi import FastAPI

from ecommerce_project.db import Base, engine
from ecommerce_project.routers import orders, products, users


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Lifespan event handler that creates tables on startup and does nothing on shutdown.
    :param _: reference to the FastAPI app, required for lifespan event
    :return: None
    """
    # startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # run application
    # shutdown
    pass


app = FastAPI(lifespan=lifespan)

# include routers
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(users.router, prefix="/users", tags=["Users"])



# basic endpoints
@app.get("/")
def root():
    return {"message": "Welcome to the E-commerce platform!"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/favicon.ico")
async def favicon():
    """Handles default favicon request"""
    return {"path": "/static/favicon.ico"}


