from PySide6.QtGui import QPainter, QPixmap, QIcon, QColor, QPen, QPainterPath
from PySide6.QtCore import Qt, QPointF, QRectF
import math


def _pixmap(size=48):
    p = QPixmap(size, size)
    p.fill(Qt.GlobalColor.transparent)
    return p


def _painter(pixmap):
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
    return p


def icon_theme_toggle(is_dark=True, color="#89b4fa", size=48):
    px = _pixmap(size)
    p = _painter(px)
    s = size

    pen = QPen(QColor(color))
    pen.setWidthF(s * 0.06)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)

    cx, cy = s * 0.5, s * 0.5

    if is_dark:
        r = s * 0.18
        p.drawEllipse(QPointF(cx, cy), r, r)
        ray_len = s * 0.1
        ray_start = r + s * 0.06
        for i in range(8):
            angle = math.radians(i * 45)
            x1 = cx + ray_start * math.cos(angle)
            y1 = cy + ray_start * math.sin(angle)
            x2 = cx + (ray_start + ray_len) * math.cos(angle)
            y2 = cy + (ray_start + ray_len) * math.sin(angle)
            p.drawLine(QPointF(x1, y1), QPointF(x2, y2))
    else:
        path = QPainterPath()
        r = s * 0.3
        path.addEllipse(QPointF(cx, cy), r, r)
        cut_path = QPainterPath()
        offset_x = r * 0.55
        offset_y = -r * 0.25
        cut_path.addEllipse(QPointF(cx + offset_x, cy + offset_y), r * 0.85, r * 0.85)
        final_path = path.subtracted(cut_path)
        p.setBrush(QColor(color))
        p.drawPath(final_path)

    p.end()
    return QIcon(px)


def icon_scan(color="#89b4fa", size=48):
    px = _pixmap(size)
    p = _painter(px)
    s = size
    w = s * 0.06
    pen = QPen(QColor(color), w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    m = s * 0.22
    rect = QRectF(m, m, s - 2 * m, s - 2 * m)
    p.drawRoundedRect(rect, s * 0.08, s * 0.08)

    y_positions = [s * 0.42, s * 0.52, s * 0.62]
    for y in y_positions:
        p.drawLine(QPointF(s * 0.32, y), QPointF(s * 0.68, y))

    p.end()
    return QIcon(px)


def icon_convert(color="#89b4fa", size=48):
    px = _pixmap(size)
    p = _painter(px)
    s = size
    w = s * 0.06
    pen = QPen(QColor(color), w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    p.drawLine(QPointF(s * 0.3, s * 0.35), QPointF(s * 0.7, s * 0.35))
    p.drawLine(QPointF(s * 0.6, s * 0.25), QPointF(s * 0.7, s * 0.35))
    p.drawLine(QPointF(s * 0.6, s * 0.45), QPointF(s * 0.7, s * 0.35))

    p.drawLine(QPointF(s * 0.7, s * 0.65), QPointF(s * 0.3, s * 0.65))
    p.drawLine(QPointF(s * 0.4, s * 0.55), QPointF(s * 0.3, s * 0.65))
    p.drawLine(QPointF(s * 0.4, s * 0.75), QPointF(s * 0.3, s * 0.65))

    p.end()
    return QIcon(px)


def icon_delete(color="#f38ba8", size=48):
    px = _pixmap(size)
    p = _painter(px)
    s = size
    w = s * 0.06
    pen = QPen(QColor(color), w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    p.drawLine(QPointF(s * 0.25, s * 0.3), QPointF(s * 0.75, s * 0.3))
    p.drawLine(QPointF(s * 0.42, s * 0.22), QPointF(s * 0.58, s * 0.22))
    p.drawLine(QPointF(s * 0.42, s * 0.22), QPointF(s * 0.42, s * 0.3))
    p.drawLine(QPointF(s * 0.58, s * 0.22), QPointF(s * 0.58, s * 0.3))

    p.drawLine(QPointF(s * 0.32, s * 0.3), QPointF(s * 0.36, s * 0.78))
    p.drawLine(QPointF(s * 0.68, s * 0.3), QPointF(s * 0.64, s * 0.78))
    p.drawLine(QPointF(s * 0.36, s * 0.78), QPointF(s * 0.64, s * 0.78))

    p.drawLine(QPointF(s * 0.5, s * 0.38), QPointF(s * 0.5, s * 0.7))

    p.end()
    return QIcon(px)


def icon_files(color="#89b4fa", size=48):
    px = _pixmap(size)
    p = _painter(px)
    s = size
    w = s * 0.06
    pen = QPen(QColor(color), w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    path = QPainterPath()
    path.moveTo(s * 0.25, s * 0.78)
    path.lineTo(s * 0.25, s * 0.22)
    path.lineTo(s * 0.55, s * 0.22)
    path.lineTo(s * 0.7, s * 0.37)
    path.lineTo(s * 0.7, s * 0.78)
    path.closeSubpath()
    p.drawPath(path)

    p.drawLine(QPointF(s * 0.55, s * 0.22), QPointF(s * 0.55, s * 0.37))
    p.drawLine(QPointF(s * 0.55, s * 0.37), QPointF(s * 0.7, s * 0.37))

    p.end()
    return QIcon(px)


def icon_settings(color="#89b4fa", size=48):
    px = _pixmap(size)
    p = _painter(px)
    s = size
    w = s * 0.06
    pen = QPen(QColor(color), w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    cx, cy = s * 0.5, s * 0.5
    p.drawEllipse(QPointF(cx, cy), s * 0.12, s * 0.12)

    teeth = 6
    inner_r = s * 0.22
    outer_r = s * 0.32
    for i in range(teeth):
        angle = math.radians(i * 60)
        x1 = cx + inner_r * math.cos(angle)
        y1 = cy + inner_r * math.sin(angle)
        x2 = cx + outer_r * math.cos(angle)
        y2 = cy + outer_r * math.sin(angle)
        p.drawLine(QPointF(x1, y1), QPointF(x2, y2))

    p.drawEllipse(QPointF(cx, cy), s * 0.22, s * 0.22)

    p.end()
    return QIcon(px)


def icon_about(color="#89b4fa", size=48):
    px = _pixmap(size)
    p = _painter(px)
    s = size
    w = s * 0.06
    pen = QPen(QColor(color), w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    cx, cy = s * 0.5, s * 0.5
    p.drawEllipse(QPointF(cx, cy), s * 0.3, s * 0.3)

    dot_pen = QPen(QColor(color))
    dot_pen.setWidthF(s * 0.09)
    dot_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    p.setPen(dot_pen)
    p.drawPoint(QPointF(cx, cy - s * 0.12))

    p.setPen(pen)
    p.drawLine(QPointF(cx, cy - s * 0.02), QPointF(cx, cy + s * 0.15))

    p.end()
    return QIcon(px)