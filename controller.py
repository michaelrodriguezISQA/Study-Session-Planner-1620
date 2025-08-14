from model import Model


class Controller:
    """
    The Controller class handles the interaction between the Model and the View.
    It processes user input from the GUI and updates the Model accordingly.
    """
    def __init__(self, model, view):
        """
        Initializes the Controller with a Model and a View.

        Args:
            model (Model): The data model for the application.
            view (View): The user interface view.
        """
        self.model = model
        self.view = view
        self.view.setup_table_with_data(self.model.get_data())
        self.view.save_button.clicked.connect(self.save_data)
        self.view.update_button.clicked.connect(self.update_data_from_gui)

    def save_data(self):
        """
        Saves the data from the model to the CSV file.
        """
        self.model.save_to_csv()

    def update_data_from_gui(self):
        """
        Retrieves data from the selected row in the GUI table and
        updates the corresponding row in the model.
        """
        selected_row = self.view.table_widget.currentRow()
        if selected_row > 0:
            new_data = []
            for col in range(self.view.table_widget.columnCount()):
                item = self.view.table_widget.item(selected_row, col)
                new_data.append(item.text())

            self.model.update_row(selected_row, new_data)