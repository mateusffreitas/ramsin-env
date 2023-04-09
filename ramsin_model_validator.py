from __future__ import annotations
import ramsin_model
from pydantic import BaseSettings, validator
from ramsin_model_config import RamsinConfig


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
    pass


class ModelOptions(ramsin_model.ModelOptions):
    pass


class IsanControl(ramsin_model.IsanControl):
    pass


class IsanIsentropic(ramsin_model.IsanIsentropic):
    pass


class Post(ramsin_model.Post):
    pass


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
    def multiple_of_dtlong(cls, v, values):
        if (
                values.get("model_grids") is not None
                and values["model_grids"].dtlong is not None
                and (v.frqanl % values["model_grids"].dtlong) != 0.0
        ):
            raise ValueError('frqanl must be a multiple of dtlong')
        return v
