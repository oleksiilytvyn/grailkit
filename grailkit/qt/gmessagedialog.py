# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gmessagedialog
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Replacement for default OS message dialog
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from grailkit.qt import GDialog
from grailkit.util import OS_MAC


class GMessageDialog(GDialog):
    """Message dialog, replacement of a default dialog"""

    # default icons
    NoIcon = 0
    Information = 1
    Warning = 2
    Critical = 3
    Question = 4

    # enum of all available standard icons
    Icon = (NoIcon, Information, Warning, Critical, Question)

    # button role
    InvalidRole = -1
    AcceptRole = 0
    RejectRole = 1
    DestructiveRole = 2
    ActionRole = 3
    HelpRole = 4
    YesRole = 5
    NoRole = 6
    ApplyRole = 7
    ResetRole = 8

    # enum of button roles
    Role = (InvalidRole, AcceptRole, RejectRole, DestructiveRole, ActionRole,
            HelpRole, YesRole, NoRole, ApplyRole, ResetRole)

    # standard buttons
    Ok = 1
    Open = 2
    Save = 3
    Cancel = 4
    Close = 5
    Discard = 6
    Apply = 7
    Reset = 8
    RestoreDefaults = 9
    Help = 10
    SaveAll = 11
    Yes = 12
    YesToAll = 13
    No = 14
    NoToAll = 15
    Abort = 16
    Retry = 17
    Ignore = 18
    NoButton = 19

    StandardButton = (Ok, Open, Save, Cancel, Close, Discard, Apply, Reset, RestoreDefaults, Help,
                      SaveAll, Yes, YesToAll, No, NoToAll, Abort, Retry, Ignore, NoButton)

    StandardButtonRoleName = {
        1: (AcceptRole, "Ok"),
        2: (AcceptRole, "Open"),
        3: (AcceptRole, "Save"),
        4: (RejectRole, "Cancel"),
        5: (RejectRole, "Close"),
        6: (DestructiveRole, "Discard"),
        7: (ApplyRole, "Apply"),
        8: (ResetRole, "Reset"),
        9: (ResetRole, "Restore Defaults"),
        10: (HelpRole, "Help"),
        11: (AcceptRole, "Save All"),
        12: (YesRole, "Yes"),
        13: (YesRole, "Yes to All"),
        14: (NoRole, "No"),
        15: (NoRole, "No to All"),
        16: (RejectRole, "Abort"),
        17: (AcceptRole, "Retry"),
        18: (AcceptRole, "Ignore"),
        19: (NoButton, "Button")
        }

    buttonClicked = pyqtSignal(object)

    def __init__(self, parent=None,
                 title="Primary text providing basic information and a suggestion",
                 text="Secondary text providing further details. Also includes information "
                      "that explains any unobvious consequences of actions.",
                 icon=None,
                 buttons=[]):
        """Initialize a message dialog"""

        super(GMessageDialog, self).__init__(parent)

        self._title = title
        self._text = text
        self._icon = None
        self._buttons = []

        self.__ui__()

        self.setIcon(icon)
        self.setStandardButtons(buttons)

    def __ui__(self):
        """Create ui components"""

        self._ui_icon = QLabel(self)
        self._ui_icon.setAlignment(Qt.AlignCenter)
        self._ui_icon.setGeometry(20, 18, 64, 64)

        self._ui_title = QLabel(self._title)
        self._ui_title.setObjectName("g_message_title")
        self._ui_title.setWordWrap(True)
        self._ui_title.setIndent(88)

        self._ui_text = QLabel(self._text)
        self._ui_text.setObjectName("g_message_text")
        self._ui_text.setWordWrap(True)
        self._ui_text.setIndent(88)

        self._ui_buttons_layout = QBoxLayout(QBoxLayout.LeftToRight)
        self._ui_buttons_layout.setSpacing(6)
        self._ui_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self._ui_buttons_layout.addStretch(1)

        self._ui_buttons = QWidget(self)
        self._ui_buttons.setLayout(self._ui_buttons_layout)

        self._ui_layout = QVBoxLayout()
        self._ui_layout.setContentsMargins(12, 24, 12, 8)

        self._ui_layout.addWidget(self._ui_title, 0, Qt.AlignTop)
        self._ui_layout.addWidget(self._ui_text, 1, Qt.AlignTop)
        self._ui_layout.addWidget(self._ui_buttons, 0, Qt.AlignBottom)

        self.setLayout(self._ui_layout)
        self.setWindowTitle(self._title if not OS_MAC else "")
        self.setMinimumSize(420, 80)
        self._update_size()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)

    def title(self):
        """Get a dialog title"""

        return self._title

    def text(self):
        """Get a dialog text"""

        return self._text

    def icon(self):
        """Get a icon of dialog"""

        return QIcon(self._icon)

    def setTitle(self, title):
        """Set dialog title

        Args:
            title (str): title
        """

        self._title = title
        self._ui_title.setText(self._title)

    def setText(self, text):
        """Text displayed in dialog

        Args:
            text (str): informative text
        """

        self._text = text
        self._ui_text.setText(self._text)

    def setIcon(self, icon):
        """Set dialog icon

        Args:
            icon (QIcon, QPixmap): icon of dialog
        """

        size = 56

        # pick a standard icon
        if icon in GMessageDialog.Icon:
            standard_icon = QStyle.SP_MessageBoxInformation

            if icon == GMessageDialog.Information:
                standard_icon = QStyle.SP_MessageBoxInformation
            elif icon == GMessageDialog.Question:
                standard_icon = QStyle.SP_MessageBoxQuestion
            elif icon == GMessageDialog.Warning:
                standard_icon = QStyle.SP_MessageBoxWarning
            elif icon == GMessageDialog.Critical:
                standard_icon = QStyle.SP_MessageBoxCritical

            icon = QApplication.style().standardIcon(standard_icon)

        if isinstance(icon, QIcon):
            self._icon = icon.pixmap(size)

        if isinstance(icon, QPixmap):
            self._icon = icon.scaledToWidth(size)

        self._ui_icon.setPixmap(self._icon)

    def buttons(self):
        """Returns a list of all the buttons that have been added to the message box.
        """

        return [item[3] for item in self._buttons]

    def button(self, button):
        """Returns a pointer corresponding to the standard button which,
        or 0 if the standard button doesn't exist in this message box.
        """
        for item in self._buttons:
            if item[2] == button:
                return item[3]

        return 0

    def buttonRole(self, button):
        """Returns the button role for the specified button. This function returns
        InvalidRole if button is 0 or has not been added to the message box.
        """

        for item in self._buttons:
            if item[3] == button:
                return item[2]

        return GMessageDialog.InvalidRole

    def addButton(self, button, role=None):

        name = "Untitled"

        if isinstance(button, str):
            name = button
            value = -1
        elif button in GMessageDialog.StandardButton:
            name = GMessageDialog.StandardButtonRoleName[button][1]
            role = GMessageDialog.StandardButtonRoleName[button][0]
            value = button
        elif isinstance(button, QPushButton):
            name = button.text()
            value = -1
        else:
            raise Exception("Invalid argument passed")

        def triggered(cls, btn):

            def fn(falg):
                cls._button_clicked(btn)

            return fn

        if isinstance(button, QPushButton):
            btn = button
        else:
            btn = QPushButton(name)

        btn.role = role
        btn.clicked.connect(triggered(self, btn))

        self._buttons.append((name, value, role, btn))
        self._ui_buttons_layout.addWidget(btn)
        self._update_size()

    def setStandardButtons(self, buttons):
        """Set a standard buttons"""

        if not buttons:
            return

        for button in buttons:
            if button not in GMessageDialog.StandardButton:
                raise Exception("Button type is not standard")

            self.addButton(button)

    def _button_clicked(self, button):
        """"""

        self.buttonClicked.emit(button)

    def _update_size(self):
        self.adjustSize()
        self.setFixedSize(self.size().width(), self.size().height())

    @staticmethod
    def warning(parent=None, title="Warning", text=""):
        """Warning dialog"""

        buttons = [GMessageDialog.Ok]

        return GMessageDialog(parent, title, text, GMessageDialog.Warning, buttons)

    @staticmethod
    def critical(parent=None, title="Critical Problem", text=""):
        """Warning dialog"""

        buttons = [GMessageDialog.Ok]

        return GMessageDialog(parent, title, text, GMessageDialog.Critical, buttons)


    @staticmethod
    def question(parent=None, title="Are you sure?", text=""):
        """Warning dialog"""

        buttons = [GMessageDialog.Ok]

        return GMessageDialog(parent, title, text, GMessageDialog.Question, buttons)


    @staticmethod
    def information(parent=None, title="Information", text=""):
        """Warning dialog"""

        buttons = [GMessageDialog.Ok]

        return GMessageDialog(parent, title, text, GMessageDialog.Information, buttons)


# test a dialog
if __name__ == '__main__':
    import sys
    from grailkit.qt import GApplication

    def clicked(btn):
        print(btn)
        print(btn.text())

    app = GApplication(sys.argv)

    btn = QPushButton("Destruct")
    btn.setStyleSheet("background: red;color: white;")

    win = GMessageDialog(icon=GMessageDialog.Critical)
    win.buttonClicked.connect(clicked)
    win.addButton(btn, GMessageDialog.DestructiveRole)
    win.setStandardButtons([GMessageDialog.Yes, GMessageDialog.No, GMessageDialog.Help])
    win.show()

    sys.exit(app.exec_())
