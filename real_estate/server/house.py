from pydantic import BaseModel

class house(BaseModel):
    total_sqft : int
    bath:int
    balcony:int
    bhk:int 
    area_type: str
    is_ready:bool 
    location :str