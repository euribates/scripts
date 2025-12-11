#!/usr/bin/env python3

import argparse
import pwd
import grp
import subprocess
import settings
import locallib
import saslib

OK = '\033[0;32m[Ok]\033[0m'

def bold(text: str) -> str:
    return f'\033[1m{text}\033[0m'

def groups_by_username(username: str) -> list[str]:
    output = subprocess.check_output(['groups', username]).decode('utf-8')
    _username, groups = output.split(' : ')
    return groups.split()


def get_options() -> {}:
    parser = argparse.ArgumentParser(prog="alta-usuario-sas-viya")
    parser.add_argument('username', nargs="+", help="El login del usuario o usuarios")
    parser.add_argument('-v', '--verbose', action='store_true')
    opts = parser.parse_args()
    if opts.verbose:
        settings.is_tron(True)
    return opts


def main():
    options = get_options()
    for username in options.username:
        print(f'username: {username}')
        user_data = pwd.getpwnam(username)
        print(f'  - Nombre completo: {user_data.pw_gecos}')
        print(f'  - Local UID: {user_data.pw_uid}')
        print('  - Grupos:')
        for grupo in groups_by_username(username):
            _g = grp.getgrnam(grupo)
            print(f'      {grupo} ({_g.gr_gid})')
        print()

if __name__ == '__main__':
    main()
