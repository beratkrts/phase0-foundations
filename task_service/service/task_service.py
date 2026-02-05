from task_service.domain.task import Task
from task_service.repository import file_repo

def next_id() -> int:
    tasks = file_repo.get_all()
    if not tasks:
        return 10000
    max_id = max(task.id for task in tasks)
    return max_id + 1

def create_task(title: str) -> Task:
    """
    Create task with new id and persist it.
    """
    if not title:
        raise ValueError
    task = Task(next_id(), title)
    file_repo.add(task)
    return task


def list_tasks() -> list[Task]:
    """
    Return all tasks.
    """
    return file_repo.get_all()

def mark_done(task_id: int) -> Task:
    """
    Mark task done. Return True if found.
    """
    tasks = file_repo.get_all()
    for task in tasks:
        if task_id == task.id:
            task.done = True
            file_repo.update(task)
            return task
    
    return None