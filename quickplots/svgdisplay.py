BASE = """
<?xml version="1.0" encoding="utf-8"?>
<!-- Generator: QuickPlots  -->
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" xmlns="http://www.w3.org/2000/svg"
 xmlns:xlink="http://www.w3.org/1999/xlink" width="%ipx" height="%ipx">
%s
</svg>"""


def produce_svg(chart, dimensions):
    svg = ""

    return BASE % (dimensions[0], dimensions[1], svg)
