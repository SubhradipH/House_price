import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location,sqft,bhk,bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2)

def get_location_names():
    return __locations

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    # Ensure these paths are correct relative to where you run your Flask app
    # For example, if 'app.py' is in the same directory as 'artifacts', then 'artifacts/columns.json' is correct.
    try:
        with open("artifacts/columns.json", 'r') as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[3:]

        with open("artifacts/banglore_home_prices_model.pickle", 'rb') as f:
            __model = pickle.load(f)

        print("loading saved artifacts...done")
    except FileNotFoundError as e:
        print(f"Error loading artifacts: {e}. Make sure 'artifacts' directory and files are in the correct path.")
        # You might want to exit or raise the error further here
    except Exception as e:
        print(f"An unexpected error occurred during artifact loading: {e}")

# Call load_saved_artifacts directly when the module is imported
# This ensures that __locations and __model are populated when Flask app starts
load_saved_artifacts()

if __name__=='__main__':
    # This block will still run if you execute util.py directly,
    # but the artifacts will already be loaded from the call above.
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar',1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2)) # other location
    print(get_estimated_price('Ejipura', 1000, 2, 2))  # other location