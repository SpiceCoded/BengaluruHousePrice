import json
import pickle
import numpy as np

__data_columns = None
__model = None
__others = None

def load_artifacts():
    global __data_columns, __model, __others
    if __data_columns is not None:
        return

    with open(r'A:\code\real_estate\server\artifacts\columns.json', 'r', encoding='utf-8') as f:
        all_columns = json.load(f)
    with open(r'A:\code\real_estate\server\artifacts\output.json', 'r', encoding='utf-8') as f:
        others = json.load(f)

    with open(r'A:\code\real_estate\server\artifacts\model.pkl', 'rb') as f:
        __model = pickle.load(f)

    expected = __model.n_features_in_  
    print(f"Model expects {expected} features")

    __data_columns = all_columns[:expected]
    __others = others
    print(f"Using first {len(__data_columns)} columns")
    print("First 12 columns:", __data_columns[:12])
    print("Sample area types:", __data_columns[7:10])
    print("is_ready index:", __data_columns.index("is_ready") if "is_ready" in __data_columns else "Not found!")

load_artifacts()

def predict_price(total_sqft, bath, balcony, bhk, area_type, is_ready, location):
    x = np.zeros(len(__data_columns))

    x[0] = total_sqft
    x[1] = bath
    x[2] = balcony
    x[4] = bhk                              
    x[5] = total_sqft / bhk                  

    if "is_ready" in __data_columns:
        x[__data_columns.index("is_ready")] = 1 if is_ready else 0

    area_type = area_type.strip()
    possible_areas = ["Carpet  Area", "Plot  Area", "Super built-up  Area"]
    possible_areas = [x.strip() for x in possible_areas]
    if area_type in possible_areas and area_type in __data_columns:
        x[__data_columns.index(area_type)] = 1

    if location in __data_columns:
        x[__data_columns.index(location)] = 1
    elif location in __others:
        pass
    else : raise Exception

    
    price = __model.predict([x])[0]
    return round(price, 2)

def get_location_names():
    return __data_columns[12:]
