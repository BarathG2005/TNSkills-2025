from pydantic import BaseModel
class (BaseModel):
    name: str
    category: str
    value: float
    status: str

class AssetCreate(AssetBase):
    pass

class AssetUpdate(AssetBase):
    pass
