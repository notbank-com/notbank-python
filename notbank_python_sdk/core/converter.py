from enum import Enum
from decimal import Decimal
from dataclasses import asdict
from typing import Any, Callable, Dict, List, Type, TypeVar, Union
from uuid import UUID

import simplejson as json
from dacite import Config, DaciteError, from_dict as dacite_from_dict

from notbank_python_sdk.core.either import Either
from notbank_python_sdk.error import ErrorCode, NotbankException
from notbank_python_sdk.core.tools import dec_to_str_stripped


T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
CAST_TYPE_FN = Callable[[Any], Any]
TYPE = Type[Any]

SPECIAL_CASES_MAP = {
    "oms_id": "OMSId",
    "api_key": "APIKey",
    "order_id_oco": "OrderIdOCO",
    "requires_2fa": "Requires2FA",
    "two_fa_type": "TwoFAType",
    "two_fa_token": "TwoFAToken",
    "enforce_enable_2fa": "EnforceEnable2FA",
    "use_2fa": "Use2FA",
    "cr": "CR",
    "dr": "DR",
    "parent_id": "ParentID",
    "request_ip": "RequestIP",
    "ipv6a": "IPv6a",
    "ipv6b": "IPv6b",
    "pending_2fa": "Pending2Fa",
    "confirmed_2fa": "Confirmed2Fa",
    "md_update_id": "MDUpdateID",
    "rolling_24_hr_volume": "Rolling24HrVolume",
    "rolling_24_hr_notional": "Rolling24HrNotional",
    "rolling_24_num_trades": "Rolling24NumTrades",
    "rolling_24_hr_px_change": "Rolling24HrPxChange",
    "rolling_24_hr_px_change_percent": "Rolling24HrPxChangePercent",
    "result": "result",
    "errormsg": "errormsg",
    "errorcode": "errorcode",
    "detail": "detail",
    "base64_bytes": "base64Bytes",
    "market_pair": "Market_Pair",
    "m": "m",
    "n": "n",
    "o": "o",
    "i": "i",
    "report_flavor": "reportFlavor",
    "create_time": "createTime",
    "initial_run_time": "initialRunTime",
    "interval_start_time": "intervalStartTime",
    "interval_end_time": "intervalEndTime",
    "interval_duration": "intervalDuration",
    "last_instance_id": "lastInstanceId",
    "account_ids": "accountIds",
}

DEFAULT_CAST: Dict[Type[Any], Any] = {
    Decimal: lambda x: dec_to_str_stripped(x), UUID: lambda x: str(x)}


def _cast_value_or_default(type_hooks: Dict[Type[T1], Callable[[T1], T2]], value: T1) -> Union[T1, T2]:
    cast_fn = type_hooks.get(type(value))
    if cast_fn is None:
        if isinstance(value, Enum):
            return value.value
        return value
    return cast_fn(value)


def _build_factory(type_hooks: Dict[Type[Any], Any]) -> Callable[[dict], dict]:
    def factory(data: dict) -> dict:
        return dict(
            [entry[0], _cast_value_or_default(type_hooks, entry[1])]
            for entry
            in data
            if entry[1] is not None)
    return factory


def _to_pascal_case(key: str, exclusions: List[str] = [], overrides: Dict[str, str] = {}) -> str:
    converted_key = overrides.get(key)
    if converted_key:
        return converted_key
    pascal_case_key = SPECIAL_CASES_MAP.get(key)
    if pascal_case_key is not None:
        return pascal_case_key
    if key in exclusions:
        return key
    chunks = key.split('_')
    return ''.join(chunk.title() for chunk in chunks)


def to_json_str(data, cast: Dict[Type[Any], Any] = dict()) -> str:
    json_dict = to_dict(data, cast)
    return json.dumps(json_dict, use_decimal=True)


def to_nb_dict(data, cast: Dict[Type[Any], Any] = DEFAULT_CAST) -> dict:
    return to_dict(data, cast, as_snake_case_dict=True)


def to_dict(data, cast: Dict[Type[Any], Any] = DEFAULT_CAST, as_snake_case_dict: bool = False) -> dict:
    if data is None:
        return {}
    dict_factory = _build_factory(cast)
    snake_case_dict = asdict(data, dict_factory=dict_factory)   # type: ignore
    if as_snake_case_dict:
        return snake_case_dict
    return {_to_pascal_case(key): snake_case_dict[key] for key in snake_case_dict}


def from_dict(cls: Type[T1], data, no_pascal_case: List[str] = [], overrides: Dict[str, str] = {}, from_pascal_case: bool = True) -> T1:
    convert_key = get_convert_key_fn(
        no_pascal_case, overrides, from_pascal_case)
    return dacite_from_dict(
        cls,
        data,
        config=Config(
            cast=[Enum],
            convert_key=convert_key,
            type_hooks={
                Decimal: lambda x: Decimal(str(x)),
                float: lambda x: Decimal(str(x)),
                UUID: lambda x: UUID(x),
                int: lambda x: int(x),
            }
        )
    )


def get_convert_key_fn(no_pascal_case: List[str], overrides: Dict[str, str], from_pascal_case: bool) -> Callable[[str], str]:
    if from_pascal_case:
        def convert_key(key): return _to_pascal_case(
            key, no_pascal_case, overrides)
        return convert_key
    return lambda x: x


def from_json_str(cls: Type[T1], json_str: str, overrides: Dict[str, str] = {}) -> Either[NotbankException, T1]:
    try:
        data = json.loads(json_str, use_decimal=True)
    except json.JSONDecodeError as e:
        return Either.left(NotbankException(ErrorCode.CONFIGURATION_ERROR, f"Failed to parse json. {e}"))
    try:
        instance = from_dict(cls, data, overrides=overrides)
    except DaciteError as e:
        return Either.left(NotbankException(ErrorCode.CONFIGURATION_ERROR, f"Failed to parse json. {e}"))
    return Either.right(instance)


def list_from_json_str(cls: Type[T1], json_str: str) -> Either[NotbankException, List[T1]]:
    try:
        data = json.loads(json_str, use_decimal=True)
    except json.JSONDecodeError as e:
        return Either.left(NotbankException(ErrorCode.CONFIGURATION_ERROR, f"Failed to parse json. {e}"))
    if not isinstance(data, list):
        return Either.left(NotbankException(ErrorCode.CONFIGURATION_ERROR, f"Failed to parse json. data is not a list. data is {json_str}"))
    try:
        instance_list = [from_dict(cls, data_elem) for data_elem in data]
    except DaciteError as e:
        return Either.left(NotbankException(ErrorCode.CONFIGURATION_ERROR, f"Failed to parse json. {e}"))
    return Either.right(instance_list)
