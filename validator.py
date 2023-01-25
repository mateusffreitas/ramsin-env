from pydantic import BaseModel, validator


class RamsinModel(BaseModel):
    dtlong: float = 3.
    frqanl: float = 6.

    @validator('dtlong')
    def dtlong_greater_or_equal_to_1(cls, v):
        if v < 1.:
            raise ValueError('dtlong must be greater or equal to 1')
        return v

    @validator('frqanl')
    def multiple_of_dtlong(cls, v, values):
        if v % values['dtlong'] != 0.:
            raise ValueError('frqanl is not a multiple of dtlong')
        return v


def test_pydantic_validation():
    ramsin = RamsinModel(
        dtlong=3,
        frqanl=6
    )
    print(ramsin)


test_pydantic_validation()