#!/usr/bin/env bash

f90nml RAMSIN_BASIC ramsin.json

datamodel-codegen --input ramsin.json \
    --input-file-type json \
    --base-class pydantic.BaseSettings \
    --output ramsin_model.py \
    --class-name RamsinBasic

f90nml RAMSIN_ADVANCED ramsin_adv.json

datamodel-codegen --input ramsin_adv.json \
    --input-file-type json \
    --base-class pydantic.BaseSettings \
    --output ramsin_adv_model.py \
    --class-name RamsinAdvanced

get_list_vars()  {
  grep ${1} ramsin_model.py ramsin_adv_model.py \
  | cut -d':' -f2 \
  | perl -pe 's{^(.*)$}{"$1",}; s/\s+//; s/\n+//'
}

FLOAT_LIST_VARS=$(get_list_vars "List\[float\]")
INT_LIST_VARS=$(get_list_vars "List\[int\]")
STR_LIST_VARS=$(get_list_vars "List\[str\]")
BOOL_LIST_VARS=$(get_list_vars "List\[bool\]")


cat <<-EOF > ramsin_model_config.py
from pydantic.env_settings import SettingsSourceCallable
from typing import Any

FLOAT_LIST_VARS = [${FLOAT_LIST_VARS%,}]
INT_LIST_VARS = [${INT_LIST_VARS%,}]
STR_LIST_VARS = [${STR_LIST_VARS%,}]
BOOL_LIST_VARS = [${BOOL_LIST_VARS%,}]

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

EOF

#Add RamsinConfig class to generated Model
sed -i -E '7s@^@from ramsin_model_config import RamsinConfig\n\n@ ;
   s@^(class .*:)$@\1\n    class Config(RamsinConfig): pass@
' ramsin_adv_model.py  ramsin_model.py
