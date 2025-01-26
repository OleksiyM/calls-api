import os

commands = [
    "alembic upgrade head",
    "uvicorn main:app --host 0.0.0.0 --port 8080 --reload",
]


def run_command(command):
    print("Running command: {}".format(command))
    os.system(command)


for command in commands:
    run_command(command)
