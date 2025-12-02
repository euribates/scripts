from pathlib import Path
import os
import getpass
from json import load as json_load
from datetime import datetime as DateTime

import settings
from locallib import execute

TRON = settings.is_tron()


def sas_needs_profile() -> bool:
    filename = Path('~/.sas/config.json')
    if not filename.exists():
        if TRON:
            print('Tenemos que actualizar el perfil')
        return True
    return False

    
def sas_needs_credentials_update() -> bool:
    filename = Path('~/.sas/credentials.json')
    if filename.exists():
        with open(filename, 'r', encoding='utf-8') as f_in:
            credentials = json_load(f_in)
            if 'Default' in credentials:
                default = credentials['Default']
                if 'expiry' in default:
                    expiry = DateTime.fromisoformat(default['expiry'])
                    return expiry <= DateTime.now()

    if TRON:
        print('Tenemos que realizar el login')
    return True


def sas_init_profile():
    """Inicializa el profile del usuario.
    """
    if TRON:
        print(
            f"Actualizando el perfil de conexión de usuario."
            )
    cmd = [
        settings.SAS_CLI,
        "profile",
        "init",
        "--colors-enabled",
        "--output",
        "json",
        "--sas-endpoint",
        settings.SAS_ENDPOINT,
        "--with-defaults",
        ]
    result = execute(*cmd)
    print(result)


def sas_login():
    user = input(f'Usuario con el que conectarse a SAS [{settings.ADMIN_USER}]:').strip()
    user = user or settings.ADMIN_USER
    password = _read_dot_password()
    if not password:
        password = getpass.getpass()
    execute(
        settings.SAS_CLI,
        "auth",
        "login",
        "--user",
        user,
        "--password",
        password,
        )


def sas_update_user(username: str, uid: int, gid: int):
    if TRON:
        print(
            f"Actualizando el perfil de usuario {username} en SAS"
            f" para asignarle uid={uid} y gid={gid}"
            )
    execute(
        settings.SAS_CLI,
        "--output",
        "json",
        "identities",
        "update-user",
        "--id",
        username,
        "--uid",
        str(uid),
        "--gid",
        str(gid),
        )


def sas_update_group(group: str, gid: int):
    if TRON:
        print(
            f"Actualizando el grupo {group} en SAS"
            f" para vinclularlo con el grupo local {gid}"
            )
    execute(
        settings.SAS_CLI,
        "--output",
        "json",
        "identities",
        "update-group",
        "--id",
        group,
        "--gid",
        str(gid),
        )


def sas_init():
    os.environ['SSL_CERT_FILE'] = settings.SSL_CERT_FILE
    if sas_needs_profile():
        sas_init_profile()
    if sas_needs_credentials_update():
        sas_login()


def _read_dot_password():
    f = Path('./.password')
    if f.exists():
        with open(f, 'r') as s:
            return s.read().strip()
    return None

