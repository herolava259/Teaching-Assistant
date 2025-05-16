from fastapi import FastAPI

app = FastAPI()


# include routers

# add middlewares

# add health checks 

@app.get("/")
async def root():
    return {"message": "Hello World"}