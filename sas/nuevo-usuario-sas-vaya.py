#!/usr/bin/env python3

import argparse

import settings
import locallib
import saslib


def get_options() -> {}:
    parser = argparse.ArgumentParser(prog="alta-usuario-sas-viya")
    parser.add_argument('username', help="El login del usuario a incoporar")
    parser.add_argument('group', help='El nombre del grupo al que pertence')
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
    if uid:
        raise ValueError(
            f'El usuario indicado: [{opts.username}] ya existe.'
            )
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
    if settings.is_tron():
        print(
             f'dando de alta al usuario {username}'
             f' en el grupo {group}'
             )
    uid = opt['uid']
    gid = opt['gid']
    last_uid = locallib.get_last_user_id()
    next_uid = last_uid + 1
    if settings.is_tron():
        print(f"Ultimo id es {last_uid}, el siguiente es {next_uid}")
    locallib.create_local_user(username, next_uid, gid)
    saslib.sas_init()
    saslib.sas_update_user(username, next_uid, gid)
    if settings.is_tron():
        print(
            f"Creado el usuario {username} con uid: {uid}"
            f" en el grupo {group} con gid: {gid}"
            )


if __name__ == '__main__':
    main()
