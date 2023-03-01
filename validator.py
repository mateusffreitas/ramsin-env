from __future__ import annotations
import os
from pydantic import BaseModel, validator, BaseSettings, Field, create_model, \
    root_validator
from pydantic.env_settings import SettingsSourceCallable

from typing import List, Optional
import f90nml


class MyConfig:
    @classmethod
    def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
    ) -> tuple[SettingsSourceCallable, ...]:
        return env_settings, init_settings, file_secret_settings


class ModelAdvRamsin(BaseModel):
    advanced_ramsin: str


class ModelGrids(BaseSettings):
    expnme: str
    runtype: str
    timeunit: str
    timmax: int
    imonth1: int
    idate1: int
    iyear1: int
    itime1: int
    nnxp: int
    nnyp: int
    nnzp: int
    nzg: int
    nzs: int
    deltax: float
    deltay: float
    deltaz: float
    dzrat: float
    dzmax: float
    fixlevels: int
    zz: List[float]
    dtlong: float = Field(30., ge=1.0, env=["RAMSIN_MODEL_GRIDS_DTLONG", "DTLONG"])
    polelat: float
    polelon: float
    centlat: float
    centlon: float

    @validator('dtlong')
    def dtlong_greater_or_equal_to_1(cls, v):
        if v < 1.:
            raise ValueError('dtlong must be greater or equal to 1')
        return v

    @validator('dtlong')
    def dtlong_is_float(cls, v):
        if not isinstance(v, float):
            raise ValueError('dtlong must be float')
        return v

    class Config(MyConfig):
        pass


class CcattInfo(BaseModel):
    ccatt: int
    chemistry: int
    chem_timestep: float
    chem_assim: int
    srcmapfn: str
    aerosol: int
    aer_assim: int
    aer_timestep: float


class ModelFileInfo(BaseSettings):
    initial: int
    varfpfx: str
    tnudcent: float
    nudlat: int
    tnudlat: float
    tnudtop: float
    znudtop: float
    ipos: int
    ioutput: int
    hfilout: str
    afilout: str
    frqhis: float
    frqanl: float = Field(60., ge=1.0, env="FRQANL")
    topfiles: str
    sfcfiles: str
    sstfpfx: str
    ndvifpfx: str
    itoptfn: str
    isstfn: str
    ivegtfn: str
    isoilfn: str
    ndvifn: str

    class Config(MyConfig):
        pass


class ModelOptions(BaseModel):
    iswrtyp: int
    ilwrtyp: int
    radfrq: float
    nnqparm: int
    closure_type: str
    nnshcu: int
    confrq: float
    shcufrq: float
    isfcl: int
    isfcl_ocean: int
    soil_moist_fail: str
    usdata_in: str
    usmodel_in: str
    mcphys_type: int
    level: int


class IsanControl(BaseModel):
    isan_inc: int
    iapr: str
    varpfx: str


class IsanIsentropic(BaseModel):
    icfiletype: int
    icprefix: str
    wind_u_varname: str
    wind_v_varname: str
    temperature_varname: str
    geo_varname: str
    ur_varname: str
    initial_latitude: float
    final_latitude: float
    initial_longitude: float
    final_longitude: float
    z_max_level: int
    scale_factor: List[float]


class Post(BaseModel):
    nvp: int
    vp: List[str]
    gprefix: str
    csvfile: str
    anl2gra: str
    proj: str
    mean_type: str
    lati: List[float]
    latf: List[float]
    loni: List[float]
    lonf: List[float]
    zlevmax: List[int]
    ipresslev: int
    inplevs: int
    iplevs: List[int]
    ascii_data: str
    site_lat: float
    site_lon: float


class Model(BaseSettings):
    model_adv_ramsin: Optional[ModelAdvRamsin] = None
    model_grids: Optional[ModelGrids] = None
    ccatt_info: Optional[CcattInfo] = None
    model_file_info: Optional[ModelFileInfo] = None
    model_options: Optional[ModelOptions] = None
    isan_control: Optional[IsanControl] = None
    isan_isentropic: Optional[IsanIsentropic] = None
    post: Optional[Post] = None

    @validator("model_file_info")
    def multiple_of_dtlong(cls, v, values):
        print(v)
        if values['model_grids'].dtlong is not None and (v.frqanl % values['model_grids'].dtlong) != 0.:
            raise ValueError('frqanl is not a multiple of dtlong')
        return values


    class Config(MyConfig):
        pass

# def is_multiple_of_dtlong(values, v)

class RamsinModel(BaseModel):
    dtlong: float = 30.
    frqanl: float = 60.

    @validator('dtlong', pre=True, always=True, )
    def dtlong_greater_or_equal_to_1(cls, v):
        if v < 1.:
            raise ValueError('dtlong must be greater or equal to 1')
        return v

    @validator('dtlong', pre=True, always=True, )
    def dtlong_is_float(cls, v):
        if not isinstance(v, float):
            raise ValueError('dtlong must be float')
        return v

    @validator('frqanl')
    def multiple_of_dtlong(cls, v, values):
        if values.get('dtlong') is not None and (v % values['dtlong']) != 0.:
            raise ValueError('frqanl is not a multiple of dtlong')
        return v


class Settings(BaseSettings):
    dtlong: float = Field(30., env="DTLONG")
    frqanl: float = Field(60., env="FRQANL")


class EnvPrioritySettings(BaseSettings):
    dtlong: float = Field(30., ge=1.0, env=["RAMSIN_MODEL_GRIDS_DTLONG", "DTLONG"])
    frqanl: float = Field(60., env="FRQANL")

    @validator('dtlong')
    def dtlong_greater_or_equal_to_1(cls, v):
        if v < 1.:
            raise ValueError('dtlong must be greater or equal to 1')
        return v

    @validator('dtlong')
    def dtlong_is_float(cls, v):
        if not isinstance(v, float):
            raise ValueError('dtlong must be float')
        return v

    @validator('frqanl')
    def multiple_of_dtlong(cls, v, values):
        if values.get('dtlong') is not None and (v % values['dtlong']) != 0.:
            raise ValueError('frqanl is not a multiple of dtlong')
        return v

    class Config(MyConfig):
        pass


def test_pydantic_validation():
    ramsin = RamsinModel(
        dtlong=5.,
        frqanl=10
    )
    print(ramsin)

    keydict = {'dtlong': 6., 'frqanl': 12}
    ramsin = RamsinModel(**keydict)
    print(ramsin)

    t = Settings(dtlong=44.)
    print(t)

    tp = EnvPrioritySettings(dtlong=44.)
    print(tp)
    tp.dtlong = 44
    print(tp.dict())

    tp = EnvPrioritySettings(**keydict)
    print(tp)

    adv = ModelAdvRamsin(advanced_ramsin="./RRRRR")
    m = Model(model_adv_ramsin=adv)
    print(m)


def test_pydantic_model_fill_with_f90nml_object():
    with open("RAMSIN_BASIC") as f:
        ramsin_basic = f90nml.read(f)
    values = ramsin_basic.values().mapping
    #print(values)
    model = Model(**values)
    #print(model)
    print(f"dtlong = {model.model_grids.dtlong}")
    print(f"frqanl = {model.model_file_info.frqanl}")


def environ_test_setup():
    os.environ.setdefault("DTLONG", "15a.")
    # os.environ.setdefault("RAMSIN_MODEL_GRIDS_DTLONG", "3.")
    os.environ.setdefault("frqanl", "30.")


environ_test_setup()
# test_pydantic_validation()
test_pydantic_model_fill_with_f90nml_object()
