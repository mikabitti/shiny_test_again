import pandas as pd
# Animals data
animals_data = {
    'Animal': ['Cheetah', 'Lion', 'Elephant', 'Giraffe', 'Tiger', 'Gorilla',
               'Polar Bear', 'Penguin', 'Eagle', 'Dolphin', 'Sloth', 'Kangaroo'],
    'Speed (km/h)': [120, 80, 40, 60, 65, 40, 40, 10, 160, 60, 0.27, 70],
    'Weight (kg)': [72, 190, 6000, 1200, 220, 160, 450, 35, 6.5, 150, 5, 85],
    'Living Area': ['Savanna', 'Savanna', 'Savanna', 'Savanna', 'Jungle', 'Jungle',
                    'Arctic', 'Antarctic', 'Mountains', 'Ocean', 'Jungle', 'Grassland']
}

animals_df = pd.DataFrame(animals_data)
animals_df.to_csv("animals.csv", index=False)