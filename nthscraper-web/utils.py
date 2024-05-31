import psutil
import datetime as dt


def log_ram_usage():
    with open("log_ram.txt", "a+") as f:
        f.write(f"RAM USAGE {dt.datetime.now()}: {psutil.virtual_memory().percent}%\n")


def log_cpu_usage():
    with open("log_cram.txt", "a+") as f:
        f.write(f"CPU USAGE {dt.datetime.now()}: {psutil.cpu_percent()}%\n")


def print_message(message):
    print("Message:", message)
