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
pip3 install nuitka
pip3 install -r requirements.txt
python3 -m nuitka --onefile --standalone ramsin_env.py
# Produces ramsin_env.bin
```