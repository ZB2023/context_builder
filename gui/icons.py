from PySide6.QtGui import QPainter, QPixmap, QIcon, QColor, QPen, QFont, QPainterPath
from PySide6.QtCore import Qt, QRect, QPoint


def _create_pixmap(size=64):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    return pixmap


def icon_scan(color="#89b4fa", size=64):
    pixmap = _create_pixmap(size)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(color), size * 0.08)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    m = size * 0.15
    p.drawRoundedRect(int(m), int(m), int(size - 2 * m), int(size - 2 * m), size * 0.1, size * 0.1)

    y1, y2, y3 = size * 0.35, size * 0.5, size * 0.65
    x1, x2 = size * 0.3, size * 0.7
    p.drawLine(int(x1), int(y1), int(x2), int(y1))
    p.drawLine(int(x1), int(y2), int(x2), int(y2))
    p.drawLine(int(x1), int(y3), int(size * 0.55), int(y3))

    p.end()
    return QIcon(pixmap)


def icon_convert(color="#89b4fa", size=64):
    pixmap = _create_pixmap(size)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(color), size * 0.08)
    p.setPen(pen)

    cx, cy = size * 0.5, size * 0.5
    r = size * 0.3

    path1 = QPainterPath()
    path1.moveTo(cx + r * 0.7, cy - r * 0.7)
    path1.arcTo(cx - r, cy - r, r * 2, r * 2, 45, 270)
    p.drawPath(path1)

    p.drawLine(int(cx + r * 0.5), int(cy - r * 1.0), int(cx + r * 0.7), int(cy - r * 0.7))
    p.drawLine(int(cx + r * 1.0), int(cy - r * 0.5), int(cx + r * 0.7), int(cy - r * 0.7))

    p.end()
    return QIcon(pixmap)


def icon_delete(color="#f38ba8", size=64):
    pixmap = _create_pixmap(size)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(color), size * 0.08)
    p.setPen(pen)

    m = size * 0.25
    p.drawLine(int(m), int(m), int(size - m), int(size - m))
    p.drawLine(int(size - m), int(m), int(m), int(size - m))

    p.end()
    return QIcon(pixmap)


def icon_files(color="#89b4fa", size=64):
    pixmap = _create_pixmap(size)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(color), size * 0.07)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    p.drawRoundedRect(int(size * 0.2), int(size * 0.25), int(size * 0.45), int(size * 0.55), 4, 4)
    p.drawRoundedRect(int(size * 0.35), int(size * 0.15), int(size * 0.45), int(size * 0.55), 4, 4)

    p.end()
    return QIcon(pixmap)


def icon_settings(color="#89b4fa", size=64):
    pixmap = _create_pixmap(size)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(color), size * 0.07)
    p.setPen(pen)

    cx, cy = size * 0.5, size * 0.5
    r_out, r_in = size * 0.35, size * 0.15
    p.drawEllipse(QPoint(int(cx), int(cy)), int(r_in), int(r_in))

    for i in range(6):
        import math
        angle = math.radians(i * 60)
        x1 = cx + r_in * 0.9 * math.cos(angle)
        y1 = cy + r_in * 0.9 * math.sin(angle)
        x2 = cx + r_out * math.cos(angle)
        y2 = cy + r_out * math.sin(angle)
        p.drawLine(int(x1), int(y1), int(x2), int(y2))

    p.end()
    return QIcon(pixmap)


def icon_about(color="#89b4fa", size=64):
    pixmap = _create_pixmap(size)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    pen = QPen(QColor(color), size * 0.07)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    cx, cy = size * 0.5, size * 0.5
    r = size * 0.35
    p.drawEllipse(QPoint(int(cx), int(cy)), int(r), int(r))

    p.setPen(QPen(QColor(color), size * 0.09))
    p.drawLine(int(cx), int(cy - r * 0.1), int(cx), int(cy + r * 0.35))
    p.drawPoint(int(cx), int(cy - r * 0.4))

    p.end()
    return QIcon(pixmap)


def icon_theme(color="#89b4fa", size=64):
    pixmap = _create_pixmap(size)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    cx, cy = size * 0.5, size * 0.5
    r = size * 0.3

    p.setPen(QPen(QColor(color), size * 0.07))
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawEllipse(QPoint(int(cx), int(cy)), int(r), int(r))

    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(color))
    path = QPainterPath()
    path.moveTo(cx, cy - r)
    path.arcTo(cx - r, cy - r, r * 2, r * 2, 90, 180)
    path.lineTo(cx, cy - r)
    p.drawPath(path)

    p.end()
    return QIcon(pixmap)