from typing import Optional

from pcgs_api.access_token import load_token_from_env


class PCGSClient:

    def __init__(
            self,
            access_token: Optional[str] = None,
    ) -> None:
        if access_token is None:
            access_token = load_token_from_env(raise_on_missing=True)
        self.access_token = access_token
