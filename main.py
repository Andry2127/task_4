from typing import Optional, List, Union

from fastapi import FastAPI, HTTPException, status
import uvicorn
from pydantic import BaseModel


from tasks import do_task

app = FastAPI()


class TasksModel(BaseModel):
    id: int
    name: str
    difficult: Optional[float] = None 
    

@app.get("/tasks/{task_id}/", response_model=TasksModel,  status_code=status.HTTP_200_OK)
async def get_task(task_id: int):
    task = [task for task in do_task if task.get("id") == task_id]
    if task:
        return task[0]
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@app.get("/tasks/", response_model=List[TasksModel], status_code=status.HTTP_200_OK)
async def get_task():
    return do_task

@app.post("/tasks/", status_code=status.HTTP_201_CREATED)
async def create_task(task: TasksModel):
    do_task.append(task.model_dump())
    return dict(msg="Стврено.")


@app.put("/tasks/{task_id}/", response_model = TasksModel, status_code=status.HTTP_202_ACCEPTED)
async def update_taskd(task_id: int, taskmod: TasksModel):
    for task in do_task:
        if task.get("id") == task_id:
            task["id"] = taskmod.model_dump()["id"]
            task["name"] = taskmod.model_dump()["name"]
            task["difficult"] = taskmod.model_dump()["difficult"]
            return task


@app.patch("/tasks/{param}/{tasks_id}/", status_code=status.HTTP_202_ACCEPTED)
async def update_task(param: str, task_id: int, value: Union[str, int, float]):
    for tasktaskuct in do_task:
        if tasktaskuct.get("id") == task_id:
            if param in tasktaskuct:
                tasktaskuct[param] = value
                return
            else:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Param invalid")


@app.delete("/tasks/",status_code=status.HTTP_200_OK)
async def delete_task(task:TasksModel):
    do_task.remove(task.dict())
    return dict(msg = "Видалено" )


@app.delete("/tasks/{task_id}/", response_model=TasksModel, status_code=status.HTTP_200_OK)
async def delete_task(task_id: int):
    task = next((task for task in do_task if task["id"] == task_id), None)
    if task:
        do_task.remove(task) 
        return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8001)








