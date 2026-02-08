import pandas as pd
import queue
import threading
from shiny import module, ui, render, reactive
from process import process_data

# Birds data
birds_data = {
    'Animal': ['Bald Eagle', 'Hummingbird', 'Ostrich', 'Penguin', 'Peregrine Falcon',
               'Albatross', 'Owl', 'Parrot', 'Flamingo', 'Condor', 'Peacock', 'Woodpecker'],
    'Speed (km/h)': [160, 80, 70, 10, 390, 127, 65, 40, 60, 88, 16, 25],
    'Weight (kg)': [6.5, 0.004, 135, 35, 1.5, 8.5, 2.5, 1.2, 3.5, 15, 6, 0.075],
    'Living Area': ['Mountains', 'Forest', 'Savanna', 'Antarctic', 'Mountains',
                    'Ocean', 'Forest', 'Jungle', 'Wetlands', 'Mountains', 'Forest', 'Forest']
}

birds_df = pd.DataFrame(birds_data)


@module.ui
def birds_ui():
    return ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "habitat",
                "Filter by Living Area:",
                choices=["All"] + sorted(birds_df['Living Area'].unique().tolist())
            ),
            ui.input_slider(
                "min_speed",
                "Minimum Speed (km/h):",
                min=0,
                max=int(birds_df['Speed (km/h)'].max()),
                value=0
            ),
            ui.input_slider(
                "max_weight",
                "Maximum Weight (kg):",
                min=0,
                max=int(birds_df['Weight (kg)'].max()),
                value=int(birds_df['Weight (kg)'].max())
            ),
            ui.input_action_button("process", "Process Data"),
        ),
        ui.output_data_frame("data_table"),
        ui.output_text("stats")
    )


STATUS_COLORS = {
    "success": "#90EE90",  # Light green
    "warning": "#FFE4B5",  # Moccasin/light orange
    "error": "#FFB6C1",    # Light pink
}


@module.server
def birds_server(input, output, session):
    # Dict mapping row index -> status
    processed_rows = reactive.Value({})
    result_queue = queue.Queue()
    is_processing = reactive.Value(False)

    @reactive.Calc
    def filtered_df():
        df = birds_df.copy()

        if input.habitat() != "All":
            df = df[df['Living Area'] == input.habitat()]

        df = df[df['Speed (km/h)'] >= input.min_speed()]
        df = df[df['Weight (kg)'] <= input.max_weight()]

        return df

    def run_processing(df):
        """Runs in background thread, puts results into queue."""
        for i, row, status in process_data(df):
            result_queue.put((i, status))
        result_queue.put(None)  # Signal completion

    @reactive.effect
    @reactive.event(input.process)
    def start_processing():
        processed_rows.set({})
        # Clear any old items from queue
        while not result_queue.empty():
            try:
                result_queue.get_nowait()
            except queue.Empty:
                break
        is_processing.set(True)
        # Start background thread
        thread = threading.Thread(target=run_processing, args=(filtered_df(),))
        thread.daemon = True
        thread.start()

    @reactive.effect
    def poll_results():
        if not is_processing.get():
            return

        # Check queue for new results
        updated = False
        current = processed_rows.get().copy()
        done = False
        while not result_queue.empty():
            try:
                result = result_queue.get_nowait()
                if result is None:  # Processing complete
                    done = True
                    break
                i, status = result
                current[i] = status
                updated = True
            except queue.Empty:
                break

        if updated or done:
            processed_rows.set(current)

        if done:
            is_processing.set(False)
            return

        # Keep polling while processing
        reactive.invalidate_later(0.1)

    @render.data_frame
    def data_table():
        df = filtered_df()
        processed = processed_rows.get()

        # Group rows by status for styling
        styles = []
        for status, color in STATUS_COLORS.items():
            rows = [i for i, s in processed.items() if s == status]
            if rows:
                styles.append({
                    "rows": rows,
                    "style": {"background-color": color},
                })

        return render.DataTable(df, styles=styles)

    @render.text
    def stats():
        return f"Showing {len(filtered_df())} of {len(birds_df)} birds"
