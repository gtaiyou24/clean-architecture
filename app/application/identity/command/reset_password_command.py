from dataclasses import dataclass


@dataclass(init=True, unsafe_hash=True, frozen=True)
class ResetPasswordCommand:
    reset_token: str
    password: str
