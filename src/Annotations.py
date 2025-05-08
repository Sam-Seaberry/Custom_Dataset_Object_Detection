from PyQt5.QtWidgets import QDialog, QFileDialog, QApplication, QLabel, QMainWindow, QTreeWidgetItem, QTreeWidget
from create_lable_map import lable_map_creator
from PyQt5.QtCore import pyqtSignal,  Qt, QPoint
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QColor
from dataclasses import dataclass
from PIL import Image, ImageOps
import threading
import logging
import shutil
import time
import cv2
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class point_map_manual():
    
    
    def __init__(self, img, resize = None):
        self.annotations = []
        self.img = img
        self.calls = 0
        self.resize = resize
        self.resize_flag = 0 
        self.setup()


    # ============================================================================= #
    # Callback to click event. Left click creates points Right click is used        #
    # to remove points. Only points between right click down and right click up are #
    # removed. Any point within the box created by the two click are removed.       #                      
    # ============================================================================= #
    def click_event(self, event, x, y, flags, params):
        # Only handle these events
        if event in [cv2.EVENT_LBUTTONDOWN, cv2.EVENT_RBUTTONDOWN, cv2.EVENT_RBUTTONUP]:
            print(f"event: {event} x: {x} y: {y}")

            self.calls += 1
            global box_flag

            if event == cv2.EVENT_RBUTTONDOWN:
                box_flag = False
                self.current_box = [x, 0, y, 0]  # Store initial x and y as x1, y1

            elif event == cv2.EVENT_RBUTTONUP:
                box_flag = True
                # Complete the box with x2, y2
                if hasattr(self, 'current_box'):
                    self.current_box[1] = x
                    self.current_box[3] = y

                    if all(self.current_box):  # Ensure no zeros
                        self.annotations.append(self.current_box)  # Save the box
                        cv2.rectangle(
                            self.out_img,
                            (self.current_box[0], self.current_box[2]),  # x1, y1
                            (self.current_box[1], self.current_box[3]),  # x2, y2
                            (255, 0, 0),
                            4
                        )
                        print(f"box: {self.current_box}")
            

        
    
    # ==================================================================== #
    # Called from __init__ this function sets up the callback and opencv   #
    # image show functions. NOTE the image will not show without calls to #
    # cv.waitkey and cv.destroyAllWindows.                               #
    # ==================================================================== #
   
    def setup(self):
        if type(self.resize) is not None:
            self.resize_flag = 1

        self.out_img = cv2.imread(self.img)

        if self.resize_flag:
            self.out_img = self.resize_img(self.out_img)

        if self.out_img is None:
            print("Error: No Image Found In Directory")
            exit()
        
        cv2.namedWindow("annotation")
        cv2.setMouseCallback('annotation', self.click_event)
        
        while True:
            cv2.imshow("annotation", self.out_img)
            cv2.waitKey(1)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                self.out_img = cv2.imread(self.img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    # =============================================================== #
    # Used to display the points ontop of the given image. Refreshed  #
    # each click callback                                             #
    # =============================================================== #
    def display(self):
        self.out_img = cv2.imread(self.img)

        # Resize image if flag set
        if self.resize_flag:
            self.out_img = self.resize_img(self.out_img)

        if len(self.annotations) > 0:
            for i in self.annotations:
                
                cv2.imshow('annotations', self.out_img)

    # ============================================================ # 
    # Function to return pointmap in list form                     #
    # ============================================================ #
    def get_boxes(self):
        return self.annotations
   


    # ============================================================ # 
    # Function to resize images                                    #
    # ============================================================ #
    def resize_img(self, img):
        (hi,wi) = img.shape[:2]
        rh = int(hi/self.resize)
        rw = int(wi/self.resize)
        img = cv2.resize(img, (rw,rh))

        return img
    
@dataclass
class Annotation:
    Lable: str
    coords: list
    imagePath: str

class createannotations(QtWidgets.QMainWindow):
    FinishedClicked = pyqtSignal(str)
    def __init__(self, parent=None, images=None):
        super().__init__(parent)
        
        logger.info("Annotations Page Loaded")
        
        self.dialog = uic.loadUi('res/pages/annotations.ui', self)
        self.images = images
        self.image_num = 0
        
        self.labels = []
        
        self.lineSize = 2
        
        self.dialog.nextImage.clicked.connect(self.next_image)
        
        self.zoom_factor = 1.0
                
        self.display()
        
        self.dialog.finish_Button.clicked.connect(lambda: self.dialog.close())
        self.dialog.increaseLineButton.clicked.connect(self.increaseLineSize)
        self.dialog.decreaseLineButton.clicked.connect(self.decreaseLineSize)
        self.dialog.deleteButton.clicked.connect(self.deleteLastAnnotation)
        self.dialog.clearButton.clicked.connect(self.clearAnnotations)
        self.dialog.addLables.clicked.connect(self.addLabels)
        # = point_map_manual(self.images[0], 2)
        
    def increaseLineSize(self):
        self.lineSize += 1
    
    
    def decreaseLineSize(self):
        if self.lineSize > 1:
            self.lineSize -= 1
            
    def deleteLastAnnotation(self):
        if self.annotations:
            self.annotations.pop()
            self.cv_image = self.original_image.copy()
            for annotation in self.annotations:
                cv2.rectangle(self.cv_image,
                              (annotation[0], annotation[2]),
                              (annotation[1], annotation[3]),
                              (0, 255, 0), 2)
            self.display_image()
        else:
            print("No annotations to delete.")
            
    def clearAnnotations(self):
        self.annotations = []
        self.cv_image = self.original_image.copy()
        self.display_image()

    def addLabels(self):
        if self.dialog.labelName.text() == "":
            print("Please enter a label name.")
            return
        elif self.dialog.labelName.text() in [label.Lable for label in self.labels]:
            print("Label already exists.")
            return
        else:
            self.annotations = Annotation(self.dialog.labelName.text(), [], [])
            self.labels.append(self.annotations)
            self.updateTreeView()
        
            
        
    def display(self):
        
        self.cv_image = cv2.imread(self.images[self.image_num])
        self.cv_image = cv2.resize(self.cv_image, (int(self.cv_image.shape[1] / 4), int(self.cv_image.shape[0] / 4)))
        self.original_image = self.cv_image.copy()

        # QLabel to display image
        self.label = self.dialog.image_display

        # For drawing
        self.drawing = False
        self.start_point = QPoint()
        self.end_point = QPoint()

        self.display_image()

    def display_image(self):
        image = self.get_scaled_image()
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.label.setPixmap(pixmap)

    def get_scaled_image(self):
        # Scale the original image based on zoom factor
        height, width = self.original_image.shape[:2]
        new_size = (int(width * self.zoom_factor), int(height * self.zoom_factor))
        return cv2.resize(self.original_image, new_size, interpolation=cv2.INTER_LINEAR)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()

        # Adjust zoom factor with bounds
        if delta > 0:
            self.zoom_factor *= 1.1
        else:
            self.zoom_factor /= 1.1

        # Clamp zoom to reasonable levels
        self.zoom_factor = max(0.1, min(10.0, self.zoom_factor))

        self.display_image()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.start_point = self.get_image_coordinates(event)
            self.end_point = self.start_point

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_point = self.get_image_coordinates(event)
            self.cv_image = self.original_image.copy()
            cv2.rectangle(self.cv_image,
                          (self.start_point.x(), self.start_point.y()),
                          (self.end_point.x(), self.end_point.y()),
                          (0, 255, 0), 2)
            self.display_image()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.cv_image = self.original_image.copy()
            cv2.rectangle(self.cv_image,
                          (self.start_point.x(), self.start_point.y()),
                          (self.end_point.x(), self.end_point.y()),
                          (0, 255, 0), self.lineSize)
            self.original_image = self.cv_image.copy()
            if len(self.labels) == 0:
                print("Please add a label first.")
                return
            if len(self.labels) == 1:
                self.labels[0].coords.append([self.start_point.x(), self.start_point.y(), self.end_point.x(), self.end_point.y()])
                self.labels[0].imagePath.append(self.images[self.image_num])
            else:
                self.labels[len(self.labels)-1].coords.append([self.start_point.x(), self.start_point.y(), self.end_point.x(), self.end_point.y()])
                self.labels[len(self.labels)-1].imagePath.append(self.images[self.image_num])
            self.updateTreeView()
            self.display_image()
            
    def get_image_coordinates(self, event):
        # Get position of mouse inside the label
        mouse_pos = self.label.mapFrom(self, event.pos())
        label_width = self.label.width()
        label_height = self.label.height()

        image_height, image_width, _ = self.cv_image.shape

        # Compute scaling factors
        scale_x = image_width / label_width
        scale_y = image_height / label_height

        # Scale mouse position to image coordinate
        img_x = int(mouse_pos.x() * scale_x)
        img_y = int(mouse_pos.y() * scale_y)

        # Clamp to image bounds
        img_x = max(0, min(image_width - 1, img_x))
        img_y = max(0, min(image_height - 1, img_y))

        return QPoint(img_x, img_y)
    
    def next_image(self):
        self.image_num += 1
        if self.image_num >= len(self.images):
            self.image_num = 0

        print("Current image number:", self.image_num)
        self.display()
        
    
    def updateTreeView(self):
        # Update the tree view with the current annotation
        self.dialog.treeWidget.clear()
        for label in self.labels:
            label_item = QtWidgets.QTreeWidgetItem([label.Lable])
            for coords in label.coords:
                coord_item = QtWidgets.QTreeWidgetItem([f"Coords: {coords}"])
                label_item.addChild(coord_item)
            

        
        
        
        
        
        
