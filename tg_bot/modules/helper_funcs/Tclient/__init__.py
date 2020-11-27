from tg_bot import (
    Tclient,
    SUDO_USERS,
    OWNER_ID
)

MOD_USERS = SUDO_USERS + OWNER_ID

MOD_USERS = (
    list(SUDO_USERS)
    + list(OWNER_ID)
)

MOD_USERS.append(1087968824)
