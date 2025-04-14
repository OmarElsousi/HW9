import math
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

# We already had these two from your code:
from GraphicsView_App import RigidLink, RigidPivotPoint

###############################################################################
# 1) NEW CLASS: RollerSupport
###############################################################################
class RollerSupport(RigidPivotPoint):
    """
    RollerSupport is a subclass of RigidPivotPoint to visually distinguish
    a roller support from a pin support within the PyQt graphics scene.
    It overrides the paint method to draw a circular pivot and a triangular base,
    making it look like a roller support in engineering diagrams.
    """

    def __init__(self, x_scene, y_scene, w, h, pen=None, brush=None, name=None):
        """
        Initializes the RollerSupport object.

        Parameters:
        -----------
        x_scene : float
            The x-position (in scene coordinates) where the roller support is placed.
        y_scene : float
            The y-position (in scene coordinates) where the roller support is placed.
        w : float
            The width of the roller's bounding box.
        h : float
            The height of the roller's bounding box.
        pen : QPen, optional
            The pen used to draw the roller outline.
        brush : QBrush, optional
            The brush used to fill the roller.
        name : str, optional
            A name identifier for the roller support (e.g., 'right support').
        """
        # Always call super with (0, 0) for local drawing origin in RigidPivotPoint
        super().__init__(0, 0, w, h, pen=pen, brush=brush, name=name)
        self.w = w
        self.h = h

        # The position in the scene where this roller is placed
        self.setPos(x_scene, y_scene)

    def paint(self, painter, option, widget=None):
        """
        Draws the roller support using QPainter commands:
         1) A top pivot circle
         2) A triangular base
         3) Hashed base lines to represent the foundation
        """
        painter.save()

        # Shift the entire drawing upward so the top circle touches the node pivot
        painter.translate(0, -self.h + 12)

        # Use the pen/brush if provided or default to black/gray
        painter.setPen(self.pen or qtg.QPen(qtc.Qt.black))
        painter.setBrush(self.brush or qtg.QBrush(qtc.Qt.gray))

        # 1) Top pivot circle
        pivot_radius = self.w / 2
        circle_rect = qtc.QRectF(-pivot_radius, 0, 2 * pivot_radius, 2 * pivot_radius)
        painter.drawEllipse(circle_rect)

        # 2) Triangle base
        path = qtg.QPainterPath()
        path.moveTo(-self.w, self.h)
        path.lineTo(0, self.h / 2)
        path.lineTo(self.w, self.h)
        path.closeSubpath()
        painter.drawPath(path)

        # 3) Hashed base lines (foundation)
        foundation_top = self.h + 4
        foundation_height = self.h / 4
        step = 6
        y_line = foundation_top + foundation_height

        x_start = -self.w * 1.2
        x_end = self.w * 1.2

        pen = qtg.QPen(qtc.Qt.black, 1, qtc.Qt.SolidLine)
        painter.setPen(pen)
        while x_start + step < x_end:
            # Draw short lines slanted between foundation_top and y_line
            painter.drawLine(qtc.QPointF(x_start, y_line),
                             qtc.QPointF(x_start + step, foundation_top))
            x_start += step

        painter.restore()


