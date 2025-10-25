# ramsin-env
A prototype of a tool to enable the usage of environment variables to edit the RAMSIN namelist of BRAMS.

## Usage
```bash
python3 ramsin_env.py -h
# With Nuitka binary
./ramsin_env.bin -h
```

## Generating a bundled binary with [Nuitka](https://nuitka.net/doc/user-manual.html)
Currently it does not work with Python 3.13 or newer
```bash
./create_bin.sh
# Produces ramsin_env.bin
```
