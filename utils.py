from PyQt5.QtWidgets import QTextEdit

def format_lots_input(self: QTextEdit):
    text = self.text_input.toPlainText().replace(".1\n", ";")
    text = text.replace(".1\r\n", ";")
    text = text.replace(".1",";")
    self.text_input.setPlainText(text)