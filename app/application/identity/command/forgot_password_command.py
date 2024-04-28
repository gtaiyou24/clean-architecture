from dataclasses import dataclass


@dataclass(init=True, unsafe_hash=True, frozen=True)
class ForgotPasswordCommand:
    email_address: str
