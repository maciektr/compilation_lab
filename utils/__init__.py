import sys

def stdout_print(*args):
    print(*args)

def stderr_print(*args):
    print(*args,file=sys.stderr)

def exit_fail(message: str=None):
    if message:
        stderr_print(message)
    sys.exit(1)

def exit_ok(message: str=None):
    if message:
        stderr_print(message)
    sys.exit(0)
