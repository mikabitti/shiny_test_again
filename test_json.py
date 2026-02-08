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


if __name__ == "__main__":
# Example usage:
    data_old = {
        "row_status": ["success", "warning", "error", "success", "success", 
                    "warning", "error", "success", "success", "error"]
    }

    data = {
        "status": {
            "Dog" : "success",
            "Polar Bear" : "warning"
            }
    }

    data = {
        "success": [ 1, 2],
        "warning": [ 3, 7],
        "error" : [8]
    }

    animal_json = 'animals_status.json'

    # Save to file
    save_to_json(data, animal_json)

    # Load from file
    row_status = load_from_json(animal_json)
    print(row_status)

    # # Group rows by status for styling
    # styles = []
    # rows = [1,2]
    # for key in row_status['status'].keys():
    #     df[df['status'] == 'active'].index.tolist()


    financial_data = {
        "success": [ 1, 2],
        "warning": [ 3, 7],
        "error" : [8]
    }

    empty = {
    "success": [ ],
    "warning": [ ],
    "error" : [ ]
    }

    save_to_json(data, "row_status.json")