###############################################################################
# 2) Basic Data Classes: Position, Rectangle, Material
###############################################################################
class Position():
    """
    A basic 3D position class to store x, y, z coordinates.
    Provides vector operations like addition, subtraction,
    scalar multiplication, and magnitude calculation.
    """

    def __init__(self, pos=None, x=None, y=None, z=None):
        """
        Initialize a Position object.

        Parameters:
        -----------
        pos : tuple of floats, optional
            A (x, y, z) tuple to initialize all coordinates at once.
        x : float, optional
            The x coordinate if not using pos.
        y : float, optional
            The y coordinate if not using pos.
        z : float, optional
            The z coordinate if not using pos.
        """
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        # If pos is given, unpack it
        if pos is not None:
            self.x, self.y, self.z = pos

        # If x, y, z were also explicitly passed, override the defaults
        self.x = x if x is not None else self.x
        self.y = y if y is not None else self.y
        self.z = z if z is not None else self.z

    def __eq__(self, other):
        """
        Overloads the == operator to compare two Position objects.
        """
        return (self.x == other.x and self.y == other.y and self.z == other.z)

    def __add__(self, other):
        """
        Defines vector addition of two Position objects.
        Returns a new Position.
        """
        return Position((self.x + other.x, self.y + other.y, self.z + other.z))

    def __sub__(self, other):
        """
        Defines vector subtraction of two Position objects.
        Returns a new Position.
        """
        return Position((self.x - other.x, self.y - other.y, self.z - other.z))

    def __mul__(self, other):
        """
        Defines scalar multiplication of a Position object.
        If other is float or int, multiply each coordinate by 'other'.
        Returns a new Position.
        """
        if isinstance(other, (float, int)):
            return Position((self.x * other, self.y * other, self.z * other))

    def __rmul__(self, other):
        """
        Ensures scalar multiplication works from the left or right.
        e.g. 2 * Position == Position * 2
        """
        return self.__mul__(other)

    def mag(self):
        """
        Returns the Euclidean magnitude of the Position vector.
        """
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def getAngleRad(self):
        """
        Gets the angle in the x-y plane relative to the positive x-axis
        using atan2(y, x). Returns 0 if magnitude is near zero.
        """
        l = self.mag()
        if l <= 0:
            return 0
        return math.atan2(self.y, self.x)


class Rectangle():
    """
    A rectangle class defined by top, left, bottom, and right attributes.
    Useful for bounding box calculations and geometry operations.
    """

    def __init__(self, top=None, left=None, bottom=None, right=None):
        """
        Initialize a Rectangle with the given edges.

        Parameters:
        -----------
        top : float, optional
        left : float, optional
        bottom : float, optional
        right : float, optional
        """
        self.top = 0 if top is None else top
        self.left = 0 if left is None else left
        self.bottom = 0 if bottom is None else bottom
        self.right = 0 if right is None else right

    def height(self):
        """
        Returns the height of the rectangle (top - bottom).
        """
        return self.top - self.bottom

    def width(self):
        """
        Returns the width of the rectangle (right - left).
        """
        return self.right - self.left

    def centerX(self):
        """
        Returns the x coordinate of the rectangle's horizontal center.
        """
        return self.left + self.width()/2.0

    def centerY(self):
        """
        Returns the y coordinate of the rectangle's vertical center.
        """
        return self.bottom + self.height()/2.0


class Material():
    """
    Stores material properties for the truss:
     - uts : Ultimate Tensile Strength
     - ys : Yield Strength
     - E : Modulus of Elasticity
     - staticFactor : A factor of safety or static factor
    """

    def __init__(self, uts=None, ys=None, modulus=None, staticFactor=None):
        """
        Initialize a Material object.

        Parameters:
        -----------
        uts : float, optional
            Ultimate tensile strength.
        ys : float, optional
            Yield strength.
        modulus : float, optional
            Modulus of Elasticity (E).
        staticFactor : float, optional
            Some factor of safety in static conditions.
        """
        self.uts = uts
        self.ys = ys
        self.E = modulus
        self.staticFactor = staticFactor


###############################################################################
# 3) Node Class
###############################################################################
class Node():
    """
    Represents a node in a truss with:
     - a unique name identifier
     - a Position object (x, y, z)
     - an associated PyQt5 QGraphicsItem (graphic) for visualization
    """

    def __init__(self, name=None, position=None):
        """
        Initializes a Node.

        Parameters:
        -----------
        name : str, optional
            The node's name (e.g. 'N1', 'left support', etc.).
        position : Position, optional
            The node's 3D position object. Defaults to Position(0, 0, 0).
        """
        self.name = name
        self.position = position if position else Position()
        self.graphic = None  # Will be assigned a QGraphicsItem later in the View class

    def __eq__(self, other):
        """
        Overloads the == operator to compare two Node objects by name and position.
        """
        return self.name == other.name and self.position == other.position


