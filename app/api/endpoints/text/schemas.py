import enum
import datetime
from typing import Optional, List, Union

from pydantic import validator, root_validator

from app.db.schemas import BaseSchema


class LangEnum(str, enum.Enum):
    en = "en"
    de = "de"
    es = "es"
    fr = "fr"
    it = "it"
    nl = "nl"
    pl = "pl"
    ru = "ru"


class StatValueEnum(str, enum.Enum):
    flesch_reading_ease = "flesch_reading_ease"  # -> float
    wiener_sachtextformel = "wiener_sachtextformel"  # variant: int -> float
    syllable_count = "syllable_count"  # -> int
    lexicon_count = "lexicon_count"  # removepunct: bool (True) -> int
    sentence_count = "sentence_count"  # -> int
    char_count = "character_count"  # ignore_spaces: bool (True) -> int
    letter_count = "letter_count"  # ignore_spaces: bool (True) -> int
    polysyllabcount = "polysyllable_count"  # int
    monosyllabcount = "mono_syllable_count"  # int


class ArgumentParamEnum(str, enum.Enum):
    variant = "variant"
    removepunct = "removepunct"
    ignore_spaces = "ignore_spaces"


class StatBase(BaseSchema):
    name: StatValueEnum
    value: float
    argument: Optional[dict]
    lang: Optional[LangEnum] = LangEnum.en


class StatCreate(StatBase):
    pass


class StatUpdate(StatBase):
    pass


class TextBase(BaseSchema):
    id: str


class TextCreate(TextBase):
    name: str
    content_type: str
    extension: str


class TextUpdate(TextBase):
    internal_name: Optional[str]


class TextRead(TextCreate):
    created_at: datetime.datetime
    updated_at: datetime.datetime


class TextStats(BaseSchema):
    stats: Optional[List[StatBase]]


class StatArgumentParam(BaseSchema):
    name: ArgumentParamEnum
    value: Optional[Union[int, bool]]

    @root_validator(pre=True)
    def required_value(cls, values: dict) -> dict:
        if values.get("name") == ArgumentParamEnum.variant and values.get("value") is None:
            raise ValueError("value is required")
        return values

    @validator("value", pre=True)
    def check_int_value(cls, v: Union[int, bool], values: dict) -> Union[int, bool]:
        if values.get("name") == ArgumentParamEnum.variant:
            if type(v) != int:
                raise ValueError("must be an integer")
        return v

    @validator("value", pre=True)
    def check_int_range_type(cls, v: Union[int, bool], values: dict) -> Union[int, bool]:
        if values.get("name") == ArgumentParamEnum.variant:
            if v not in range(1, 5):
                raise ValueError("variant can only be an integer between 1 and 4")
        return v

    @validator("value", pre=True)
    def check_bool_type(cls, v: Union[int, bool], values: dict) -> Union[int, bool]:
        if values.get("name") in (ArgumentParamEnum.ignore_spaces, ArgumentParamEnum.removepunct):
            if type(v) != bool:
                raise ValueError("must be a bool")
        return v


class StatArgument(BaseSchema):
    name: StatValueEnum
    lang: Optional[LangEnum] = LangEnum.en
    argument: Optional[StatArgumentParam]

    @validator("argument", pre=True)
    def argument_as_required(cls, v: Optional[dict], values: dict) -> dict:
        name = values.get("name")
        argument_name = v.get("name")
        if name == StatValueEnum.wiener_sachtextformel:
            if not v or argument_name != ArgumentParamEnum.variant:
                raise ValueError(f"missing required argument: '{ArgumentParamEnum.variant}'")
        return v

    @validator("argument", pre=True)
    def argument_as_needed(cls, v: Optional[dict], values: dict) -> dict:
        name = values.get("name")
        argument_name = v.get("name")
        if name != StatValueEnum.wiener_sachtextformel and argument_name == ArgumentParamEnum.variant:
            cls.is_not_allowed(ArgumentParamEnum.variant)
        elif name != StatValueEnum.lexicon_count and argument_name == ArgumentParamEnum.removepunct:
            cls.is_not_allowed(ArgumentParamEnum.removepunct)
        elif (
                name not in (StatValueEnum.char_count, StatValueEnum.letter_count) and
                argument_name == ArgumentParamEnum.ignore_spaces
        ):
            cls.is_not_allowed(ArgumentParamEnum.ignore_spaces)
        return v

    @classmethod
    def is_not_allowed(cls, argument: ArgumentParamEnum) -> None:
        raise ValueError(f"'{argument}' is not allowed argument")
