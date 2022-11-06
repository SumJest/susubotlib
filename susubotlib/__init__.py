import os
import __main__
import logging
import stat
from susubotlib.pid import make_pid_file, async_make_pid_file

__version__ = "0.1.2"

main_file = os.path.basename(__main__.__file__)


def check_directory(path: str):
    listdir = os.listdir(path)
    bashes_path = f"{os.path.dirname(__file__)}/bashes/"

    if "run" not in listdir:
        with open(f"{bashes_path}/run", 'r') as original_file:
            with open(f"{path}/run", 'w') as created_file:
                created_file.write(original_file.read().replace("<MAIN_FILE>", main_file))
                created_file.close()
            original_file.close()
        st = os.stat(f"{path}/run")
        os.chmod(f"{path}/run", st.st_mode | stat.S_IEXEC)
        print(f"BotLib: Run file created attached to {main_file}")

    if "stop" not in listdir:
        with open(f"{bashes_path}/stop", 'r') as original_file:
            with open(f"{path}/stop", 'w') as created_file:
                created_file.write(original_file.read().replace("<MAIN_FILE>", main_file))
                created_file.close()
            original_file.close()
        st = os.stat(f"{path}/stop")
        os.chmod(f"{path}/stop", st.st_mode | stat.S_IEXEC)
        print(f"BotLib: Stop file created attached to {main_file}")


if main_file != "setup.py":
    check_directory(os.getcwd())
