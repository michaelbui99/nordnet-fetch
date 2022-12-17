from pathlib import Path
from os import path
from os import environ
from os import linesep


class NoEnvFileException(Exception):
    def __init__(self, message):
        super().__init__(message)
        print(message)


class DotEnv:
    def __init__(self):
        self.DEFAULT_PATH = str(Path(".env").resolve())

    def load(self, env_path: str = ""):
        if (not env_path):
            env_path = self.DEFAULT_PATH
        if (not path.exists(env_path)):
            raise NoEnvFileException(
                f"Failed to locate env file at {env_path}")

        with open(env_path, "r") as env:
            lines = env.readlines()
            for line in lines:
                arg, val = line.split("=")
                if (arg not in environ):
                    environ[arg] = val.strip(linesep)
