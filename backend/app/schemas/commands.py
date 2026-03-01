from pydantic import BaseModel


class CommandRequest(BaseModel):
    pass


class ClimatizationStartRequest(BaseModel):
    target_temperature: float


class UnlockRequest(BaseModel):
    spin: str


class CommandResponse(BaseModel):
    status: str
    message: str | None = None
