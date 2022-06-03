from pydantic import BaseModel


class ReserveHR(BaseModel):
    edad: int
    reserveHR: int

class HostaticTest(BaseModel):
    hr_one: int
    hr_two: int
