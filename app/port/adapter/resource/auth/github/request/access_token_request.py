from typing import Annotated

from fastapi import Form


class AccessTokenRequest:
    def __init__(
        self,
        code: Annotated[str, Form()],
        redirect_uri: Annotated[str, Form()],
        code_verifier: Annotated[str, Form()],
        grant_type: Annotated[str, Form()]
    ):
        self.code = code
        self.redirect_uri = redirect_uri
        self.code_verifier = code_verifier
        self.grant_type = grant_type
