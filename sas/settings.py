from pathlib import Path

from prettyconf import config

ETC_PASSWD: Path = Path("/etc/passwd")
ETC_GROUP: Path = Path("/etc/group")

SAS_CLI = config('SAS_CLI', default='/datos/SAS-VIYA-CLI/sas-viya')
SAS_ENDPOINT = config('SAS_ENDPOINT', default='https://piad-pre.gobiernodecanarias.net/')

TRON = config('TRON', default=False, cast=config.boolean)

def is_tron(value=None) -> bool:
    global TRON
    if value is not None:
        TRON = bool(value)
    return TRON
