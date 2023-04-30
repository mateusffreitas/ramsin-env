# ramsin-env
A prototype of a tool to enable the usage of environment variables to edit the RAMSIN namelist of BRAMS.

## Usage
```bash
python3 ramsin_env.py -h
# With Nuitka binary
./ramsin_env.bin -h
```

## Generating a bundled binary with [Nuitka](https://nuitka.net/doc/user-manual.html)

```bash
pip install nuitka
python3 -m nuitka --follow-imports ramsin_env.py
# Produces ramsin_env.bin
```