from __future__ import annotations
import ramsin_model
from pydantic import BaseSettings, validator
from ramsin_model_config import RamsinConfig


class ModelAdvRamsin(ramsin_model.ModelAdvRamsin):
    pass


class ModelGrids(ramsin_model.ModelGrids):
    @validator("timmax")
    def timmax_gt_0(cls, v):
        if v <= 0:
            raise ValueError("Must be greater than 0")
        return v

    @validator("dtlong")
    def dtlong_gte_1(cls, v):
        if v < 1.0:
            raise ValueError("Must be greater or equal to 1")
        return v


class CcattInfo(ramsin_model.CcattInfo):
    pass


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
