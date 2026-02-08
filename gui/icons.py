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


def icon_scan(color="#89b4fa", size=48):
    px = _pixmap(size)
    p = _painter(px)
    s = size
    w = s * 0.06

    pen = QPen(QColor(color), w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    m = s * 0.18
    rect = QRectF(m, m, s - 2 * m, s - 2 * m)
    p.drawRoundedRect(rect, s * 0.08, s * 0.08)

    pen.setWidth(max(1, int(w * 0.8)))
    p.setPen(pen)
    x1, x2 = s * 0.32, s * 0.68
    for y_ratio in [0.38, 0.50, 0.62]:
        y = s * y_ratio
        end = x2 if y_ratio != 0.62 else s * 0.55
        p.drawLine(QPointF(x1, y), QPointF(end, y))

    p.end()
    return QIcon(px)


def icon_convert(color="#89b4fa", size=48):
    px = _pixmap(size)
    p = _painter(px)
    s = size
    w = s * 0.06

    pen = QPen(QColor(color), w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)

    cx, cy = s * 0.5, s * 0.5
    r = s * 0.28

    path = QPainterPath()
    path.arcMoveTo(cx - r, cy - r, r * 2, r * 2, 60)
    path.arcTo(cx - r, cy - r, r * 2, r * 2, 60, 240)
    p.drawPath(path)

    end = path.currentPosition()
    a = math.radians(60 + 240)
    arr = s * 0.1
    p.drawLine(end, QPointF(end.x() + arr * math.cos(a - 0.6), end.y() - arr * math.sin(a - 0.6)))
    p.drawLine(end, QPointF(end.x() + arr * math.cos(a + 0.6), end.y() - arr * math.sin(a + 0.6)))

    p.end()
    return QIcon(px)


def icon_delete(color="#f38ba8", size=48):
    px = _pixmap(size)
    p = _painter(px)
    s = size
    w = s * 0.06

    pen = QPen(QColor(color), w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
    p.setPen(pen)

    cx = s * 0.5
    p.drawLine(QPointF(s * 0.3, s * 0.22), QPointF(s * 0.7, s * 0.22))
    p.drawLine(QPointF(cx - s * 0.05, s * 0.15), QPointF(cx + s * 0.05, s * 0.15))

    body = QRectF(s * 0.28, s * 0.26, s * 0.44, s * 0.52)
    p.drawRoundedRect(body, s * 0.04, s * 0.04)

    pen.setWidth(max(1, int(w * 0.7)))
    p.setPen(pen)
    for x_ratio in [0.4, 0.5, 0.6]:
        x = s * x_ratio
        p.drawLine(QPointF(x, s * 0.36), QPointF(x, s * 0.68))

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

    r1 = QRectF(s * 0.15, s * 0.25, s * 0.45, s * 0.55)
    p.drawRoundedRect(r1, s * 0.06, s * 0.06)

    r2 = QRectF(s * 0.30, s * 0.12, s * 0.45, s * 0.55)

    c = QColor(color)
    c.setAlpha(60)
    p.setBrush(c)
    p.drawRoundedRect(r2, s * 0.06, s * 0.06)

    p.end()
    return QIcon(px)


def icon_settings(color="#89b4fa", size=48):
    px = _pixmap(size)
    p = _painter(px)
    s = size
    w = s * 0.055

    pen = QPen(QColor(color), w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    cx, cy = s * 0.5, s * 0.5
    r_inner = s * 0.12
    r_outer = s * 0.32

    p.drawEllipse(QPointF(cx, cy), r_inner, r_inner)

    teeth = 8
    for i in range(teeth):
        a = math.radians(i * (360 / teeth))
        x1 = cx + r_inner * 1.3 * math.cos(a)
        y1 = cy + r_inner * 1.3 * math.sin(a)
        x2 = cx + r_outer * math.cos(a)
        y2 = cy + r_outer * math.sin(a)
        p.drawLine(QPointF(x1, y1), QPointF(x2, y2))

    p.end()
    return QIcon(px)


def icon_about(color="#89b4fa", size=48):
    px = _pixmap(size)
    p = _painter(px)
    s = size
    w = s * 0.06

    pen = QPen(QColor(color), w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    cx, cy = s * 0.5, s * 0.5
    r = s * 0.32
    p.drawEllipse(QPointF(cx, cy), r, r)

    dot_w = s * 0.08
    pen2 = QPen(QColor(color), dot_w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
    p.setPen(pen2)
    p.drawPoint(QPointF(cx, cy - r * 0.38))

    pen3 = QPen(QColor(color), w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
    p.setPen(pen3)
    p.drawLine(QPointF(cx, cy - r * 0.08), QPointF(cx, cy + r * 0.42))

    p.end()
    return QIcon(px)


def icon_theme_toggle(is_dark=True, color="#89b4fa", size=48):
    px = _pixmap(size)
    p = _painter(px)
    s = size
    w = s * 0.06

    pen = QPen(QColor(color), w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
    p.setPen(pen)

    cx, cy = s * 0.5, s * 0.5
    r = s * 0.28

    if is_dark:
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(QPointF(cx, cy), r, r)

        ray_len = s * 0.1
        ray_start = r + s * 0.04
        for i in range(8):
            a = math.radians(i * 45)
            x1 = cx + ray_start * math.cos(a)
            y1 = cy + ray_start * math.sin(a)
            x2 = cx + (ray_start + ray_len) * math.cos(a)
            y2 = cy + (ray_start + ray_len) * math.sin(a)
            p.drawLine(QPointF(x1, y1), QPointF(x2, y2))
    else:
        p.setBrush(Qt.BrushStyle.NoBrush)

        path = QPainterPath()
        path.arcMoveTo(cx - r, cy - r, r * 2, r * 2, -40)
        path.arcTo(cx - r, cy - r, r * 2, r * 2, -40, 260)

        offset = r * 0.6
        path.arcTo(cx - r + offset, cy - r - offset * 0.2, r * 1.6, r * 1.6, 200, -220)

        p.drawPath(path)

    p.end()
    return QIcon(px)