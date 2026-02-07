from pydantic import BaseModel

class VehicleCreate(BaseModel):
    number: str
    type: str
    owner_name: str

class VehicleResponse(VehicleCreate):
    id: int

    model_config = {
        "from_attributes": True,
    }

