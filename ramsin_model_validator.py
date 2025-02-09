from __future__ import annotations
import ramsin_model
from pydantic import BaseSettings, validator
from ramsin_model_config import RamsinConfig
from datetime import date

class ModelAdvRamsin(ramsin_model.ModelAdvRamsin):
    pass


class ModelGrids(ramsin_model.ModelGrids):

    @validator("expnme")
    def expnme_length_gte_1(cls, v):
        if len(v) == 0:
            raise ValueError("Length must be greater or equal to 1")
        return v

    @validator('runtype')
    def runtype_valid_values(cls, v):
        choices = ['MAKESFC', 'MAKEVFILE', 'INITIAL', 'HISTORY', 'MEMORY']
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("timeunit")
    def timeunit_valid_values(cls, v):
        choices = ['h', 'm', 's']
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator('timmax', 'imonth1', 'idate1', 'iyear1', 'nnxp', 'nnyp', 'nnzp', 'nzg',
               'nzs', 'deltax', 'deltay')
    def positive_value(cls, v):
        if v <= 0:
            raise ValueError('Value must be positive')
        return v

    @validator('iyear1')
    def check_valid_date(cls, v, values):
        try:
            exp_date = date.fromisoformat(f"{v:04}-{values['imonth1']:02}-{values['idate1']:02}")
        except ValueError as e:
            raise ValueError(e)
        return v

    @validator("dtlong")
    def dtlong_gte_1(cls, v):
        if v < 1.0:
            raise ValueError("Value must be greater or equal to 1")
        return v

    @validator("zz")
    def zz_length_eq_nnzp(cls, v, values):
        if values["deltaz"] == 0. and len(v) != values["nnzp"]:
            raise ValueError("Length must be equal to nnzp")
        return v


class CcattInfo(ramsin_model.CcattInfo):
    @validator("ccatt", "chem_assim", "aerosol", "aer_assim")
    def ccattinfo_on_off_valid_values(cls, v):
        choices = [0, 1]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("chemistry")
    def chemistry_valid_values(cls, v):
        choices = [-1, 0, 1, 2, 3, 4]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v


class ModelFileInfo(ramsin_model.ModelFileInfo):
    @validator("ioutput")
    def ioutput_valid_values(cls, v):
        choices = [0, 1, 2, 10]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v


class ModelOptions(ramsin_model.ModelOptions):
    @validator("ilwrtyp")
    def ilwrtyp_valid_values(cls, v):
        choices = [0, 1, 2, 3, 4, 5, 6]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("nnqparm")
    def nnqparm_valid_values(cls, v):
        choices = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("closure_type")
    def closure_type_valid_values(cls, v):
        choices = ['PB', 'EN', 'GR', 'LO', 'MC', 'SC', 'AS']
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("nnshcu")
    def nnshcu_valid_values(cls, v):
        choices = [0, 1, 2, 3]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("isfcl")
    def isfcl_valid_values(cls, v):
        choices = [0, 1, 2, 3, 4, 5]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("isfcl_ocean")
    def isfcl_ocean_valid_values(cls, v):
        choices = [0, 1]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("soil_moist_fail")
    def soil_moist_fail_valid_values(cls, v):
        choices = ['s', 'h', 'l']
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("mcphys_type")
    def mcphys_type_valid_values(cls, v):
        choices = [0, 1, 2, 3, 4, 5, 6, 7]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v


class IsanControl(ramsin_model.IsanControl):
    @validator("isan_inc")
    def isan_inc_positive(cls, v):
        if v <= 0:
            raise ValueError(f"Value must be positive")
        return v


class IsanIsentropic(ramsin_model.IsanIsentropic):
    @validator("icfiletype")
    def icfiletype_valid_values(cls, v):
        choices = [0, 1, 2, 3, 4]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v


class Post(ramsin_model.Post):
    @validator("vp")
    def vp_length_eq_nvp(cls, v, values):
        if len(v) != int(values["nvp"]):
            raise ValueError("Length must be equal to nvp")
        return v


class RamsinBasic(BaseSettings):
    class Config(RamsinConfig):
        pass

    model_adv_ramsin: ModelAdvRamsin
    model_grids: ModelGrids
    ccatt_info: CcattInfo
    model_file_info: ModelFileInfo
    model_options: ModelOptions
    isan_control: IsanControl
    isan_isentropic: IsanIsentropic
    post: Post

    @validator("model_file_info")
    def frqanl_multiple_of_dtlong(cls, v, values):
        if (
                values.get("model_grids") is not None
                and values["model_grids"].dtlong is not None
                and (v.frqanl % values["model_grids"].dtlong) != 0.0
        ):
            raise ValueError('frqanl must be a multiple of dtlong')
        return v

    @validator("ccatt_info")
    def chem_timestep_multiple_of_dtlong(cls, v, values):
        if (
                v.ccatt == 1
                and values.get("model_grids") is not None
                and values["model_grids"].dtlong is not None
                and ((v.chem_timestep % values["model_grids"].dtlong) != 0.0
                     or (v.chem_timestep / values["model_grids"].dtlong) > 4)
        ):
            raise ValueError(
                'chem_timestep must be a multiple of dtlong and 4 times at most')
        return v

    @validator("ccatt_info")
    def aer_timestep_multiple_of_dtlong(cls, v, values):
        if (
                v.ccatt == 1
                and v.aerosol == 1
                and values.get("model_grids") is not None
                and values["model_grids"].dtlong is not None
                and ((v.aer_timestep % values["model_grids"].dtlong) != 0.0
                     or (v.aer_timestep / values["model_grids"].dtlong) > 4)
        ):
            raise ValueError(
                'aer_timestep must be a multiple of dtlong and 4 times at most')
        return v
