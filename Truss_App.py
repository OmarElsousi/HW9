from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
import sys

# Generated Qt Designer code
from Truss_GUI import Ui_TrussStructuralDesign

# Our controller
from Truss_Classes import TrussController

class MainWindow(Ui_TrussStructuralDesign, qtw.QWidget):
    """
    MainWindow is the top-level widget/class that wires together the UI (from Truss_GUI),
    the TrussController, and user interactions such as file loading and zoom controls.
    """
    def __init__(self):
        """
        Initializes the main window by:
         1) Setting up the UI from the generated designer code.
         2) Creating a TrussController instance.
         3) Connecting UI widgets to controller methods.
         4) Installing an event filter for scene interaction.
         5) Showing the main window.
        """
        super().__init__()
        self.setupUi(self)

        # Force the viewport to propagate hover events (fixes missing tooltips)
        self.gv_Main.viewport().setAttribute(qtc.Qt.WA_Hover, True)
        self.gv_Main.setMouseTracking(True)

        # Create the controller and assign the relevant display widgets
        self.controller = TrussController()
        self.controller.setDisplayWidgets(
            (
                self.te_DesignReport,  # QTextEdit for report
                self.le_LinkName,      # QLineEdit for the link name
                self.le_Node1Name,     # QLineEdit for node1 name
                self.le_Node2Name,     # QLineEdit for node2 name
                self.le_LinkLength,    # QLineEdit for link length
                self.gv_Main           # QGraphicsView for drawing
            )
        )

        # Install the event filter so we can intercept scene events
        self.controller.installSceneEventFilter(self)

        # Connect GUI events to their corresponding functions
        self.btn_Open.clicked.connect(self.OpenFile)
        self.spnd_Zoom.valueChanged.connect(self.setZoom)

        # Finally, show the main window
        self.show()

    def setZoom(self):
        """
        Sets the zoom level of the QGraphicsView to the value of spnd_Zoom.
        Resets the view transform before applying the new scale factor.
        """
        self.gv_Main.resetTransform()
        self.gv_Main.scale(self.spnd_Zoom.value(), self.spnd_Zoom.value())

    def eventFilter(self, obj, event):
        """
        Handles events passing through the filter, specifically for the QGraphicsScene.

        Parameters:
        -----------
        obj : QObject
            The object generating the event.
        event : QEvent
            The event to filter.

        Returns:
        --------
        bool
            True if the event is consumed by the controller, otherwise passes it onward.
        """
        # Check if this event is coming from the scene, then let the controller process it
        if self.controller.isSceneObject(obj):
            consumed, info = self.controller.handleSceneEvent(event, self.gv_Main)
            if info is not None:
                # Display mouse position or any info returned by the controller
                self.lbl_MousePos.setText(info)
            if consumed:
                # If the controller fully handled it, don't pass it to parent
                return True
        return super().eventFilter(obj, event)

    def OpenFile(self):
        """
        Opens a file dialog, reads the selected file line by line, and hands the data off
        to the TrussController for parsing and updating the truss model.
        """
        filename = qtw.QFileDialog.getOpenFileName()[0]
        if not filename:
            return  # User canceled file selection
        self.te_Path.setText(filename)
        with open(filename, 'r') as f:
            data = f.readlines()
        # Let the controller parse the file data
        self.controller.ImportFromFile(data)


def Main():
    """
    The main entry point of the application, which:
     1) Creates a QApplication.
     2) Instantiates the MainWindow.
     3) Runs the application event loop.
    """
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    Main()
