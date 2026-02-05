import argparse
from task_service.service import task_service

def main():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest="cmd")

    add = subs.add_parser("add")
    add.add_argument("title")
    

    subs.add_parser("list")

    done = subs.add_parser("done")
    done.add_argument("id", type = int)

    args = parser.parse_args()

    try:
        if args.cmd == "add":
            task = task_service.create_task(args.title)
            print(f"Created: {task.id}")
        
        elif args.cmd == "list":
            tasks = task_service.list_tasks()
            for task in tasks:
                status = "Done" if task.done == True else "Pending"
                print(f"{task.id} [{status}] {task.title}")

        elif args.cmd == "done":
            task_done = task_service.mark_done(args.id)
            if task_done:
                print(f"Task {task_done.title} with ID {task_done.id} is done.")
            else:
                print("Task not found.")

        else:
            parser.print_help()

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
