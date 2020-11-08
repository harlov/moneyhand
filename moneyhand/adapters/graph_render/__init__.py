from typing import List, Any

import matplotlib.pyplot as plt
from io import BytesIO

DPI = 150


def render_table(titles: List[Any], data: List[List[Any]]) -> BytesIO:
    fig = plt.figure(dpi=DPI, figsize=(5, 1))

    table = plt.table(cellLoc="left", cellText=data, colLabels=titles, loc="top")
    table.set_fontsize(14)
    table.scale(1, 2)

    plt.axis("off")
    plt.grid("off")

    file_obj = BytesIO()

    fig.savefig(file_obj, dpi=DPI, bbox_inches="tight", pad_inches=0.1)
    file_obj.seek(0)

    return file_obj
