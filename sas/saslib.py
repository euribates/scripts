from pathlib import Path
import getpass
from json import load as json_load
from datetime import datetime as DateTime

from locallib import execute
from settings import SAS_CLI
from settings import SAS_ENDPOINT
from settings import is_tron


def sas_needs_profile() -> bool:
    filename = Path('~/.sas/config.json')
    if not filename.exists():
        if is_tron():
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

    if is_tron():
        print('Tenemos que realizar el login')
    return True


def sas_init_profile():
    """Inicializa el profile del usuario.
    """
    execute(
        SAS_CLI,
        "profile",
        "init",
        "--colors-enabled",
        "no",
        "--output",
        "json",
        "--sas-endpoint",
        SAS_ENDPOINT,
        "--with-defaults",
        )


def sas_login():
    user = getpass.getuser()
    password = getpass.getpass()
    execute(
        SAS_CLI,
        "auth",
        "login",
        "--user",
        user,
        "--password",
        password,
        )


def sas_update_user(username: str, uid: int, gid: int):
    if is_tron():
        print(
            f"Actualizando el perfil de usuario {username} en SAS"
            f" para asignarle uid={uid} y gid={gid}"
            )
    execute(
        SAS_CLI,
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
    if is_tron():
        print(
            f"Actualizando el grupo {group} en SAS"
            f" para vinclularlo con el grupo local {gid}"
            )
    execute(
        SAS_CLI,
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
    if sas_needs_profile():
        sas_init_profile()
    if sas_needs_credentials_update():
        sas_login()

