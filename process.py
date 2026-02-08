import pandas as pd
import time
import json

def save_to_json(data, filename):
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filename: Path to the JSON file
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")

def load_from_json(filename):
    """
    Load data from a JSON file.
    
    Args:
        filename: Path to the JSON file
    
    Returns:
        Dictionary loaded from the file
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    print(f"Data loaded from {filename}")
    return data






def process_data(df: pd.DataFrame):
    """Generator that yields (index, row, status) after processing each row.

    Status can be: "success", "warning", "error"
    """
    data = df.to_dict(orient='records')
    for i, row in enumerate(data):
        first_key = list(row.keys())[0]
        time.sleep(1)  # simulate processing

        # Example logic: status based on some condition
        speed = row.get('Speed (km/h)', 0)
        if speed > 100:
            status = "success"
        elif speed > 50:
            status = "warning"
        else:
            status = "error"

        print(f"{row[first_key]} processed - {status}")
        yield i, row, status

def process_fina_data(df: pd.DataFrame):
    """Generator that yields (index, row, status) after processing each row.

    Status can be: "success", "warning", "error"
    """
    data = df.to_dict(orient='records')
    for i, row in enumerate(data):
        #first_key = list(row.keys())[0]
        time.sleep(2)  # simulate processing

        # Example logic: status based on some condition
        try:
            value = int(row.get('value', 0))
            if value >= 2000:
                status = "success"
            elif value < 2000:
                status = "warning"
        except Exception as e:
            status = "error"

        print(f"Row: {i} processed - {status}")
        #yield i, row, status
        data = load_from_json("row_status.json")
        data[status].append(i)
        save_to_json(data, "row_status.json")


if __name__ == "__main__":
    # # Birds data
    # birds_data = {
    #     'Animal': ['Bald Eagle', 'Hummingbird', 'Ostrich', 'Penguin', 'Peregrine Falcon',
    #             'Albatross', 'Owl', 'Parrot', 'Flamingo', 'Condor', 'Peacock', 'Woodpecker'],
    #     'Speed (km/h)': [160, 80, 70, 10, 390, 127, 65, 40, 60, 88, 16, 25],
    #     'Weight (kg)': [6.5, 0.004, 135, 35, 1.5, 8.5, 2.5, 1.2, 3.5, 15, 6, 0.075],
    #     'Living Area': ['Mountains', 'Forest', 'Savanna', 'Antarctic', 'Mountains',
    #                     'Ocean', 'Forest', 'Jungle', 'Wetlands', 'Mountains', 'Forest', 'Forest']
    # }


    # df = pd.DataFrame(birds_data)

    # for i, row, status in process_data(df):
    #     pass  # Generator handles printing
    data_pkl = "fina_data.pkl"
    df: pd.DataFrame = pd.read_pickle(data_pkl)
    process_fina_data(df) 