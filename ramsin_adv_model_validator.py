from __future__ import annotations
import ramsin_adv_model
from pydantic import BaseSettings, validator
from ramsin_model_config import RamsinConfig


class ModelGrids2(ramsin_adv_model.ModelGrids2):
    pass


class CcattInfo2(ramsin_adv_model.CcattInfo2):
    pass


class TebSpmInfo(ramsin_adv_model.TebSpmInfo):
    pass


class ModelFileInfo2(ramsin_adv_model.ModelFileInfo2):
    pass


class ModelOptions2(ramsin_adv_model.ModelOptions2):
    pass


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
