#!/usr/bin/env python3

import subprocess
from pathlib import Path
import argparse

PASSWD: str = Path("/etc/passwd")
DEFAULT_GROUP: int = 1004


def get_options() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="alta-usuario-sas-viya")
    parser.add_argument('username')
    return parser.parse_args()


def leer_ultimas_ids() -> tuple[int, int]:
    ids = []
    with open(PASSWD, 'r') as file_input:
        for line in file_input:
             username, _pwd, uid, gid, *rest = line.split(':')
             if username == 'nobody':
                 continue
             ids.append((int(uid), int(gid)))
    return max(ids)


def crear_usuario_local(gid, uid, username):
    print(f"Creamos el usuario {username}, con uid {uid} y gid {gid}")
    cmds = [
        "/usr/sbin/useradd",
        "-d",
        f"/home/{username}",
        "-g",
        str(gid),
        "-m",
        "-s",
        "/sbin/nologin",
        "-u",
        str(uid),
        username,
        ]
    print(*cmds, end="...")
    subprocess.check_call(cmds)
    print("\33[0;32m [OK] \33[0m")

def comprobar_token() -> bool:
    pass

def main():
    opt = get_options()
    last_uid, _gid = leer_ultimas_ids()
    next_uid = last_uid + 1
    print(f"Ultimo id es {last_uid}, el siguiente es {next_uid}")
    crear_usuario_local(DEFAULT_GROUP, next_uid, opt.username)


if __name__ == '__main__':
    main()
