from typing import List, Optional

class Point:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

class Box:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height

def pack_boxes(container: Box, boxes: List[Box]) -> List[Point]:
    """
    Pack boxes and return points

    # Three boxes that fix in two columns
    >>> pack_boxes(Box(10, 10), [Box(1, 5), Box(2, 5), Box(1, 1)])
    [(0, 0), (0, 5), (2, 0)]

    # Box is too wide
    >>> pack_boxes(Box(10, 10), [Box(1, 11)])
    []

    # Box is too tall
    >>> pack_boxes(Box(10, 10), [Box(11, 1)])
    []

    # One box fits and one doesn't
    >>> pack_boxes(Box(10, 10), [Box(1, 1), Box(1, 11)])
    [(0, 0)]
    """

    def pack_box(x: int, y: int, max_width: int, boxes: List[Box]) -> Optional[Point]:
        # No boxes left to pack is a terminal state
        if len(boxes) == 0:
            return
        box = boxes[0]
        # Too wide means nothing can be done
        if box.width + x > container.width:
            return
        # Too tall for the container means nothing can be done
        if box.height > container.height:
            return
        # Too tall for remaining space means try to pack the same box again
        if box.height + y > container.height:
            for p in pack_box(x + max_width, 0, 0, boxes):
                yield p
        # Box fits, add it and try next
        else:
            max_width = max(max_width, box.width)
            yield Point(x, y)
            for p in pack_box(x, y + box.height, max(max_width, box.width), boxes[1:]):
                yield p

    # Make an in-memory list, but could convert this entire function to lazy evaluate
    return list(pack_box(0, 0, 0, boxes))


# Two columns fit all boxes
# print([(p.x, p.y) for p in pack_boxes(
#     Box(10, 10), [Box(1, 5), Box(2, 5), Box(1, 1)]
# )])
