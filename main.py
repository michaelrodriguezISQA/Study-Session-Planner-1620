import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import QDate, QTimer
from gui import Ui_MainWindow
from model import StudySession, save_session, load_sessions, filter_sessions_by_date, update_session

class StudyApp(QMainWindow):
    """
    Main application class for the Study Session Planner.
    This class handles the main application logic, connecting the user interface
    with the data model to manage study sessions.
    """
    def __init__(self):
        """
        Initializes the StudyApp window and sets up UI and connections.
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.selected_row = None
        load_sessions()
        self.ui.AddSessionPushButton.clicked.connect(self.add_or_update_session)
        self.ui.ClearPushButton.clicked.connect(self.clear_form)
        self.ui.CalendarWidget.clicked.connect(self.show_calendar_sessions)
        self.ui.TableWidget.cellClicked.connect(self.load_session_into_form)
        self.show_all_sessions()

    def add_or_update_session(self):
        """
        Adds a new study session or updates an existing one.

        It validates user input and displays error messages for missing
        subject or a duration of zero. If the input is valid, it either
        creates a new session or updates the selected one, then refreshes
        the UI and clears the form.
        """
        self._clear_highlights()

        subject = self.ui.SubjectLineEdit.text()
        date = self.ui.DateEdit.date().toString("yyyy-MM-dd")
        duration = self.ui.SpinBox.value()
        notes = self.ui.NotesTextEdit.toPlainText()

        has_error = False
        if not subject:
            self.ui.SubjectErrorLabel.setText("Subject is required.")
            has_error = True
        if duration == 0:
            self.ui.DurationErrorLabel.setText("Duration must be greater than 0.")
            has_error = True
        if has_error:
            QMessageBox.warning(self, "Missing Info", "Please correct the highlighted errors.")
            return

        session = StudySession(subject, date, duration, notes)
        if self.selected_row is not None:
            update_session(self.selected_row, session)
            self.selected_row = None
        else:
            save_session(session)

        self.clear_form()
        self.show_all_sessions()

        QTimer.singleShot(2000, self._clear_highlights)

    def show_all_sessions(self):
        """
        Loads and displays all study sessions in the summary table.
        """
        sessions = load_sessions()
        table = self.ui.TableWidget
        self._populate_table(table, sessions)

    def show_calendar_sessions(self, date: QDate):
        """
        Displays sessions for the selected date from the calendar.

        Args:
            date (QDate): The date selected by the user on the calendar.
        """
        selected_date_str = date.toString("yyyy-MM-dd")
        sessions_on_date = filter_sessions_by_date(selected_date_str)

        if sessions_on_date:
            details = f"Sessions on {selected_date_str}:\n"
            for session in sessions_on_date:
                details += f"- {session.subject} ({session.duration} min)\n"
        else:
            details = f"No sessions on {selected_date_str}."

        self.ui.SessionDetailsTextEdit.setText(details)
        self.ui.tabWidget.setCurrentIndex(1)

    def load_session_into_form(self, row, column):
        """
        Loads the data of a selected session from the table into the input form.

        Args:
            row (int): The row index of the selected table cell.
            column (int): The column index of the selected table cell.
        """
        table = self.ui.TableWidget
        self.ui.SubjectLineEdit.setText(table.item(row, 0).text())
        self.ui.DateEdit.setDate(QDate.fromString(table.item(row, 1).text(), "yyyy-MM-dd"))
        self.ui.SpinBox.setValue(int(table.item(row, 2).text()))
        self.ui.NotesTextEdit.setPlainText(table.item(row, 3).text())
        self.selected_row = row

        self.ui.tabWidget.setCurrentIndex(0)

    def _populate_table(self, table, sessions):
        """
        Populates the given table widget with session data.

        Args:
            table (QTableWidget): The table widget to populate.
            sessions (list): A list of StudySession objects.
        """
        sessions.sort(key=lambda s: s.date)

        table.setRowCount(len(sessions))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Subject", "Date", "Duration", "Notes"])

        for i, session in enumerate(sessions):
            table.setItem(i, 0, QTableWidgetItem(session.subject))
            table.setItem(i, 1, QTableWidgetItem(session.date))
            table.setItem(i, 2, QTableWidgetItem(str(session.duration)))
            table.setItem(i, 3, QTableWidgetItem(session.notes))

    def clear_form(self):
        """
        Clears all input fields and resets the form to its default state.
        """
        self.ui.SubjectLineEdit.clear()
        self.ui.DateEdit.setDate(self.ui.CalendarWidget.selectedDate())
        self.ui.SpinBox.setValue(0)
        self.ui.NotesTextEdit.clear()
        self.selected_row = None
        self._clear_highlights()

    def _clear_highlights(self):
        """
        Clears all error messages and resets any highlighted styles.
        """
        self.ui.SubjectErrorLabel.clear()
        self.ui.DurationErrorLabel.clear()
        self.ui.SubjectLineEdit.setStyleSheet("")
        self.ui.SpinBox.setStyleSheet("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudyApp()
    window.show()
    sys.exit(app.exec())