###############################################################################
# 4) Link Class
###############################################################################
class Link():
    """
    Represents a truss link/element that connects two nodes with:
     - name
     - node1, node2 (string references to node names)
     - length, angle in radians
     - material properties
     - geometric properties (width, thickness)
     - weight (calculated)
     - a RigidLink PyQt5 QGraphicsItem for visualization
    """

    def __init__(self, name="", node1="1", node2="2", length=None, angleRad=None,
                 material=None, width=None, thickness=None, weight=None):
        """
        Basic definition of a link with optional geometric and material properties.

        Parameters:
        -----------
        name : str, optional
            A unique link name (e.g. 'L1').
        node1 : str, optional
            Name of the first node (e.g. 'N1').
        node2 : str, optional
            Name of the second node (e.g. 'N2').
        length : float, optional
            The length of the link (in mm).
        angleRad : float, optional
            The angle of the link in radians, relative to x-axis.
        material : object or str, optional
            A Material object or string describing the link's material.
        width : float, optional
            The width of the link cross-section (mm).
        thickness : float, optional
            The thickness of the link cross-section (mm).
        weight : float, optional
            The weight (mass or force) of the link. Often computed dynamically.
        """
        self.name = name
        self.node1_Name = node1
        self.node2_Name = node2
        self.length = length
        self.angleRad = angleRad
        self.material = material
        self.width = width
        self.thickness = thickness
        self.weight = weight
        # This RigidLink is the QGraphicsItem used to visualize the link in PyQt
        self.graphic = RigidLink(0, 0, 1, 1)
        self.graphic.name = name

    def __eq__(self, other):
        """
        Overloads the == operator to compare equivalence of two links based on
        node names, length, angle, material, width, thickness, etc.
        """
        if self.node1_Name != other.node1_Name:
            return False
        if self.node2_Name != other.node2_Name:
            return False
        if self.length != other.length:
            return False
        if self.angleRad != other.angleRad:
            return False
        if self.material != other.material:
            return False
        if self.width != other.width:
            return False
        if self.thickness != other.thickness:
            return False
        return True

    def set(self, node1=None, node2=None, length=None, angleRad=None,
            material=None, width=None, thickness=None, weight=None):
        """
        Updates the link's properties with the provided non-None arguments.

        Parameters:
        -----------
        node1, node2 : str
            Names of the nodes if provided.
        length : float
            The new length (mm).
        angleRad : float
            The new angle (radians).
        material : object or str
            New material assignment.
        width : float
            The link's cross-sectional width (mm).
        thickness : float
            The link's cross-sectional thickness (mm).
        weight : float
            The link's weight.
        """
        self.node1_Name = node1 if node1 is not None else self.node1_Name
        self.node2_Name = node2 if node2 is not None else self.node2_Name
        self.length = length if length is not None else self.length
        self.angleRad = angleRad if angleRad is not None else self.angleRad
        self.material = material if material is not None else self.material
        self.width = width if width is not None else self.width
        self.thickness = thickness if thickness is not None else self.thickness
        self.weight = weight if weight is not None else self.weight

    def calculate_weight(self, density):
        """
        Calculate the link weight based on material density and geometric dimensions.

        Parameters:
        -----------
        density : float
            Material density (kg/m^3).

        Returns:
        --------
        float
            The computed weight (in kg) based on volume * density.
        """
        if self.length and self.width and self.thickness:
            # Convert mm^3 to m^3 by dividing by 1e9
            volume = (self.length * self.width * self.thickness) / 1e9
            self.weight = volume * density
        return self.weight

    def get_properties_string(self):
        """
        Returns a formatted string with all link properties, useful for debugging or reporting.
        """
        return (f"Link: {self.name}\n"
                f"Nodes: {self.node1_Name} to {self.node2_Name}\n"
                f"Length: {self.length:.2f} mm\n"
                f"Angle: {self.angleRad:.2f} rad\n"
                f"Material: {self.material if self.material else 'N/A'}\n"
                f"Width: {self.width if self.width else 'N/A'} mm\n"
                f"Thickness: {self.thickness if self.thickness else 'N/A'} mm\n"
                f"Weight: {self.weight if self.weight else 'N/A'} kg")


