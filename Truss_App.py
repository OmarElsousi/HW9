from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
import sys

# Generated Qt Designer code
from Truss_GUI import Ui_TrussStructuralDesign

# Our controller
from Truss_Classes import TrussController

class MainWindow(Ui_TrussStructuralDesign, qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # ✅ Force the viewport to propagate hover events (fix for tooltip display)
        self.gv_Main.viewport().setAttribute(qtc.Qt.WA_Hover, True)
        self.gv_Main.setMouseTracking(True)

        # Create the controller and wire up the UI widgets
        self.controller = TrussController()
        self.controller.setDisplayWidgets(
            (
                self.te_DesignReport,
                self.le_LinkName,
                self.le_Node1Name,
                self.le_Node2Name,
                self.le_LinkLength,
                self.gv_Main
            )
        )
        # Install the event filter via the controller
        self.controller.installSceneEventFilter(self)

        # GUI events
        self.btn_Open.clicked.connect(self.OpenFile)
        self.spnd_Zoom.valueChanged.connect(self.setZoom)

        self.show()

    def setZoom(self):
        # Zoom the QGraphicsView without calling the view directly
        self.gv_Main.resetTransform()
        self.gv_Main.scale(self.spnd_Zoom.value(), self.spnd_Zoom.value())

    def eventFilter(self, obj, event):
        # Pass scene events to the controller
        if self.controller.isSceneObject(obj):
            consumed, info = self.controller.handleSceneEvent(event, self.gv_Main)
            if info is not None:
                # Display the string returned by controller
                self.lbl_MousePos.setText(info)
            if consumed:
                return True
        return super().eventFilter(obj, event)

    def OpenFile(self):
        filename = qtw.QFileDialog.getOpenFileName()[0]
        if not filename:
            return
        self.te_Path.setText(filename)
        with open(filename, 'r') as f:
            data = f.readlines()
        # Let the controller parse file data
        self.controller.ImportFromFile(data)


def Main():
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    Main()
