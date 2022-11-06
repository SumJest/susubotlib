import __main__
import os


def make_pid_file():
    with open(f"{os.path.dirname(__main__.__file__)}/bot.pid", "w") as file:
        file.write(str(os.getpid()))
        file.close()


async def async_make_pid_file():
    with open(f"{os.path.dirname(__main__.__file__)}/bot.pid", "w") as file:
        file.write(str(os.getpid()))
        file.close()


def test_function(some):
    print("lol")
    print(some)