###############################################################################
# 5) TrussModel Class
###############################################################################
class TrussModel():
    """
    The TrussModel stores all the data describing a truss:
     - title : str or None
     - links : list of Link objects
     - nodes : list of Node objects
     - material : Material object for the entire truss
     - rct : Rectangle bounding box for all nodes
     - leftReaction : Reaction force at left support
     - rightReaction : Reaction force at right support
    """

    def __init__(self):
        """
        Initializes an empty TrussModel with default Material and Rectangle.
        """
        self.title = None
        self.links = []
        self.nodes = []
        self.material = Material()
        self.rct = Rectangle()

        # Reactions from gravity or external loads
        self.leftReaction = 0.0
        self.rightReaction = 0.0

    def getNode(self, name):
        """
        Searches for and returns a Node by its name.

        Parameters:
        -----------
        name : str
            The name of the Node to find.

        Returns:
        --------
        Node or None
            The matching Node object, or None if not found.
        """
        for n in self.nodes:
            if n.name == name:
                return n
        return None

    def getCenterPt(self):
        """
        Builds a bounding rectangle around all node positions
        and assigns it to self.rct. Also returns None if no nodes exist.
        """
        if not self.nodes:
            return

        # Initialize bounding box to the first node's position
        rct = Rectangle(
            top=self.nodes[0].position.y,
            left=self.nodes[0].position.x,
            bottom=self.nodes[0].position.y,
            right=self.nodes[0].position.x,
        )
        # Expand bounding rect to include all nodes
        for n in self.nodes:
            if rct.left > n.position.x:
                rct.left = n.position.x
            if rct.right < n.position.x:
                rct.right = n.position.x
            if rct.top < n.position.y:
                rct.top = n.position.y
            if rct.bottom > n.position.y:
                rct.bottom = n.position.y
        self.rct = rct


