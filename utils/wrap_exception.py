from fastapi import HTTPException
from colorama import init, Fore


init(autoreset=True)


def wrap_except(func):
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            err = str(err)
            print(Fore.RED+'ERROR:    ' + err)
            return {'error': err}
    return wrap
