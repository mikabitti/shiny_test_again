import pandas as pd
from pathlib import Path
from shiny import module, ui, render, reactive
from constants import STATUS_COLORS
from process import process_fina_data
import json

csv_path = Path(__file__).parent.parent / "data" / "annual-enterprise-survey-2024-financial-year-provisional-size-bands.csv"

json_path = Path(__file__).parent.parent / "row_status.json"



@module.ui
def csv_ui():
    return ui.layout_sidebar(
        ui.sidebar(
            ui.input_numeric("row_number", "Row to scroll to:", value=1, min=1),
            ui.input_action_button("scroll_btn", "Scroll to Row"),
            ui.input_action_button("process", "Process Data"),
        ),
        ui.output_data_frame("data_table"),
        ui.tags.script("""
            Shiny.addCustomMessageHandler('scrollToRow', function(data) {
                console.log('Received scroll message:', data);
                
                const rowIndex = data.row;
                const tableId = data.table_id;
                
                console.log('Looking for table with ID:', tableId);
                const tableContainer = document.getElementById(tableId);
                
                if (tableContainer) {
                    console.log('Found container');
                    const table = tableContainer.querySelector('table');
                    
                    if (table) {
                        const tbody = table.querySelector('tbody');
                        if (tbody && tbody.rows[rowIndex]) {
                            const row = tbody.rows[rowIndex];
                            row.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            
                            // Highlight the row
                            const originalBg = row.style.backgroundColor;
                            row.style.backgroundColor = '#ffff99';
                            setTimeout(function() {
                                row.style.backgroundColor = originalBg;
                            }, 1000);
                        } else {
                            console.log('Row not found at index:', rowIndex);
                        }
                    } else {
                        console.log('Table element not found');
                    }
                } else {
                    console.log('Container not found with ID:', tableId);
                }
            });
        """)
    )


@module.server
def csv_server(input, output, session):
    @reactive.file_reader(csv_path)
    def read_csv():
        return pd.read_csv(csv_path)
    
    @reactive.file_reader(json_path)
    def row_status() -> dict:
        with open(json_path, 'r') as f:
            data = json.load(f)
            print(f"Data loaded from {json_path}")
        return data



    @reactive.Calc
    def filtered_df():
        df = read_csv()

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

    @reactive.effect
    @reactive.event(input.scroll_btn)
    async def scroll_to_row():
        row_idx = input.row_number() - 1
        # Pass the namespaced ID
        await session.send_custom_message('scrollToRow', {
            'row': row_idx,
            'table_id': session.ns('data_table')
        })

    @reactive.effect
    @reactive.event(input.process)
    def start_processing():
        df: pd.DataFrame = filtered_df()
        df.to_pickle("fina_data.pkl")