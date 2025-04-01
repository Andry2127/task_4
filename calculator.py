from fastapi import FastAPI, Query
from typing import List
import uvicorn

app = FastAPI()



@app.get("/calculator/")
async def calc(action: str = Query(), num1: float = Query(), num2: float = Query()):
    if action == "add":
        result = num1 + num2
    elif action == "subtrack":
        result = num1 - num2
    elif action == "square":
        result = [num1 **2, num2 **2]
    
    return dict(result=result)


@app.get("/calc/{action}/{num1}/{num2}")
async def calc1(action: str, num1: float, num2: float, name: str):
    if action == "add":
        result = num1 + num2
    elif action == "subtrack":
        result = num1 - num2
    elif action == "square":
        result = [num1 **2, num2 **2]
    
    return dict(result=result)    

if __name__ == "__main__":
    uvicorn.run("calculator:app")