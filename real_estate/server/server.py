from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from util import get_location_names, predict_price
from house import house


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def greet():
    return 'hello world'

@app.get('/locations')
async def get_locations():
    locations = get_location_names()
    return {"locations": locations}   

@app.post('/estimate')
async def estimate(house: house):
    price = predict_price(
        area_type=house.area_type,
        total_sqft=house.total_sqft,
        bath=house.bath,
        balcony=house.balcony,
        bhk=house.bhk,
        is_ready=house.is_ready,
        location=house.location
    )
    return {"estimated_price": round(price, 2)} 
    