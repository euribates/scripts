#!/usr/bin/env python3

import argparse

import settings
import locallib
import saslib

OK = '\033[0;32m[Ok]\033[0m'

def bold(text: str) -> str:
    return f'\033[1m{text}\033[0m'



def get_options() -> {}:
    parser = argparse.ArgumentParser(prog="alta-usuario-sas-viya")
    parser.add_argument('group', help='El nombre del grupo al que pertence')
    parser.add_argument('username', help="El login del usuario a incoporar")
    parser.add_argument('-v', '--verbose', action='store_true')
    opts = parser.parse_args()
    print(opts)
    if opts.verbose:
        settings.is_tron(True)
    gid = locallib.get_gid(opts.group)
    if not gid:
        raise ValueError(
            f'El nombre de grupo indicado: [{opts.group}]'
            ' no existe.'
            )
    uid = locallib.get_uid(opts.username)
    return {
        'username': opts.username,
        'uid': uid,
        'group': opts.group,
        'gid': gid,
        'verbose': opts.verbose,
        }


def main():
    opt = get_options()
    username = opt['username']
    group = opt['group']
    uid = opt['uid']
    gid = opt['gid']
    if uid:
        if settings.is_tron():
            print(f'El usuario {bold(username)} ya existe localmente con uid {uid}.', OK)
    else: 
        if settings.is_tron():
            print(f'El usuario {bold(username)} no existe localmente, lo crearemos.')
            print(
                f'Dando de alta al usuario {username} (uid por determinar)'
                f' en el grupo {group} (gid: {gid})'
                )
        last_uid = locallib.get_last_user_id()
        uid = last_uid + 1
        if settings.is_tron():
            print(f"Ultimo id es {last_uid}, el siguiente es {uid}")
            print("Creando el usuario local")
        locallib.create_local_user(username, uid, gid)
        if settings.is_tron():
            print(OK)
    saslib.sas_init()
    saslib.sas_update_user(username, uid, gid)
    if settings.is_tron():
        print(
            f"Creado el usuario {username} con uid: {uid}"
            f" en el grupo {group} con gid: {gid}"
            )


if __name__ == '__main__':
    main()
