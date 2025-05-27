from fastapi import FastAPI
from drivers.routers import conversation as conversation_router

app = FastAPI()


# include routers
app.include_router(conversation_router.router)

# add middlewares

# add health checks



@app.get("/")
async def root():
    return {"message": "Hello World"}