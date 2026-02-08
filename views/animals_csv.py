import pandas as pd
from pathlib import Path
from shiny import module, ui, render, reactive
from constants import STATUS_COLORS
import json

csv_path = Path(__file__).parent.parent / "animals.csv"

json_path = Path(__file__).parent.parent / "animals_status.json"

@module.ui
def animals_csv_ui():
    return ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "habitat",
                "Filter by Living Area:",
                choices=["All"]
            ),
            ui.input_slider(
                "min_speed",
                "Minimum Speed (km/h):",
                min=0,
                max=1,
                value=0
            ),
            ui.input_slider(
                "max_weight",
                "Maximum Weight (kg):",
                min=0,
                max=1,
                value=1
            ),
        ),
        ui.output_data_frame("data_table"),
        ui.output_text("stats")
    )


@module.server
def animals_csv_server(input, output, session):
    @reactive.file_reader(csv_path)
    def read_csv():
        return pd.read_csv(csv_path)
    
    @reactive.file_reader(json_path)
    def row_status() -> dict:
        with open(json_path, 'r') as f:
            data = json.load(f)
            print(f"Data loaded from {json_path}")
        return data

    @reactive.effect
    def update_controls():
        df = read_csv()
        habitats = ["All"] + sorted(df['Living Area'].dropna().unique().tolist())
        ui.update_select("habitat", choices=habitats)
        ui.update_slider("min_speed", max=int(df['Speed (km/h)'].max()))
        ui.update_slider("max_weight",
                         max=int(df['Weight (kg)'].max()),
                         value=int(df['Weight (kg)'].max()))

    @reactive.Calc
    def filtered_df():
        df = read_csv()

        if input.habitat() != "All":
            df = df[df['Living Area'] == input.habitat()]

        df = df[df['Speed (km/h)'] >= input.min_speed()]
        df = df[df['Weight (kg)'] <= input.max_weight()]

        return df

    def build_styles():
        statuses = row_status()

        # Group rows by status for styling
        styles = []
        for status, color in STATUS_COLORS.items():
            rows = statuses.get(status, [])
            if rows:
                styles.append({
                    "rows": rows,
                    "style": {"background-color": color},
                })

        return styles

    @render.data_frame
    def data_table():
        return render.DataTable(filtered_df(), styles=build_styles())

    @render.text
    def stats():
        return f"Showing {len(filtered_df())} of {len(read_csv())} animals"
