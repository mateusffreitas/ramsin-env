from __future__ import annotations
import ramsin_adv_model
from pydantic import BaseSettings, validator
from ramsin_model_config import RamsinConfig


class ModelGrids2(ramsin_adv_model.ModelGrids2):

    @validator("ihtran")
    def ihtran_valid_values(cls, v):
        choices = [0, 1]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("ideltat")
    def ideltat_valid_values(cls, v):
        choices = [0, 1, 2]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v


class CcattInfo2(ramsin_adv_model.CcattInfo2):
    @validator("split_method")
    def split_method_valid_values(cls, v):
        choices = ['SYMMETRIC', 'SEQUENTIAL', 'PARALLEL']
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("chemistry_aq", "recycle_tracers", "plumerise", "volcanoes")
    def ccattinfo2_on_off_valid_values(cls, v):
        choices = [0, 1]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("def_proc_src")
    def def_proc_src_valid_values(cls, v):
        choices = ['STOP', 'LAST_SOURCES']
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v


class TebSpmInfo(ramsin_adv_model.TebSpmInfo):
    @validator("teb_spm")
    def teb_spm_valid_values(cls, v):
        choices = [0, 1]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v


class ModelFileInfo2(ramsin_adv_model.ModelFileInfo2):
    @validator("nud_type")
    def nud_type_valid_values(cls, v):
        choices = [0, 1, 2]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("iclobber", "ihistdel", "ipastin", "kwrite", "initfld", "iupdndvi",
               "iupdsst", "mkcoltab")
    def modelfileinfo2_on_off_valid_values(cls, v):
        choices = [0, 1]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("applyiau")
    def applyiau_valid_values(cls, v):
        choices = [0, 1, 2]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

class ModelOptions2(ramsin_adv_model.ModelOptions2):

    @validator("dyncore_flag")
    def dyncore_flag_valid_values(cls, v):
        choices = [0, 1, 2, 3]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("advmnt")
    def advmnt_valid_values(cls, v):
        choices = [0, 1, 2]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v

    @validator("icorflg","imassflx", "lonrad", "g3d_spread")
    def modeloptions2_on_off_valid_values(cls, v):
        choices = [0, 1]
        if v not in choices:
            raise ValueError(f"Value must be one of {choices}")
        return v


class ModelSound(ramsin_adv_model.ModelSound):
    pass


class ModelPrint(ramsin_adv_model.ModelPrint):
    pass


class IsanControl2(ramsin_adv_model.IsanControl2):
    pass


class IsanIsentropic2(ramsin_adv_model.IsanIsentropic2):
    pass


class Digitalfilter(ramsin_adv_model.Digitalfilter):
    pass


class Meteogram(ramsin_adv_model.Meteogram):
    pass


class RamsinAdvanced(BaseSettings):
    class Config(RamsinConfig): pass

    model_grids2: ModelGrids2
    ccatt_info2: CcattInfo2
    teb_spm_info: TebSpmInfo
    model_file_info2: ModelFileInfo2
    model_options2: ModelOptions2
    model_sound: ModelSound
    model_print: ModelPrint
    isan_control2: IsanControl2
    isan_isentropic2: IsanIsentropic2
    digitalfilter: Digitalfilter
    meteogram: Meteogram
