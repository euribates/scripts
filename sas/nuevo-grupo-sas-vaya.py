#!/usr/bin/env python3


import argparse

import settings
import locallib
import saslib


def get_options() -> {}:
    parser = argparse.ArgumentParser(prog="nuevo-grupo-sas-viya")
    parser.add_argument('group', help_text='El nombre del grupo que quiere crear')
    parser.add_argument('-v', '--verbose', action='store_false')
    opts = parser.parse_args()
    if opts.verbose:
        settings.is_tron(True)
    gid = locallib.get_gid(opts.group)
    if gid:
        raise ValueError(
            f'El grupo indicado: [{opts.group}]'
            ' ya existe.'
            )
    return {
        'group': opts.group,
        'verbose': opts.verbose,
        }


def main():
    opt = get_options()
    group = opt['group']
    last_gid = locallib.get_last_group_id()
    next_gid = last_gid + 1
    if settings.is_tron():
        print(f"Ultimo gid es {last_gid}, el siguiente es {next_gid}")
    saslib.init()
    saslib.sas_update_group(group, next_gid)
