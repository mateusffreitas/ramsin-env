from pydantic.env_settings import SettingsSourceCallable
from typing import Any

FLOAT_LIST_VARS = ["zz","scale_factor","lati","latf","loni","lonf","wt_nudge_grid","toptenh","toptwvl","z0max","slz","slmstr","stgoff","csx","csz","xkhkm","zkhkm","akmin","gnu","ps","ts","rts","us","vs","gridwt","wvlnth","swvlnth","respon","dlimit","ulimit"]
INT_LIST_VARS = ["zlevmax","iplevs","nstratx","nstraty","nndtrat","nstratz1","nstratz2","ninest","njnest","nknest","nnsttop","nnstbot","nxtnest","diur_cycle","itoptflg","isstflg","ivegtflg","isoilflg","ndviflg","nofilflg","itopsflg","iz0flg","idiffk","ixsctn","isbval","levth"]
STR_LIST_VARS = ["vp","iplfld"]
BOOL_LIST_VARS = []

class RamsinConfig:
    env_prefix = 'RAMSIN_'

    @classmethod
    def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
    ) -> tuple[SettingsSourceCallable, ...]:
        return env_settings, init_settings, file_secret_settings

    @classmethod
    def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
        if field_name in FLOAT_LIST_VARS:
            return [float(x) for x in raw_val.split(',')]
        elif field_name in INT_LIST_VARS:
            return [int(x) for x in raw_val.split(',')]
        elif field_name in STR_LIST_VARS:
            return [str(x) for x in raw_val.split(',')]
        elif field_name in BOOL_LIST_VARS:
            return [bool(x) for x in raw_val.split(',')]
        return cls.json_loads(raw_val)

