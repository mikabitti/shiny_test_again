from shiny import App, ui

from views.animals import animals_ui, animals_server
from views.animals_csv import animals_csv_ui, animals_csv_server
from views.birds import birds_ui, birds_server
from views.financial_data import csv_ui, csv_server


app_ui = ui.page_navbar(
    ui.nav_panel("Animals", animals_ui("animals")),
    ui.nav_panel("Animals (CSV)", animals_csv_ui("animals_csv")),
    ui.nav_panel("Birds", birds_ui("birds")),
    ui.nav_panel("Big CSV", csv_ui("csv")),
    title="Animals & Birds Database",
)


def server(input, output, session):
    animals_server("animals")
    animals_csv_server("animals_csv")
    birds_server("birds")
    csv_server("csv")


app = App(app_ui, server)
