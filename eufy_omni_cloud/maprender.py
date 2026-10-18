"""Render a :class:`~eufy_omni_cloud.mapstream.RobotMap` to PNG with Pillow.

Kept separate from the decoder so the decoder has no imaging dependency. Home
Assistant ships Pillow, so the integration can always import this module.
"""

from __future__ import annotations

import io
import math

from PIL import Image, ImageDraw

from .mapstream import PIXEL_CARPET, PIXEL_FREE, PIXEL_OBSTACLE, RobotMap

BACKGROUND = (0, 0, 0, 0)
WALL = (70, 70, 80, 255)
FLOOR = (205, 208, 214, 255)
CARPET = (190, 185, 170, 255)
PATH = (40, 110, 200, 220)
ROBOT = (255, 140, 0, 255)
ROBOT_EDGE = (120, 60, 0, 255)
DOCK = (40, 160, 70, 255)
FORBIDDEN = (220, 50, 50, 255)
NO_MOP = (240, 150, 30, 255)
WALL_LINE = (220, 50, 50, 255)

# Distinct, muted room colours; index = room id modulo table length.
ROOM_COLOURS = [
    (164, 196, 240), (190, 226, 176), (247, 205, 160), (214, 190, 236), (248, 232, 150),
    (168, 220, 226), (242, 180, 200), (196, 228, 212), (226, 204, 180), (182, 198, 230),
    (210, 232, 170), (240, 192, 176), (200, 184, 224), (234, 222, 166), (176, 214, 236),
]


def _cell_colour(rmap: RobotMap, cx: int, cy: int) -> tuple[int, int, int, int]:
    pv = rmap.pixel(cx, cy)
    if pv == PIXEL_OBSTACLE:
        return WALL
    if pv not in (PIXEL_FREE, PIXEL_CARPET):
        return BACKGROUND
    if rmap.room_grid is not None and rmap.grid is not None:
        # room grid may have its own origin; translate through world coordinates
        wx = rmap.grid.origin_x + cx * rmap.grid.resolution
        wy = rmap.grid.origin_y + cy * rmap.grid.resolution
        rid = rmap.room_at(wx, wy)
        # ids above 31 (32 seen on the C28) mark cells outside any room
        if rid and rid < 32 and (not rmap.rooms or rid in rmap.rooms):
            r, g, b = ROOM_COLOURS[(rid - 1) % len(ROOM_COLOURS)]
            if pv == PIXEL_CARPET:
                r, g, b = (r * 9 // 10, g * 9 // 10, b * 9 // 10)
            return (r, g, b, 255)
        # free space outside every room (lidar seen through windows and doors): hide it,
        # as the app does, so the floor plan ends at the house
        return BACKGROUND
    return CARPET if pv == PIXEL_CARPET else FLOOR


def render_png(rmap: RobotMap, *, max_size: int = 800, show_path: bool = True) -> bytes:
    """Return PNG bytes; an empty 1x1 transparent image if there is no map yet."""
    if not rmap.has_map or rmap.grid is None:
        img = Image.new("RGBA", (1, 1), BACKGROUND)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

    g = rmap.grid
    base = Image.new("RGBA", (g.width, g.height), BACKGROUND)
    px = base.load()
    for cy in range(g.height):
        row = g.height - 1 - cy  # robot y grows upwards; images grow downwards
        for cx in range(g.width):
            c = _cell_colour(rmap, cx, cy)
            if c is not BACKGROUND:
                px[cx, row] = c

    scale = max(1, min(max_size // g.width, max_size // g.height))
    img = base.resize((g.width * scale, g.height * scale), Image.NEAREST) if scale > 1 else base
    draw = ImageDraw.Draw(img)

    def to_img(x_cm: float, y_cm: float) -> tuple[float, float]:
        fx = (x_cm - g.origin_x) / g.resolution
        fy = (y_cm - g.origin_y) / g.resolution
        return (fx + 0.5) * scale, (g.height - 1 - fy + 0.5) * scale

    for zone in rmap.forbidden_zones:
        draw.polygon([to_img(x, y) for x, y in zone], outline=FORBIDDEN, width=max(1, scale // 2))
    for zone in rmap.no_mop_zones:
        draw.polygon([to_img(x, y) for x, y in zone], outline=NO_MOP, width=max(1, scale // 2))
    for (x0, y0), (x1, y1) in rmap.virtual_walls:
        draw.line([to_img(x0, y0), to_img(x1, y1)], fill=WALL_LINE, width=max(1, scale // 2))

    if show_path and len(rmap.path) > 1:
        seg: list[tuple[float, float]] = []
        for p in rmap.path:
            if p.new_segment and len(seg) > 1:
                draw.line(seg, fill=PATH, width=max(1, scale // 2))
                seg = []
            elif p.new_segment:
                seg = []
            seg.append(to_img(p.x, p.y))
        if len(seg) > 1:
            draw.line(seg, fill=PATH, width=max(1, scale // 2))

    r = max(2.0, scale * 1.2)
    for x, y, _theta in rmap.docks:
        ix, iy = to_img(x, y)
        draw.rectangle([ix - r, iy - r, ix + r, iy + r], fill=DOCK)

    if rmap.pose is not None:
        x, y, theta = rmap.pose
        ix, iy = to_img(x, y)
        rr = max(3.0, scale * 1.6)
        draw.ellipse([ix - rr, iy - rr, ix + rr, iy + rr], fill=ROBOT, outline=ROBOT_EDGE, width=1)
        # heading tick; theta is radians * 100 in the robot's frame (y up)
        ang = theta / 100.0
        draw.line([(ix, iy), (ix + math.cos(ang) * rr * 1.8, iy - math.sin(ang) * rr * 1.8)], fill=ROBOT_EDGE, width=max(1, scale // 2))

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()
