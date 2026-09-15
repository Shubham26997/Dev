from fastapi import APIRouter, HTTPException, Path, Query
from models import ToDos
from starlette import status
from database import SessionDep
from sqlmodel import select, delete
from utils import token_validate


router = APIRouter()

@router.post("/create_table", status_code= status.HTTP_201_CREATED)
async def create_todo_record(user: token_validate, todo_task: ToDos,db: SessionDep):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,\
                            detail="Authentication Error")
    print(user.get("id"))
    new_record = ToDos(**todo_task.model_dump(), owner_id=user.get('id'))
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.get("/get_tasks")
async def get_todo_tasks(user: token_validate, db: SessionDep):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,\
                            detail="Authentication Error")
    result = db.exec(select(ToDos).where(ToDos.owner_id == user.get('id'))).all()
    if result:
        return result
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="No records found in the db")

@router.get("/get_task/{task_id}")
async def get_todo_task_id(user: token_validate, db: SessionDep, task_id: int = Path(ge=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,\
                            detail="Authentication Error")
    if task_id:
        task = db.exec(select(ToDos).where(ToDos.id == task_id, ToDos.owner_id == user.get('id'))).first()
        if task:
            print(task)
            return task
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No task found with {task_id} id")
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task id is required")

@router.get("/get_task_priority/")
async def get_task_based_priority(user: token_validate, db: SessionDep, priority: int = Query(gt=0, le=5)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,\
                            detail="Authentication Error")
    if priority:
        task = db.exec(select(ToDos).where(ToDos.priority==priority,\
                                        ToDos.owner_id == user.get('id'))).fetchall()
        if task:
            # print(task)
            return task
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No task found with {priority} as priority")
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide the priority")

@router.put("/update_task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_task(user: token_validate, updated_task: ToDos, db: SessionDep, task_id: int=Path(ge=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,\
                            detail="Authentication Error")
    if task_id:
        task = db.exec(select(ToDos).where(ToDos.id == task_id,\
                                        ToDos.owner_id == user.get('id'))).first()
        if task:
            # task.completed = updated_task.completed
            # task.description = updated_task.description
            # task.priority = updated_task.priority
            task = updated_task
            db.add(task)
            db.commit()
            db.refresh(task)
            return task
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No task found with {task_id} id")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide the task id")

@router.delete("/delete_task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(user: token_validate, db: SessionDep, task_id: int=Path(ge=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,\
                            detail="Authentication Error")
    if task_id:
        task = db.exec(select(ToDos).where(ToDos.id == task_id, \
                                        ToDos.owner_id == user.get('id'))).first()
        if task:
            # task.completed = updated_task.completed
            # task.description = updated_task.description
            # task.priority = updated_task.priority
            db.exec(delete(ToDos).where(ToDos.id == task_id))
            db.commit()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No task found with {task_id} id")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide the task id")