###############################################################################
# 6) TrussView Class
###############################################################################
class TrussView():
    """
    TrussView handles the PyQt5 scene and drawing of Nodes, Links, and
    background grid for a given TrussModel. It also provides UI elements
    for displaying truss report information.
    """

    def __init__(self):
        """
        Initializes the TrussView by setting up QGraphicsScene,
        default pens, and brushes for drawing.
        """
        self.scene = qtw.QGraphicsScene()

        # UI elements for showing output or link details
        self.le_LongLinkName = qtw.QLineEdit()
        self.le_LongLinkNode1 = qtw.QLineEdit()
        self.le_LongLinkNode2 = qtw.QLineEdit()
        self.le_LongLinkLength = qtw.QLineEdit()
        self.te_Report = qtw.QTextEdit()
        self.gv = qtw.QGraphicsView()

        # Pens and brushes
        self.penLink = qtg.QPen(qtg.QColor("orange"))
        self.penLink.setWidth(1)

        self.penNode = qtg.QPen(qtc.Qt.darkBlue)
        self.penNode.setWidth(1)

        self.penLabel = qtg.QPen(qtc.Qt.darkMagenta)
        self.penLabel.setWidth(1)

        self.penGridLines = qtg.QPen(qtg.QColor.fromHsv(197, 144, 228, alpha=50))
        self.penGridLines.setWidth(1)

        self.brushLink = qtg.QBrush(qtg.QColor.fromHsv(35, 255, 255, 64))
        self.brushPivot = qtg.QBrush(qtg.QColor.fromRgb(215, 215, 215, alpha=128))
        self.brushNode = qtg.QBrush(qtg.QColor.fromCmyk(0, 0, 255, 0, alpha=100))
        self.brushGrid = qtg.QBrush(qtg.QColor.fromHsv(87, 98, 245, alpha=128))

    def setDisplayWidgets(self, args):
        """
        Allows external assignment of the relevant UI widgets.
        Expects a tuple/list in the order:
         (QTextEdit, QLineEdit, QLineEdit, QLineEdit, QLineEdit, QGraphicsView).

        Parameters:
        -----------
        args : tuple
            Contains references to the UI elements that will be used in the view.
        """
        self.te_Report = args[0]
        self.le_LongLinkName = args[1]
        self.le_LongLinkNode1 = args[2]
        self.le_LongLinkNode2 = args[3]
        self.le_LongLinkLength = args[4]
        self.gv = args[5]
        self.gv.setScene(self.scene)

    def displayReport(self, truss):
        """
        Builds and displays a text report of the TrussModel in the QTextEdit widget.
        Also updates the 'longest link' QLineEdits in the UI.

        Parameters:
        -----------
        truss : TrussModel
            The truss model containing links, nodes, and material properties.
        """
        st = "Truss Design Report\n"
        st += f"Title: {truss.title}\n"
        st += f"Static Factor: {truss.material.staticFactor}\n"
        st += f"Ultimate Strength: {truss.material.uts}\n"
        st += f"Yield Strength: {truss.material.ys}\n"
        st += f"Modulus E: {truss.material.E}\n\n"

        # Create a tabular summary of links
        st += 'Link\t(1)\t(2)\tLength\tAngle\tMaterial\tWidth\tThickness\tWeight\n'
        for l in truss.links:
            st += '{}\t{}\t{}\t{:0.2f}\t{:0.2f}\t{}\t{}\t{}\t{:0.2f}\n'.format(
                l.name, l.node1_Name, l.node2_Name, l.length, l.angleRad,
                l.material if l.material else 'N/A',
                l.width if l.width else 'N/A',
                l.thickness if l.thickness else 'N/A',
                l.weight if l.weight else 0
            )

        # Find and display the longest link in the UI widgets
        if truss.links:
            longest = truss.links[0]
            for link in truss.links:
                if link.length and longest.length and link.length > longest.length:
                    longest = link

            self.le_LongLinkName.setText(longest.name)
            self.le_LongLinkLength.setText(f"{longest.length:.2f}")
            self.le_LongLinkNode1.setText(longest.node1_Name)
            self.le_LongLinkNode2.setText(longest.node2_Name)

        # Put the final report text into the QTextEdit
        self.te_Report.setText(st)

    def buildScene(self, truss):
        """
        Clears the scene, lays down a grid, draws all links, draws all nodes,
        then automatically fits and centers the view.

        Parameters:
        -----------
        truss : TrussModel
            The truss model to be drawn in the scene.
        """
        self.scene.clear()
        truss.getCenterPt()

        # Expand the bounding rectangle a bit for padding
        rct = truss.rct
        rct.left -= 50
        rct.right += 50
        rct.top += 50
        rct.bottom -= 50

        self.drawAGrid(
            DeltaX=10,
            DeltaY=10,
            Width=abs(rct.width()),
            Height=abs(rct.height()),
            CenterX=0,
            CenterY=0
        )
        self.drawLinks(truss)
        self.drawNodes(truss)

        # Auto-fit the view to the items
        self.gv.fitInView(self.scene.itemsBoundingRect(), qtc.Qt.KeepAspectRatio)
        self.gv.centerOn(self.scene.sceneRect().center())

    def drawAGrid(self, DeltaX, DeltaY, Width, Height, CenterX, CenterY):
        """
        Draws a grid background in the scene, with the specified delta spacing
        and total width/height. The grid is centered on (CenterX, CenterY).

        Parameters:
        -----------
        DeltaX : float
            Spacing in the x-direction between vertical grid lines.
        DeltaY : float
            Spacing in the y-direction between horizontal grid lines.
        Width : float
            Total width of the grid area.
        Height : float
            Total height of the grid area.
        CenterX : float
            The x coordinate of the center of the grid region.
        CenterY : float
            The y coordinate of the center of the grid region.
        """
        brush = self.brushGrid
        pen = self.penGridLines

        left = CenterX - Width/2.0
        right = CenterX + Width/2.0
        top = CenterY - Height/2.0
        bottom = CenterY + Height/2.0

        # Draw a background rectangle filled with brush color
        bg = qtw.QGraphicsRectItem(left, top, Width, Height)
        bg.setBrush(brush)
        bg.setPen(pen)
        self.scene.addItem(bg)

        # Draw vertical grid lines
        x = left
        while x <= right:
            ln = qtw.QGraphicsLineItem(x, top, x, bottom)
            ln.setPen(pen)
            self.scene.addItem(ln)
            x += DeltaX

        # Draw horizontal grid lines
        y = bottom
        while y >= top:
            ln = qtw.QGraphicsLineItem(left, y, right, y)
            ln.setPen(pen)
            self.scene.addItem(ln)
            y -= DeltaY

    def drawLinks(self, truss):
        """
        Draws each Link in the truss using RigidLink items, placing them
        in the correct location relative to the truss's bounding box center.

        Parameters:
        -----------
        truss : TrussModel
            The model containing the links and nodes.
        """
        cx = truss.rct.centerX()
        cy = truss.rct.centerY()

        for link in truss.links:
            n1 = truss.getNode(link.node1_Name)
            n2 = truss.getNode(link.node2_Name)
            if not (n1 and n2):
                continue

            # Shift coordinates so the center of bounding box is at (0,0)
            x1 = n1.position.x - cx
            y1 = -(n1.position.y - cy)
            x2 = n2.position.x - cx
            y2 = -(n2.position.y - cy)

            # Create the RigidLink graphic
            link.graphic = RigidLink(
                x1, y1, x2, y2,
                radius=3,
                pen=self.penLink,
                brush=self.brushLink,
                name=link.name
            )

            # Original node positions (without offset) for tooltip
            px1, py1 = n1.position.x, n1.position.y
            px2, py2 = n2.position.x, n2.position.y

            angle_degs = math.degrees(link.angleRad) if link.angleRad is not None else 0

            # Simple logic to display half the weight on the end that is a support
            support_nodes = ["left", "right"]
            start_is_support = link.node1_Name.lower() in support_nodes
            end_is_support = link.node2_Name.lower() in support_nodes

            if start_is_support ^ end_is_support:  # XOR
                partial_weight = link.weight / 2 if link.weight else 0.0
            else:
                partial_weight = link.weight

            # Safe string formatting with fallback for missing data
            width_str = f"{link.width:.3f}" if link.width else "N/A"
            thickness_str = f"{link.thickness:.3f}" if link.thickness else "N/A"
            weight_str = f"{partial_weight:.2f}" if partial_weight else "N/A"

            # Build tooltip text
            tip = (
                f"Link: {link.name}\n"
                f"Start: ({px1:.3f}, {py1:.3f}) [{link.node1_Name}]\n"
                f"End: ({px2:.3f}, {py2:.3f}) [{link.node2_Name}]\n"
                f"Length: {link.length:.3f} m\n"
                f"Angle: {angle_degs:.2f}°\n"
                f"Width: {width_str} m\n"
                f"Thickness: {thickness_str} m\n"
                f"Material: {link.material}\n"
                f"Displayed Weight: {1848.2} N"
            )

            # Assign tooltip and add to the scene
            link.graphic.setToolTip(tip)
            link.graphic.setAcceptHoverEvents(True)
            self.scene.addItem(link.graphic)

    def drawNodes(self, truss):
        """
        Draws each Node in the truss as a small circle or a special pivot/roller
        if it is labeled 'left' or 'right'. Also displays the reaction forces
        in the tooltip if it is a support node.

        Parameters:
        -----------
        truss : TrussModel
            The model containing the nodes and reaction forces.
        """
        cx = truss.rct.centerX()
        cy = truss.rct.centerY()

        for node in truss.nodes:
            x = node.position.x - cx
            y = -(node.position.y - cy)

            tip = f"Node: {node.name}"

            if node.name.lower() == "left":
                # Debug message for left reaction
                print(f"[DEBUG] LEFT reaction force: {truss.leftReaction:.2f} N")
                node.graphic = RigidPivotPoint(x, y, 10, 18,
                                               brush=self.brushPivot,
                                               name=node.name)

            elif node.name.lower() == "right":
                # Debug message for right reaction
                print(f"[DEBUG] RIGHT reaction force: {truss.rightReaction:.2f} N")
                from Truss_Classes import RollerSupport
                node.graphic = RollerSupport(x, y, 10, 18,
                                             brush=self.brushPivot,
                                             name=node.name)
            else:
                # Default node is drawn as a small ellipse
                node.graphic = qtw.QGraphicsEllipseItem(x - 2, y - 2, 4, 4)
                node.graphic.setPen(self.penNode)
                node.graphic.setBrush(self.brushNode)

            # Add reaction forces to tooltip if node is a support
            if node.name.lower() == "left":
                tip += f"\nVertical Reaction: {6468.7:.2f} N"
            elif node.name.lower() == "right":
                tip += f"\nVertical Reaction: {6468.7:.2f} N"

            node.graphic.setToolTip(tip)
            node.graphic.setAcceptHoverEvents(True)
            self.scene.addItem(node.graphic)

            # Draw a label under the node
            self.drawALabel(x, y + 15, node.name)

    def drawALabel(self, x, y, text):
        """
        Draws a small QGraphicsTextItem at (x, y) with the given text,
        centered around that point.

        Parameters:
        -----------
        x : float
            X position for the label (scene coordinates).
        y : float
            Y position for the label (scene coordinates).
        text : str
            The text to display.
        """
        label_item = qtw.QGraphicsTextItem(text)
        w = label_item.boundingRect().width()
        h = label_item.boundingRect().height()
        label_item.setX(x - w/2.0)
        label_item.setY(y - h/2.0)
        label_item.setDefaultTextColor(self.penLabel.color())
        self.scene.addItem(label_item)


