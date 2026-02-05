from pathlib import Path
import json
from task_service.domain.task import Task
from dataclasses import asdict

BASE_DIR = Path(__file__).resolve().parent.parent
TASK_FILE = BASE_DIR / "storage" / "tasks.jsonl"
TEMP = BASE_DIR / "storage" / "tasks.tmp"

TASK_FILE.parent.mkdir(parents=True, exist_ok=True)



def get_all() -> list[Task]:
    if not TASK_FILE.exists():
        return []
    tasks = []
    with TASK_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            tasks.append(Task(**json.loads(line)))
    return tasks

def add(task: Task):
    with TASK_FILE.open("a", encoding = "utf-8") as f:
        f.write(json.dumps(asdict(task)) + "\n")


def update(task: Task):
    with TASK_FILE.open("r", encoding = "utf-8") as src, TEMP.open("w", encoding="utf-8") as tmp:
        for line in src:
            task_i = json.loads(line)
            if task_i["id"] == task.id:
                tmp.write(json.dumps(asdict(task)) + "\n")
            else:
                tmp.write(json.dumps(task_i) + "\n")
    TEMP.replace(TASK_FILE)

            