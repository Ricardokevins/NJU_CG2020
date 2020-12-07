#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QFileDialog,
    QStyleOptionGraphicsItem,
    QColorDialog)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QTransform

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import *

# TODO: We need to set menu unchoosable to disable sudden status change while drawing polygon and curve


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.prestatus = ''
        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None

        self.start_point = None
        self.temp_p_list = []

        self.col = QColor(0, 0, 0)  # 设置画笔颜色的对应参数

    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_polygon(self, algorithm, item_id):
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_ellipse(self,  item_id):
        self.status = 'ellipse'
        self.temp_id = item_id
        self.temp_algorithm = ''

    def start_draw_curve(self, algorithm, item_id):
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_translate(self):
        if self.selected_id == '':  # not selecting anything
            self.status = ''
            return
        self.status = 'translate'
        self.temp_item = self.item_dict[self.selected_id]
        self.temp_p_list = self.temp_item.p_list

    def start_rotate(self):
        if self.selected_id == "":
            print("Not select anything yet")
            self.status = ""
            return
        self.status = 'rotate'
        self.temp_item = self.item_dict[self.selected_id]
        self.temp_p_list = self.temp_item.p_list
        self.rotate_angle = 0
        # TODO: Here not complete yet

    def start_scale(self):
        if self.selected_id == "":
            print("Not select anything yet")
            self.status = ""
            return
        self.status = 'scale'
        self.temp_item = self.item_dict[self.selected_id]
        self.temp_p_list = self.temp_item.p_list

    def start_clip_cohen_sutherland(self):
        if self.selected_id == "":
            print("Not select anything yet")
            self.status = ""
            return
        if self.item_dict[self.selected_id].item_type != 'line':
            self.status = ""
            return
        self.status = 'clip_CS'
        self.temp_item = self.item_dict[self.selected_id]
        self.temp_p_list = self.temp_item.p_list

    def start_clip_liang_barsky(self):
        if self.selected_id == "":
            print("Not select anything yet")
            self.status = ""
            return
        if self.item_dict[self.selected_id].item_type != 'line':
            self.status = ""
            return
        self.status = 'clip_LB'
        self.temp_item = self.item_dict[self.selected_id]
        self.temp_p_list = self.temp_item.p_list

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()
        self.temp_item = None

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        selected = str(selected)
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()

        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()

        self.status = ''
        self.updateScene([self.sceneRect()])

    def mousePressDetect(self, event):
        # use Mouse press poition to handle some control problem
        if event.button() == Qt.LeftButton:
            return 1
        elif event.button() == Qt.RightButton:
            return -1
        elif event.button() == Qt.MidButton:
            return 0

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())

        if self.status == 'line':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.col)
            self.scene().addItem(self.temp_item)
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.col)
            self.scene().addItem(self.temp_item)
        elif self.status == "polygon":
            # TODO:make menu not response to mouse which in case may lead to bug
            if self.temp_item == None:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.col)
                self.scene().addItem(self.temp_item)
            else:
                if self.mousePressDetect(event) == 1:
                    self.temp_item.p_list.append([x, y])
                else:
                    self.list_widget.addItem(self.temp_id)
                    self.temp_item.finish_draw = True
                    self.item_dict[self.temp_id] = self.temp_item
                    self.finish_draw()
                    # as soon as press right buttom which means stop
                    # I will refresh scene to use drawPolygon instead
                    # drawPolygoning which will draw last edge
                    self.updateScene([self.sceneRect()])
        elif self.status == 'curve':
            if self.temp_item == None:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.col)
                self.scene().addItem(self.temp_item)
            else:
                if self.mousePressDetect(event) == 1:
                    self.temp_item.p_list.append([x, y])
                else:
                    self.list_widget.addItem(self.temp_id)
                    self.temp_item.finish_draw = True
                    self.item_dict[self.temp_id] = self.temp_item
                    self.finish_draw()
                    # as soon as press right buttom which means stop
                    # I will refresh scene to use drawPolygon instead
                    # drawPolygoning which will draw last edge
                    self.updateScene([self.sceneRect()])
        elif self.status == "selecting":
            selected = self.scene().itemAt(pos, QTransform())
            for i in self.item_dict:
                if self.item_dict[i] == selected:
                    if self.selected_id != "":
                        self.item_dict[self.selected_id].selected = False
                        self.item_dict[self.selected_id].update()
                        self.updateScene([self.sceneRect()])
                    self.selected_id = i
                    self.item_dict[i].selected = True
                    self.item_dict[i].update()
                    self.main_window.list_widget.setCurrentRow(int(i))
        elif self.status == "translate":
            self.start_point = [x, y]
        elif self.status == "rotate":
            # use left buttom to decide rotate center
            # and use right buttom to caculate rotate angle
            # TODO: Not implement here Attention
            if self.mousePressDetect(event) == 1:
                self.start_point = [x, y]
            else:
                # finish rotating
                self.p_list = self.temp_item.p_list
                self.status = ''
        elif self.status == "scale":
            self.start_point = [x, y]
        elif self.status == 'clip_CS' or self.status == 'clip_LB':
            self.start_point = [x, y]
        else:
            print("Hit unknown State", self.status)
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        if self.status == 'ellipse':
            if self.temp_item == None:
                print("Hit Here")
                pass
            self.temp_item.p_list[1] = [x, y]
        if self.status == "polygon":
            # save the last position mouse stay
            # and make Item move as mouse did
            # Here Hit crash at one time
            # TODO: Pay Attention to every chance which temp_item may be None
            if self.temp_item == None:
                pass
            else:
                self.temp_item.p_list[-1] = [x, y]
        if self.status == "translate":
            self.temp_item.p_list = alg.translate(self.temp_p_list, x-self.start_point[0], y-self.start_point[1])
        if self.status == "scale":
            xp = ((x-self.start_point[0])**2 + (y-self.start_point[1])**2)/10000
            # print("缩放倍数：",xp)
            self.temp_item.p_list = alg.scale(
                self.temp_p_list, self.start_point[0], self.start_point[1], xp)
        if self.status == 'clip_LB' or self.status == 'clip_CS':
            if self.status == 'clip_LB':
                self.temp_item.p_list = alg.clip(
                    self.temp_p_list, self.start_point[0], self.start_point[1], x, y, "Liang-Barsky")
            else:
                self.temp_item.p_list = alg.clip(
                    self.temp_p_list, self.start_point[0], self.start_point[1], x, y, "Cohen-Sutherland")
        if self.status == "curve":
            if self.temp_item == None:
                print("Not creating anything")
                pass
            else:
                self.temp_item.p_list[-1] = [x, y]

        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            if self.temp_item.color == QColor(0, 0, 0):
                print("Not settting to item")
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        if self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        if self.status == "polygon":
            if self.temp_item == None:
                pass
            else:
                # try to catch last time mouse stay and draw
                pos = self.mapToScene(event.localPos().toPoint())
                x = int(pos.x())
                y = int(pos.y())
                self.temp_item.p_list[-1] = [x, y]
                # refresh Scene to see new item
                self.updateScene([self.sceneRect()])
        if self.status == "scale":
            self.p_list = self.temp_item.p_list
        if self.status == 'clip_LB' or self.status == 'clip_CS':
            self.p_list = self.temp_item.p_list
        if self.status == "curve":
            if self.temp_item == None:
                pass
            else:
                # try to catch last time mouse stay and draw
                pos = self.mapToScene(event.localPos().toPoint())
                x = int(pos.x())
                y = int(pos.y())
                self.temp_item.p_list[-1] = [x, y]
                # refresh Scene to see new item
                self.updateScene([self.sceneRect()])
            # pos = self.mapToScene(event.localPos().toPoint())
            # x = int(pos.x())
            # y = int(pos.y())
            # self.temp_item.p_list[-1] = [x, y]
            # self.updateScene([self.sceneRect()])
            # self.p_list = self.temp_item.p_list
        if self.status == 'rotate':
            self.temp_p_list == self.temp_item.p_list
    
        super().mouseReleaseEvent(event)

    def start_select(self):
        self.status = 'selecting'

    def set_pen_color(self, col):
        if col.isValid():
            # print("Canvas set color successfully")
            # if col == QColor(0, 0, 0):
            #     print("Still black")
            self.col = col
        else:
            print("Some thing wrong about color! Failed to set")

    def clear_canvas(self):
        for item in self.item_dict:
            self.scene().removeItem(self.item_dict[item])
        self.updateScene([self.sceneRect()])
        self.item_dict = {}
        self.selected_id = ''
        self.status = ''
        self.temp_item = None

    def wheelEvent(self, event):
        # delta fuction has been abandoned
        #print(event.angleDelta().y())
        if self.status == "rotate":
            if self.start_point != None:
                if event.angleDelta().y() > 0:
                    self.rotate_angle += 1
                else:
                    self.rotate_angle -= 1
                self.temp_item.p_list = alg.rotate(self.temp_p_list, self.start_point[0], self.start_point[1],self.rotate_angle)        
                #print(self.temp_item.p_list)
                #print(self.rotate_angle)
            else:
                print("Not choose Center Point now")
        self.updateScene([self.sceneRect()])


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """

    # def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', color: QColor = QColor(0, 0, 0), parent: QGraphicsItem = None):
    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', color: QColor = QColor(0, 0, 0), parent: QGraphicsItem = None):
        """
        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        if color == QColor(0, 0, 0):
            print("Still use origin color")
        self.color = color
        self.finish_draw = False

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.setPen(self.color)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            if self.finish_draw == True:
                item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            else:
                item_pixels = alg.draw_polygoning(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.setPen(self.color)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.setPen(self.color)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':

            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.setPen(self.color)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
            #print("Hit drawing curve")
            pass

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'polygon':
            xmax = -1
            ymax = -1
            xmin = 100000
            ymin = 100000
            for i in range(len(self.p_list)):
                tempx, tempy = self.p_list[i]
                xmin = min(xmin, tempx)
                ymin = min(ymin, tempy)
                xmax = max(xmax, tempx)
                ymax = max(ymax, tempy)
            w = xmax-xmin
            h = ymax-ymin
            return QRectF(xmin-1, ymin-1, w+2, h+2)
        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'curve':
            xmax = -1
            ymax = -1
            xmin = 100000
            ymin = 100000
            for i in range(len(self.p_list)):
                tempx, tempy = self.p_list[i]
                xmin = min(xmin, tempx)
                ymin = min(ymin, tempy)
                xmax = max(xmax, tempx)
                ymax = max(ymax, tempy)
            w = xmax-xmin
            h = ymax - ymin
            #print(xmin-1, ymin-1, w+2, h+2)
            return QRectF(xmin-1, ymin-1, w+2, h+2)


class MainWindow(QMainWindow):
    """
    主窗口类
    """

    def __init__(self):
        super().__init__()
        self.item_cnt = 0

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        clear_canvas_act = file_menu.addAction('清空画布')
        save_canvas_act = file_menu.addAction('保存画布')
        mouese_select_act = file_menu.addAction('选择图元')
        exit_act = file_menu.addAction('退出')

        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 关于菜单和窗口操作的信号绑定
        exit_act.triggered.connect(qApp.quit)
        set_pen_act.triggered.connect(self.set_pen)
        mouese_select_act.triggered.connect(self.select_item_action)
        clear_canvas_act.triggered.connect(self.clear_canvas)
        save_canvas_act.triggered.connect(self.save_canvas)
        self.list_widget.currentTextChanged.connect(
            self.canvas_widget.selection_changed)

        # 直线绘制算法的信号绑定
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_DDA_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)

        # 椭圆绘制算法信号绑定
        ellipse_act.triggered.connect(self.ellipse_action)

        # 多边形绘制算法信号绑定
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)

        # 曲线绘制算法的信号绑定
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)

        # 关于编辑的算法信号绑定
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)

        # 裁剪算法信号绑定
        clip_cohen_sutherland_act.triggered.connect(
            self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id

    def line_naive_action(self):
        if(self.item_cnt > 0):
            self.item_cnt -= 1
        self.canvas_widget.start_draw_line('Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_DDA_action(self):
        if(self.item_cnt > 0):
            self.item_cnt -= 1
        self.canvas_widget.start_draw_line('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        if(self.item_cnt > 0):
            self.item_cnt -= 1
        self.canvas_widget.start_draw_line('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        if(self.item_cnt > 0):
            self.item_cnt -= 1
        self.canvas_widget.start_draw_ellipse(self.get_id())
        self.statusBar().showMessage('绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        if(self.item_cnt > 0):
            self.item_cnt -= 1
        self.canvas_widget.start_draw_polygon('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_bresenham_action(self):
        if(self.item_cnt > 0):
            self.item_cnt -= 1
        self.canvas_widget.start_draw_polygon('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        if(self.item_cnt > 0):
            self.item_cnt -= 1
        self.canvas_widget.start_draw_curve('Bezier', self.get_id())
        self.statusBar().showMessage('Bezier算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        if(self.item_cnt > 0):
            self.item_cnt -= 1
        self.canvas_widget.start_draw_curve('B-spline', self.get_id())
        self.statusBar().showMessage('b_spline算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def select_item_action(self):
        self.statusBar().showMessage("使用鼠标选择图元")
        self.canvas_widget.start_select()

    def clear_canvas(self):
        self.statusBar().showMessage("清空画布")
        self.list_widget.clear()
        self.canvas_widget.clear_canvas()

    def save_canvas(self):
        self.statusBar().showMessage("保存画布")
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        self.statusBar().showMessage('保存画布')
        dialog = QFileDialog()
        filename = dialog.getSaveFileName(
            filter="Image Files(*.jpg *.png *.bmp)")
        if filename[0]:
            res = self.canvas_widget.grab(
                self.canvas_widget.sceneRect().toRect())
            res.save(filename[0])

    def set_pen(self):
        # use this fuction to set pen's color
        self.statusBar().showMessage("设置画笔")
        col = QColorDialog.getColor()
        if col.isValid():
            self.canvas_widget.set_pen_color(col)
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def translate_action(self):
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('平移')

    def rotate_action(self):
        self.canvas_widget.start_rotate()
        self.statusBar().showMessage('旋转')

    def scale_action(self):
        self.canvas_widget.start_scale()
        self.statusBar().showMessage('缩放')

    def clip_cohen_sutherland_action(self):
        self.canvas_widget.start_clip_cohen_sutherland()
        self.statusBar().showMessage('裁剪cohen_sutherland')

    def clip_liang_barsky_action(self):
        self.canvas_widget.start_clip_liang_barsky()
        self.statusBar().showMessage('裁剪liang_barsky')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
