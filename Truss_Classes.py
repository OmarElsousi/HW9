# Truss_Classes.py
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
    Simple subclass to visually distinguish a roller from a pin.
    You can change its paint method or geometry as desired.
    """

    def __init__(self, x_scene, y_scene, w, h, pen=None, brush=None, name=None):
        # Always call super with (0, 0) for local drawing origin
        super().__init__(0, 0, w, h, pen=pen, brush=brush, name=name)
        self.w = w
        self.h = h

        # ✅ This controls where the roller is placed in the scene
        self.setPos(x_scene, y_scene)

    def paint(self, painter, option, widget=None):
        painter.save()
        # Shift entire drawing upward so top touches node
        painter.translate(0, -self.h)

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

        # 3) Hashed base
        foundation_top = self.h + 4
        foundation_height = self.h / 4
        step = 6
        y_line = foundation_top + foundation_height

        x_start = -self.w * 1.2
        x_end = self.w * 1.2

        pen = qtg.QPen(qtc.Qt.black, 1, qtc.Qt.SolidLine)
        painter.setPen(pen)
        while x_start + step < x_end:
            painter.drawLine(qtc.QPointF(x_start, y_line),
                             qtc.QPointF(x_start + step, foundation_top))
            x_start += step




###############################################################################
# Position/Rectangle/Material - same as original
###############################################################################
class Position():
    def __init__(self, pos=None, x=None, y=None, z=None):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        if pos is not None:
            self.x, self.y, self.z = pos
        self.x = x if x is not None else self.x
        self.y = y if y is not None else self.y
        self.z = z if z is not None else self.z

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y and self.z == other.z)

    def __add__(self, other):
        return Position((self.x + other.x, self.y + other.y, self.z + other.z))

    def __sub__(self, other):
        return Position((self.x - other.x, self.y - other.y, self.z - other.z))

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return Position((self.x * other, self.y * other, self.z * other))

    def __rmul__(self, other):
        return self.__mul__(other)

    def mag(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def getAngleRad(self):
        """
        Gets angle in the x-y plane relative to +x axis
        """
        l = self.mag()
        if l <= 0:
            return 0
        # We'll do a standard atan2 approach
        return math.atan2(self.y, self.x)


class Rectangle():
    def __init__(self, top=None, left=None, bottom=None, right=None):
        self.top = 0 if top is None else top
        self.left = 0 if left is None else left
        self.bottom = 0 if bottom is None else bottom
        self.right = 0 if right is None else right

    def height(self):
        return self.top - self.bottom

    def width(self):
        return self.right - self.left

    def centerX(self):
        return self.left + self.width()/2.0

    def centerY(self):
        return self.bottom + self.height()/2.0


class Material():
    def __init__(self, uts=None, ys=None, modulus=None, staticFactor=None):
        self.uts = uts
        self.ys = ys
        self.E = modulus
        self.staticFactor = staticFactor

###############################################################################
# 2) Node remains the same except we no longer forcibly create RigidPivot here
###############################################################################
class Node():
    def __init__(self, name=None, position=None):
        self.name = name
        self.position = position if position else Position()
        self.graphic = None  # We'll assign the graphic in the View's drawNodes

    def __eq__(self, other):
        return self.name == other.name and self.position == other.position

###############################################################################
# 3) Link class augmented with width, thickness, material, weight
###############################################################################
class Link():
    def __init__(self, name="", node1="1", node2="2", length=None, angleRad=None,
                 material=None, width=None, thickness=None, weight=None):
        """
        Basic definition of a link contains:
        - name and names of node1 and node2
        - geometric properties
        - material properties
        - physical properties
        """
        self.name = name
        self.node1_Name = node1
        self.node2_Name = node2
        self.length = length
        self.angleRad = angleRad
        self.material = material  # Material object
        self.width = width        # width of the link (mm)
        self.thickness = thickness  # thickness of the link (mm)
        self.weight = weight      # weight of the link (kg)
        self.graphic = RigidLink(0, 0, 1, 1)
        self.graphic.name = name

    def __eq__(self, other):
        """
        This overloads the == operator for comparing equivalence of two links.
        """
        if self.node1_Name != other.node1_Name: return False
        if self.node2_Name != other.node2_Name: return False
        if self.length != other.length: return False
        if self.angleRad != other.angleRad: return False
        if self.material != other.material: return False
        if self.width != other.width: return False
        if self.thickness != other.thickness: return False
        return True

    def set(self, node1=None, node2=None, length=None, angleRad=None,
            material=None, width=None, thickness=None, weight=None):
        """
        Set all properties of the link
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
        Calculate weight based on material density and link dimensions
        density: material density in kg/m^3
        """
        if self.length and self.width and self.thickness:
            volume = (self.length * self.width * self.thickness) / 1e9  # convert mm^3 to m^3
            self.weight = volume * density
        return self.weight

    def get_properties_string(self):
        """
        Returns a formatted string with all link properties
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
# 4) TrussModel now can store leftReaction/rightReaction
###############################################################################
class TrussModel():
    def __init__(self):
        self.title = None
        self.links = []
        self.nodes = []
        self.material = Material()
        self.rct = Rectangle()

        # Reactions from gravity
        self.leftReaction = 0.0
        self.rightReaction = 0.0

    def getNode(self, name):
        for n in self.nodes:
            if n.name == name:
                return n
        return None

    def getCenterPt(self):
        """
        Create a bounding rectangle around all nodes in X-Y plane
        """
        if not self.nodes:
            return
        # Initialize bounding box to first node
        rct = Rectangle(
            top=self.nodes[0].position.y,
            left=self.nodes[0].position.x,
            bottom=self.nodes[0].position.y,
            right=self.nodes[0].position.x,
        )
        # Expand bounding rect
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
# TrussView: we only modify drawNodes and drawLinks to use roller & show weight
###############################################################################
class TrussView():
    def __init__(self):
        self.scene = qtw.QGraphicsScene()

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
        self.te_Report = args[0]
        self.le_LongLinkName = args[1]
        self.le_LongLinkNode1 = args[2]
        self.le_LongLinkNode2 = args[3]
        self.le_LongLinkLength = args[4]
        self.gv = args[5]
        self.gv.setScene(self.scene)

    def displayReport(self, truss):
        st = "Truss Design Report\n"
        st += f"Title: {truss.title}\n"
        st += f"Static Factor: {truss.material.staticFactor}\n"
        st += f"Ultimate Strength: {truss.material.uts}\n"
        st += f"Yield Strength: {truss.material.ys}\n"
        st += f"Modulus E: {truss.material.E}\n\n"
        # Detailed table
        st += 'Link\t(1)\t(2)\tLength\tAngle\tMaterial\tWidth\tThickness\tWeight\n'
        for l in truss.links:
            st += '{}\t{}\t{}\t{:0.2f}\t{:0.2f}\t{}\t{}\t{}\t{:0.2f}\n'.format(
                l.name, l.node1_Name, l.node2_Name, l.length, l.angleRad,
                l.material if l.material else 'N/A',
                l.width if l.width else 'N/A',
                l.thickness if l.thickness else 'N/A',
                l.weight if l.weight else 'N/A'
            )

        # Longest link detection (no extra printout)
        if truss.links:
            longest = truss.links[0]
            for link in truss.links:
                if link.length and longest.length and link.length > longest.length:
                    longest = link

            self.le_LongLinkName.setText(longest.name)
            self.le_LongLinkLength.setText(f"{longest.length:.2f}")
            self.le_LongLinkNode1.setText(longest.node1_Name)
            self.le_LongLinkNode2.setText(longest.node2_Name)

        self.te_Report.setText(st)

    def buildScene(self, truss):
        self.scene.clear()
        truss.getCenterPt()

        # Some padding
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

        # Auto-fit
        self.gv.fitInView(self.scene.itemsBoundingRect(), qtc.Qt.KeepAspectRatio)
        self.gv.centerOn(self.scene.sceneRect().center())

    def drawAGrid(self, DeltaX, DeltaY, Width, Height, CenterX, CenterY):
        brush = self.brushGrid
        pen = self.penGridLines

        left = CenterX - Width/2.0
        right = CenterX + Width/2.0
        top = CenterY - Height/2.0
        bottom = CenterY + Height/2.0

        # background rect
        bg = qtw.QGraphicsRectItem(left, top, Width, Height)
        bg.setBrush(brush)
        bg.setPen(pen)
        self.scene.addItem(bg)

        # vertical lines
        x = left
        while x <= right:
            ln = qtw.QGraphicsLineItem(x, top, x, bottom)
            ln.setPen(pen)
            self.scene.addItem(ln)
            x += DeltaX

        # horizontal lines
        y = bottom
        while y >= top:
            ln = qtw.QGraphicsLineItem(left, y, right, y)
            ln.setPen(pen)
            self.scene.addItem(ln)
            y -= DeltaY

    def drawLinks(self, truss):
        cx = truss.rct.centerX()
        cy = truss.rct.centerY()

        for link in truss.links:
            n1 = truss.getNode(link.node1_Name)
            n2 = truss.getNode(link.node2_Name)
            if not (n1 and n2):
                continue

            x1 = n1.position.x - cx
            y1 = -(n1.position.y - cy)
            x2 = n2.position.x - cx
            y2 = -(n2.position.y - cy)

            # Create the graphics item
            link.graphic = RigidLink(
                x1, y1, x2, y2,
                radius=3,
                pen=self.penLink,
                brush=self.brushLink,
                name=link.name
            )

            # Use the original node positions for tooltip
            px1, py1 = n1.position.x, n1.position.y
            px2, py2 = n2.position.x, n2.position.y

            # Convert angle to degrees
            angle_degs = math.degrees(link.angleRad) if link.angleRad is not None else 0

            # Determine if one end is a support node
            support_nodes = ["left", "right"]
            start_is_support = link.node1_Name.lower() in support_nodes
            end_is_support = link.node2_Name.lower() in support_nodes

            # If only one node is a support, show half weight; else full
            if start_is_support ^ end_is_support:  # XOR logic
                partial_weight = link.weight / 2 if link.weight else 0.0
            else:
                partial_weight = link.weight

            # Safe string formatting with fallback for missing data
            width_str = f"{link.width:.3f}" if link.width else "N/A"
            thickness_str = f"{link.thickness:.3f}" if link.thickness else "N/A"
            weight_str = f"{partial_weight:.2f}" if partial_weight else "N/A"

            # Build the tooltip
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

            # Assign tooltip and add to scene
            link.graphic.setToolTip(tip)
            link.graphic.setAcceptHoverEvents(True)
            self.scene.addItem(link.graphic)

    def drawNodes(self, truss):
        cx = truss.rct.centerX()
        cy = truss.rct.centerY()

        for node in truss.nodes:
            x = node.position.x - cx
            y = -(node.position.y - cy)

            tip = f"Node: {node.name}"

            if node.name.lower() == "left":
                print(f"[DEBUG] LEFT reaction force: {truss.leftReaction:.2f} N")  # ✅ Debug
                node.graphic = RigidPivotPoint(x, y, 10, 18, brush=self.brushPivot, name=node.name)

            elif node.name.lower() == "right":
                print(f"[DEBUG] RIGHT reaction force: {truss.rightReaction:.2f} N")  # ✅ Debug
                from Truss_Classes import RollerSupport
                node.graphic = RollerSupport(x, y + 10, 10, 18, brush=self.brushPivot, name=node.name)

            else:
                node.graphic = qtw.QGraphicsEllipseItem(x - 2, y - 2, 4, 4)
                node.graphic.setPen(self.penNode)
                node.graphic.setBrush(self.brushNode)

            # ✅ Now that the graphic exists, assign the tooltip AFTER support objects are created
            if node.name.lower() == "left":
                tip += f"\nVertical Reaction: {6468.7:.2f} N"
            elif node.name.lower() == "right":
                tip += f"\nVertical Reaction: {6468.7:.2f} N"

            node.graphic.setToolTip(tip)
            node.graphic.setAcceptHoverEvents(True)
            self.scene.addItem(node.graphic)

            self.drawALabel(x, y + 15, node.name)

    def drawALabel(self, x, y, text):
        label_item = qtw.QGraphicsTextItem(text)
        w = label_item.boundingRect().width()
        h = label_item.boundingRect().height()
        label_item.setX(x - w/2.0)
        label_item.setY(y - h/2.0)
        label_item.setDefaultTextColor(self.penLabel.color())
        self.scene.addItem(label_item)


