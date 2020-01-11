import sys
import base64
import requests

from PyQt5.QtWidgets import QMainWindow, QApplication

from client.view.MyView import Ui_MainWindow

exitCode = ""


class Controller(QMainWindow):
    """
        Controller for the programm, adding events to the ui and managing the implementation of the API calls
    """
    def __init__(self, parent = None):
        super().__init__(parent)

        self.myForm = Ui_MainWindow()
        self.myForm.setupUi(self)
        self.apiurl = "http://localhost:8080/detectLang"

        self.myForm.reset.clicked.connect(self.reset_fields)
        self.myForm.close.clicked.connect(self.exit_programm)
        self.myForm.check.clicked.connect(self.send_request)

    def exit_programm(self):
        """
        Exits the program with the exit code
        :return:
        """
        sys.exit(exitCode)

    def reset_fields(self):
        """
        Resets the fields in the ui with default values
        :return: void
        """
        self.myForm.text_input.setText("")
        self.myForm.text_output.setText("")

    def send_request(self):
        """
        Sends a request to a localhost webservice (localhost:8080)
        :return: void
        """
        b64_encoded_string = str(base64.urlsafe_b64encode(self.myForm.text_input.toPlainText().encode("utf-8")), "utf-8")
        params = {"text": b64_encoded_string}
        try:
            resp = requests.get(self.apiurl, params)
            if resp.status_code == 200:
                self.myForm.text_output.setText(format_response(resp))
            else:
                self.myForm.text_output.setText("<b>Error with webservice.</b>")
        except Exception:
            print()
            self.myForm.text_output.setText("<b>Error with webservice.</b>")



def format_response(response):
    """
    Formats the Request Return Object into HTML Text for the UI
    :param response: Requests response
    :return: HTML Formatted String
    """
    response = response.json()
    output = ""

    output += "reliable: "
    if response["reliable"]:
        output += "<b>yes</b><br>"
    else:
        output += "<b>no</b><br>"

    output += "language: "
    output += "<b>" + str(response["language"]).upper() + "</b><br>"

    output += "probability: "
    output += "<b>" + str(response["prob"]) + "%</b>"

    return output


if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = Controller()
    c.show()
    exitCode = app.exec_()
