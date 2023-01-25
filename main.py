import argparse
import os
import re

import f90nml


def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
A program for modifying and creating a RAMSIN file based on environment variables.
The format is RAMSIN_{GROUP}_{VARIABLE}={VALUE}.
Examples of supported environment variable naming scheme and values: \n
    RAMSIN_POST_NVP="1"                              ( Integer ) 
    RAMSIN_POST_IPLEVS="500,400,300,200"             ( Integer array ) 
    RAMSIN_MODEL_GRIDS_DELTAX="1000."                ( Real )
    RAMSIN_ISAN_ISENTROPIC_SCALE_FACTOR="1.0e10,4.2" ( Real Array )
    RAMSIN_POST_VP="'topo'"                          ( Character )
    RAMSIN_POST_VP="'topo','precip'"                 ( Character array )
    RAMSIN_METEOGRAM_APPLYMETEOGRAM=".false."        ( Logical )
    RAMSIN_METEOGRAM_APPLYMETEOGRAM=".false.,.true." ( Logical array )""")

    parser.add_argument("--ramsin_basic", "-f", action="store", type=str,
                        default="RAMSIN_BASIC",
                        help="the RAMSIN_BASIC file")
    parser.add_argument("--output_basic", "-o", action="store", type=str,
                        default="RAMSIN_BASIC_MODIFIED",
                        help="the filename to write the RAMSIN_BASIC")
    parser.add_argument("--output_advanced", "-a", action="store", type=str,
                        default="RAMSIN_ADVANCED_MODIFIED",
                        help="the filename to write the RAMSIN_ADVANCED")

    return parser.parse_args()


def get_ramsin_environment_variables():
    ramsin_env_list = []
    for env_var, value in os.environ.items():
        if re.match("RAMSIN_[^\W_]+\w*_[^\W_]+", env_var) is not None:
            group_var = env_var.split('RAMSIN_')[1].lower()
            ramsin_env_list.append((group_var, value))

    return ramsin_env_list


def update_ramsin(ramsin, ramsin_env_list):
    groups_patch_nml = {k: [f"${k} \n"] for k in
                        ramsin.todict().keys()}
    # print(groups_patch_nml)

    env_list = []
    # Filter env vars by including only for known groups.
    # If group or variable name contains underscore, tries to find the group by
    # iterating each possible sequential join. The variable becomes the remaining part.
    for group_var, value in ramsin_env_list:
        gvsplit = group_var.split('_')
        for i in range(len(gvsplit) - 1):
            candidate_group = "_".join(gvsplit[0:i + 1])
            candidate_var = "_".join(gvsplit[i + 1:])
            if candidate_group in groups_patch_nml:
                env_list.append((candidate_group, candidate_var, value))
                break

    for var_group, var_name, value in env_list:

        # TODO: Add type check
        ramsin_var = ramsin[var_group].get(var_name)
        if ramsin_var is not None:
            groups_patch_nml[var_group].append(f"{var_name} = {value} \n")
        else:
            print(
                f"{var_group} does not have a variable named '{var_name}'. Skipping it.")

    for k, v in groups_patch_nml.items():
        v.append("$end \n")

    nml_patch = "".join(["".join(v) for v in groups_patch_nml.values()])
    ramsin.patch(f90nml.reads(nml_patch))


def environ_test_setup():
    os.environ.setdefault("RAMSIN_POST_IPLEVS", "500,400,300,200")
    os.environ.setdefault("RAMSIN_POST_VP", "'500','400','300','200'")
    os.environ.setdefault("RAMSIN_MODEL_GRIDS_DELTAX", "1000.555")
    os.environ.setdefault("RAMSIN_MODEL_GRIDS_DELTAXF", "1000.555")
    os.environ.setdefault("RAMSIN_MODEL_GRIDS2_DELTAXN", "10.555")
    os.environ.setdefault("RAMSIN_METEOGRAM_APPLYMETEOGRAM", ".true.")
    os.environ.setdefault("RAMSIN_ISAN_ISENTROPIC_SCALE_FACTOR", "1.0,2.0,4.2, 2e-10")




def main():
    #environ_test_setup()

    args = get_args()

    ramsin_env_list = get_ramsin_environment_variables()

    if len(ramsin_env_list) == 0:
        print(
            "There are no environment variables set up for RAMSIN.\nNothing to be done.")
        exit(0)

    with open(args.ramsin_basic) as f:
        ramsin_basic = f90nml.read(f)

    print(f"Updating RAMSIN_BASIC from {args.ramsin_basic}")
    update_ramsin(ramsin_basic, ramsin_env_list)
    ramsin_basic.write(args.output_basic, force=True)

    ramsin_advanced_path = ramsin_basic["MODEL_ADV_RAMSIN"]["ADVANCED_RAMSIN"]

    with open(ramsin_advanced_path) as f:
        ramsin_advanced = f90nml.read(f)

    print(f"Updating RAMSIN_ADVANCED from {ramsin_advanced_path}")
    update_ramsin(ramsin_advanced, ramsin_env_list)
    ramsin_advanced.write(args.output_advanced, force=True)

    # print(ramsin_basic)


if __name__ == '__main__':
    main()
