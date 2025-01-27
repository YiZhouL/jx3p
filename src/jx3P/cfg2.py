import typing as tp

import pydantic

NAME = str
PRESS_KEY = str
TRIGGER_KEY = str
LAST_SEC_TIME = float
NEXT = PRESS_KEY
ITEM = tp.List[tp.Any]  # [NAME, PRESS_KEY, LAST_SEC_TIME, NEXT]
MICRO = NAME


class Micro(pydantic.BaseModel):
    data: tp.Dict[TRIGGER_KEY, ITEM]
    switch: TRIGGER_KEY

    @property
    def keys(self) -> tp.Set[TRIGGER_KEY]:
        return set(self.data.keys())

