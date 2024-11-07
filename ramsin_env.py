from __future__ import annotations
import argparse
import os
import f90nml
from ramsin_model_validator import RamsinBasic
from ramsin_adv_model_validator import RamsinAdvanced

def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
A program for modifying and creating a RAMSIN file based on environment variables.
The format is RAMSIN_{GROUP}_{VARIABLE}={VALUE}.
Examples of supported environment variable naming scheme and values: \n
    RAMSIN_NVP="1"                         ( Integer ) 
    RAMSIN_IPLEVS="500,400,300,200"        ( Integer array ) 
    RAMSIN_DELTAX="1000."                  ( Real )
    RAMSIN_SCALE_FACTOR="1.0e10,4.2"       ( Real Array )
    RAMSIN_VP="topo"                       ( Character )
    RAMSIN_VP="topo,precip"                ( Character array )
    RAMSIN_APPLYMETEOGRAM=".false."        ( Logical )
    RAMSIN_APPLYMETEOGRAM=".false.,.true." ( Logical array )""",
    )

    parser.add_argument(
        "--ramsin_basic",
        "-rb",
        action="store",
        type=str,
        default="RAMSIN_BASIC",
        help="the RAMSIN_BASIC file",
    )
    parser.add_argument(
        "--ramsin_advanced",
        "-ra",
        action="store",
        type=str,
        default="",
        help="the RAMSIN_ADVANCED file",
    )
    parser.add_argument(
        "--output_basic",
        "-ob",
        action="store",
        type=str,
        default="RAMSIN_BASIC_MODIFIED",
        help="the filename to write the RAMSIN_BASIC",
    )
    parser.add_argument(
        "--output_advanced",
        "-oa",
        action="store",
        type=str,
        default="RAMSIN_ADVANCED_MODIFIED",
        help="the filename to write the RAMSIN_ADVANCED",
    )

    return parser.parse_args()


def environ_test_setup():
    os.environ.setdefault("RAMSIN_DTLONG", "15")
    os.environ.setdefault("RAMSIN_NNXP", "560")
    os.environ.setdefault("RAMSIN_TIMMAX", "999")
    os.environ.setdefault("RAMSIN_EXPNME", "Test")
    #os.environ.setdefault("RAMSIN_DELTAZ", "1,2,3")
    os.environ.setdefault("RAMSIN_ZZ", "1,2,3")
    os.environ.setdefault("RAMSIN_IPLEVS", "1,2,3")
    #os.environ.setdefault("RAMSIN_VP", "precip,topo,tempc")

    # os.environ.setdefault("RAMSIN_MODEL_GRIDS_DTLONG", "3.")
    os.environ.setdefault("ramsin_frqanl", "30.")


def main():
    if os.environ.get("DEV_ENV") is not None:
        environ_test_setup()

    args = get_args()

    with open(args.ramsin_basic) as f:
        ramsin_basic = f90nml.read(f)

    print(f"Updating RAMSIN_BASIC from {args.ramsin_basic}")

    values = ramsin_basic.values().mapping
    model = RamsinBasic(**values)
    ramsin_basic.patch(model.dict())
    ramsin_basic.write(nml_path=args.output_basic, force=True, sort=False)

    if len(args.ramsin_advanced) == 0:
        ramsin_advanced_path = ramsin_basic["MODEL_ADV_RAMSIN"]["ADVANCED_RAMSIN"]
    else:
        ramsin_advanced_path = args.ramsin_advanced

    with open(ramsin_advanced_path) as f:
        ramsin_advanced = f90nml.read(f)

    print(f"Updating RAMSIN_ADVANCED from {ramsin_advanced_path}")
    adv_values = ramsin_advanced.values().mapping
    adv_model = RamsinAdvanced(**adv_values)
    ramsin_advanced.patch(adv_model.dict())
    ramsin_advanced.write(nml_path=args.output_advanced, force=True, sort=False)


if __name__ == "__main__":
    main()
