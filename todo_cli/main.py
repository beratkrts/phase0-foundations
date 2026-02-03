import argparse
import json
from pathlib import Path
from dataclasses import dataclass, asdict


TASK_FILE = Path("tasks.jsonl")
TEMP_FILE = Path("tasks.tmp")

@dataclass
class Task:
    id: int
    title: str
    done: bool = False


def next_id():
    """
    Returns the last task's id in tasks.jsonl by incrementing 1
    """
    if not TASK_FILE.exists():
        return 10000
    with TASK_FILE.open("r", encoding="utf-8") as f:
        last = None
        for line in f:
            last = json.loads(line)
    
    return last["id"] + 1

def load_tasks():
    """
    Read tasks.jsonl and return list.
    If file does not exist, return empty list.
    """
    tasks_list = []
    if not TASK_FILE.exists():
        return []
    
    with TASK_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            tasks_list.append(Task(**json.loads(line)))
    return tasks_list
    

def add_task(title: str):
    """
    Add new task with done = False
    
    :param title: Task name
    :type title: str
    """
    task = Task(next_id(), title)
    with TASK_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(task)) + "\n")
    
def list_tasks():
    """
    Print all tasks with index + status
    """
    tasks_list = load_tasks()
    if len(tasks_list) == 0:
        print("There is no tasks list.")
    for task in tasks_list:
        task_dict = asdict(task)
        print(f"Task ID: {task_dict['id']}, Task Title: {task_dict['title']}, Status: {'Done' if task_dict['done'] else 'Pending'}")

def done_task(task_id: int):
    """
    Mark given task as done
    :param task_id: Description
    :type task_id: int
    """
    if not TASK_FILE.exists():
        print("Could not find 'tasks.jsonl'")
        return

    found = False

    with TASK_FILE.open("r", encoding="utf-8") as src, TEMP_FILE.open("w", encoding="utf-8") as dst:
        for line in src:
            task = json.loads(line)
            if task["id"] == task_id:
                found = True
                task["done"] = True
            dst.write(json.dumps(task, ensure_ascii=False) + "\n")
    TEMP_FILE.replace(TASK_FILE)

    if not found:
        print("Task not found")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    #add
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("title")

    #list
    list_parser = subparsers.add_parser("list")

    #done
    done_parser = subparsers.add_parser("done")
    done_parser.add_argument("id", type=int)


    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title)

    elif args.command == "list":
        list_tasks()

    elif args.command == "done":
        done_task(args.id)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()