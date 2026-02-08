import pandas as pd
from shiny import module, ui, render, reactive

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


@module.ui
def animals_ui():
    return ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "habitat",
                "Filter by Living Area:",
                choices=["All"] + sorted(animals_df['Living Area'].unique().tolist())
            ),
            ui.input_slider(
                "min_speed",
                "Minimum Speed (km/h):",
                min=0,
                max=int(animals_df['Speed (km/h)'].max()),
                value=0
            ),
            ui.input_slider(
                "max_weight",
                "Maximum Weight (kg):",
                min=0,
                max=int(animals_df['Weight (kg)'].max()),
                value=int(animals_df['Weight (kg)'].max())
            ),
        ),
        ui.output_data_frame("data_table"),
        ui.output_text("stats")
    )


@module.server
def animals_server(input, output, session):
    @reactive.Calc
    def filtered_df():
        df = animals_df.copy()

        if input.habitat() != "All":
            df = df[df['Living Area'] == input.habitat()]

        df = df[df['Speed (km/h)'] >= input.min_speed()]
        df = df[df['Weight (kg)'] <= input.max_weight()]

        return df

    @render.data_frame
    def data_table():
        return filtered_df()

    @render.text
    def stats():
        return f"Showing {len(filtered_df())} of {len(animals_df)} animals"
