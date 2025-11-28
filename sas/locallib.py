from typing import Optional
import subprocess

import settings

TRON = settings.TRON

OK = "\33[0;32m [OK] \33[0m"


def get_uid(name: str) -> Optional[int]:
    '''Obtener el id. del usuario a partir de su nombre.
    '''
    with open(settings.ETC_PASSWD, 'r') as file_input:
        for line in file_input:
             username, _pwd, uid, *rest = line.split(':')
             if username == name:
                 return int(uid)
    return None


def get_gid(name: str) -> Optional[int]:
    '''Obtener el id. del grupo a partir del nombre del grupo.
    '''
    with open(settings.ETC_GROUP, 'r') as file_input:
        for line in file_input:
             group_name, _pwd, gid, *_rest = line.split(':')
             if group_name == name:
                 return int(gid)
    return None


def get_last_user_id() -> int:
    uids = []
    with open(settings.ETC_PASSWD, 'r') as file_input:
        for line in file_input:
             username, _pwd, uid, *rest = line.split(':')
             if username == 'nobody':
                 continue
             uids.append(int(uid))
    return max(uids)


def get_last_group_id() -> int:
    gids = []
    with open(settings.ETC_GROUP, 'r') as file_input:
        for line in file_input:
             groupname, _pwd, gid, *rest = line.split(':')
             gids.append(int(gid))
    return max(gids)


def execute(*cmds):
    if TRON:
        print(*cmds, end="...")
    # subprocess.check_call(cmds)
    if TRON:
        print(OK)


def create_local_user(username, uid, gid):
    if TRON:
        print(f"Creamos el usuario {username}, con uid {uid} y gid {gid}")
    execute(
        "/usr/sbin/useradd",
        "--base-dir",
        f"/home/{username}",
        "--gid",
        str(gid),
        "--create-home",
        "--shell",
        "/sbin/nologin",
        "--uid",
        str(uid),
        username,
        )


def create_local_group(gid: int, name: str):
    if TRON:
        print(f"Creamos el grupo local {name} con gid {gid}")
    execute(
        'groupadd',
        '--gid',
        str(gid),
        name
        )
