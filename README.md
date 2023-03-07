# ramsin-env
A prototype of a tool to enable the usage of environment variables to edit the RAMSIN namelist of BRAMS.

## Usage
```bash
python3 main.py -h
```

## Generating the model classes with code generation

```bash
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

```