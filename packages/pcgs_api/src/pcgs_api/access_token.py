import os
from typing import Union

TOKEN_ENV_VAR_NAME = "PCGS_API_ACCESS_TOKEN"


def load_token_from_env(raise_on_missing: bool = True) -> Union[str, None]:
    """Load access token from environment variable.

    If the environment variable is missing, return None.

    Returns:
        str of environment variable or None if environment variable is missing.
    """
    value = os.environ.get(TOKEN_ENV_VAR_NAME, None)
    if value is None and raise_on_missing:
        raise MissingAccessTokenError(
            f"You must specify an access token to use this client. "
            f"Pass the token to Client using the `access_token` "
            f"parameter, or specify the token in the env using the "
            f"variable `{TOKEN_ENV_VAR_NAME}`."
        )
    return value


class MissingAccessTokenError(ValueError):
    pass


