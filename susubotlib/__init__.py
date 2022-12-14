import os
import __main__
import logging
import stat
from susubotlib.pid import make_pid_file, async_make_pid_file

__version__ = "0.1.2"

main_file = os.path.basename(__main__.__file__)
base_dir = os.path.dirname(__main__.__file__)


def check_directory(path: str):
    listdir = os.listdir(path)
    bashes_path = os.path.join(os.path.dirname(__file__), 'bashes')

    if "run" not in listdir:
        with open(os.path.join(bashes_path, 'run'), 'r') as original_file:
            with open(os.path.join(path, 'run'), 'w') as created_file:
                created_file.write(original_file.read().replace("<MAIN_FILE>", main_file))
                created_file.close()
            original_file.close()
        st = os.stat(os.path.join(path, 'run'))
        os.chmod(os.path.join(path, 'run'), st.st_mode | stat.S_IEXEC)
        print(f"BotLib: Run file created attached to {main_file}")

    if "stop" not in listdir:
        with open(os.path.join(bashes_path, 'stop'), 'r') as original_file:
            with open(os.path.join(path, 'stop'), 'w') as created_file:
                created_file.write(original_file.read().replace("<MAIN_FILE>", main_file))
                created_file.close()
            original_file.close()
        st = os.stat(os.path.join(path, 'stop'))
        os.chmod(os.path.join(path, 'stop'), st.st_mode | stat.S_IEXEC)
        print(f"BotLib: Stop file created attached to {main_file}")

    if 'susubotlib.ini' not in listdir:
        with open(os.path.join(os.path.dirname(__file__), 'susubotlib.ini'), 'r') as original_file:
            with open(os.path.join(path, 'susubotlib.ini'), 'w') as created_file:
                created_file.write(original_file.read())
                created_file.close()
            original_file.close()
        print(f"BotLib: Config file created")

    if 'keyboards' not in listdir:
        os.mkdir(os.path.join(path, 'keyboards'))
    if 'messages' not in listdir:
        os.mkdir(os.path.join(path, 'messages'))


if main_file != "setup.py":
    check_directory(os.getcwd())