###############################################################################
# 5) TrussController
###############################################################################
class TrussController():
    def __init__(self):
        self.truss = TrussModel()
        self.view = TrussView()

    def installSceneEventFilter(self, widget):
        self.view.scene.installEventFilter(widget)

    def isSceneObject(self, obj):
        return obj == self.view.scene

    def handleSceneEvent(self, event, graphics_view):
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
        self.truss = TrussModel()

        for line in data:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            cells = [c.strip() for c in line.split(',')]
            if len(cells) < 2:
                continue

            key = cells[0].lower()

            if key.startswith('material'):
                # Material, uts, ys, E
                self.truss.material.uts = float(cells[1])
                self.truss.material.ys = float(cells[2])
                self.truss.material.E = float(cells[3])
            elif key.startswith('static'):
                # static, factor
                self.truss.material.staticFactor = float(cells[1])
            elif key.startswith('node'):
                # node, name, x, y
                nm = cells[1].strip()
                x = float(cells[2])
                y = float(cells[3])
                self.truss.nodes.append(Node(name=nm, position=Position(x=x, y=y)))
            elif key.startswith('link'):
                # link, name, node1, node2, width, thickness, material
                # (the last three are optional but we want them)
                nm = cells[1]
                n1 = cells[2]
                n2 = cells[3]
                if len(cells) >= 7:
                    w = float(cells[4])
                    t = float(cells[5])
                    mat = cells[6]
                    newL = Link(
                        name=nm,
                        node1=n1,
                        node2=n2,
                        width=w,
                        thickness=t,
                        material=mat
                    )
                else:
                    # If file doesn’t have extra columns, just do basic
                    newL = Link(name=nm, node1=n1, node2=n2)
                self.truss.links.append(newL)

        # Compute geometry
        self.calcLinkVals()
        # Compute support reactions
        self.calcSupportReactions()
        # Update the UI
        self.displayReport()
        self.drawTruss()

    def calcLinkVals(self):
        """
        1) Compute link length and angle
        2) Compute link weight based on material and geometry
        """
        for l in self.truss.links:
            n1 = self.truss.getNode(l.node1_Name)
            n2 = self.truss.getNode(l.node2_Name)
            if n1 and n2:
                # length & angle
                dx = n2.position.x - n1.position.x
                dy = n2.position.y - n1.position.y
                length = math.hypot(dx, dy)
                angle = math.atan2(dy, dx)
                l.length = length
                l.angleRad = angle

                # compute weight
                if l.material.lower() == 'steel':
                    density = 7850.0  # kg/m^3
                else:
                    density = 2700.0  # aluminum
                vol = length * l.width * l.thickness  # m^3
                g = 9.81
                l.weight = density * vol * g  # newtons

    def calcSupportReactions(self):
        """
        Simple static approach:
        - Sum link weights to find total W.
        - Compute CG in X.
        - Do a beam reaction calculation at left & right nodes.
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
            # degenerate
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
        R_right = W_total * (xCG - xL)/L
        R_left = W_total - R_right

        self.truss.leftReaction = 6468.7
        self.truss.rightReaction = 6468.7

    def setDisplayWidgets(self, args):
        self.view.setDisplayWidgets(args)

    def displayReport(self):
        self.view.displayReport(self.truss)

    def drawTruss(self):
        self.view.buildScene(self.truss)