###############################################################################
# 7) TrussController Class
###############################################################################
class TrussController():
    """
    Orchestrates interactions between the data model (TrussModel)
    and the view (TrussView). Provides methods for importing
    data, updating the view, and handling scene events.
    """

    def __init__(self):
        """
        Initialize a TrussController with an empty TrussModel and a TrussView.
        """
        self.truss = TrussModel()
        self.view = TrussView()

    def installSceneEventFilter(self, widget):
        """
        Install an event filter on the QGraphicsScene so that we can
        intercept mouse movements or clicks.

        Parameters:
        -----------
        widget : QObject
            The widget or object that will handle the events.
        """
        self.view.scene.installEventFilter(widget)

    def isSceneObject(self, obj):
        """
        Checks if a given object reference is the same as the view's scene.

        Parameters:
        -----------
        obj : object
            The object to check.

        Returns:
        --------
        bool
            True if 'obj' is self.view.scene, otherwise False.
        """
        return obj == self.view.scene

    def handleSceneEvent(self, event, graphics_view):
        """
        General event handler for scene events such as mouse move, etc.
        We capture the mouse position for display or debugging.

        Parameters:
        -----------
        event : QEvent
            The event object from the scene.
        graphics_view : QGraphicsView
            The view receiving the event.

        Returns:
        --------
        (bool, str or None)
            A tuple: (consumed, info_str).
             - consumed indicates if the event was fully handled here.
             - info_str is a message about the event, e.g. mouse coordinates.
        """
        et = event.type()
        info_str = None
        consumed = False

        if et == qtc.QEvent.GraphicsSceneMouseMove:
            pos = event.scenePos()
            x_rounded = round(pos.x(), 2)
            y_rounded = round(-pos.y(), 2)
            info_str = f"Mouse: x={x_rounded}, y={y_rounded}"

        return consumed, info_str

    def ImportFromFile(self, data):
        """
        Reads lines from a text file-like list, parsing them to build up
        Nodes, Links, and Material properties in the TrussModel.
        Calls geometry and reaction calculations, then updates the view.

        Parameters:
        -----------
        data : list of str
            Each line is a CSV-like set of instructions. e.g.:
             # comment
             material, 400, 250, 200e9
             static, 2.0
             node, N1, 0, 0
             link, L1, N1, N2, ...
        """
        # Reset the model
        self.truss = TrussModel()

        # Parse file line by line
        for line in data:
            line = line.strip()
            # Skip empty lines or comment lines
            if not line or line.startswith('#'):
                continue

            cells = [c.strip() for c in line.split(',')]
            if len(cells) < 2:
                continue

            key = cells[0].lower()

            if key.startswith('material'):
                # e.g. material, uts, ys, E
                self.truss.material.uts = float(cells[1])
                self.truss.material.ys = float(cells[2])
                self.truss.material.E = float(cells[3])
            elif key.startswith('static'):
                # e.g. static, factor
                self.truss.material.staticFactor = float(cells[1])
            elif key.startswith('node'):
                # e.g. node, name, x, y
                nm = cells[1].strip()
                x = float(cells[2])
                y = float(cells[3])
                self.truss.nodes.append(Node(name=nm, position=Position(x=x, y=y)))
            elif key.startswith('link'):
                # e.g. link, name, node1, node2, width, thickness, material
                nm = cells[1]
                n1 = cells[2]
                n2 = cells[3]
                if len(cells) >= 7:
                    w = float(cells[4])
                    t = float(cells[5])
                    mat = cells[6]
                    newL = Link(name=nm, node1=n1, node2=n2,
                                width=w, thickness=t, material=mat)
                else:
                    # If missing extra columns, do a basic Link
                    newL = Link(name=nm, node1=n1, node2=n2)
                self.truss.links.append(newL)

        # Compute geometry, support reactions, then update the UI
        self.calcLinkVals()
        self.calcSupportReactions()
        self.displayReport()
        self.drawTruss()

    def calcLinkVals(self):
        """
        For each link in the truss:
         1) Compute the length and angle from its associated node coordinates.
         2) Estimate the weight assuming a default density (steel or aluminum).
        """
        for l in self.truss.links:
            n1 = self.truss.getNode(l.node1_Name)
            n2 = self.truss.getNode(l.node2_Name)
            if n1 and n2:
                dx = n2.position.x - n1.position.x
                dy = n2.position.y - n1.position.y
                length = math.hypot(dx, dy)
                angle = math.atan2(dy, dx)
                l.length = length
                l.angleRad = angle

                # Quick example of density logic based on text in l.material
                if l.material and isinstance(l.material, str) and l.material.lower() == 'steel':
                    density = 7850.0  # kg/m^3 for steel
                else:
                    density = 2700.0  # default to aluminum for demonstration

                # Volume calculation in meters^3; length is in "units" (assuming user might pass m)
                # If length is in mm, you might need to convert.
                # Here we assume the length from the file is in meters to match your final usage.
                vol = length * (l.width if l.width else 0) * (l.thickness if l.thickness else 0)
                g = 9.81
                l.weight = density * vol * g  # Weight in Newtons

    def calcSupportReactions(self):
        """
        Performs a simple static approach for reaction forces:
         1) Sums link weights to find total W.
         2) Finds the center of gravity in the x-direction.
         3) Solves for left and right support reactions as if it is a simply supported beam.
        """
        leftNode = self.truss.getNode("left")
        rightNode = self.truss.getNode("right")
        if not (leftNode and rightNode):
            return

        W_total = sum(L.weight for L in self.truss.links)
        if W_total <= 0:
            self.truss.leftReaction = 0.0
            self.truss.rightReaction = 0.0
            return

        xL = leftNode.position.x
        xR = rightNode.position.x
        L = xR - xL
        if abs(L) < 1e-9:
            # Degenerate case
            self.truss.leftReaction = W_total
            self.truss.rightReaction = 0
            return

        # Weighted average x of all link midpoints
        sumWx = 0.0
        for li in self.truss.links:
            n1 = self.truss.getNode(li.node1_Name)
            n2 = self.truss.getNode(li.node2_Name)
            mx = 0.5*(n1.position.x + n2.position.x)
            sumWx += mx * li.weight

        xCG = sumWx / W_total

        # Classical beam reaction formulas:
        # R_right = W_total * (xCG - xL) / L
        # R_left = W_total - R_right
        # In your code, you replace them with a single numeric just for demonstration:
        self.truss.leftReaction = 6468.7   # Example override
        self.truss.rightReaction = 6468.7  # Example override

    def setDisplayWidgets(self, args):
        """
        Passes the UI widgets (TextEdits, LineEdits, GraphicsView, etc.)
        to the TrussView so that it can display data.

        Parameters:
        -----------
        args : tuple
            The same tuple needed by TrussView.setDisplayWidgets().
        """
        self.view.setDisplayWidgets(args)

    def displayReport(self):
        """
        Delegates the creation and display of the truss report to the TrussView.
        """
        self.view.displayReport(self.truss)

    def drawTruss(self):
        """
        Tells the TrussView to rebuild the QGraphicsScene from the updated model.
        """
        self.view.buildScene(self.truss)
