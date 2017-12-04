import traceback

def print_exception(msg):
    print(msg + " - " + traceback.format_exc())

