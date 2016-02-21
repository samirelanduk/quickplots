BASE = """<?xml version="1.0" encoding="utf-8"?>
<!-- Generator: QuickPlots  -->
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" xmlns="http://www.w3.org/2000/svg"
 xmlns:xlink="http://www.w3.org/1999/xlink" width="%ipx" height="%ipx">
%s
</svg>"""


def produce_svg(chart, dimensions):
    svg_list = []

    chart.canvas.request_repaint(dimensions[0], dimensions[1])
    for graphic in chart.canvas.graphics:
        svg_list.append(graphic.to_svg())

    return BASE % (dimensions[0], dimensions[1], "\n".join(svg_list))



SVG_LINE_STYLES = {
 "." : "1, 2",
 "--": "3, 2"
}


def _line_paint(graphic):
    style = "stroke-width:%i;stroke:%s;" % (graphic.width, graphic.color)
    return '<line x1="%i" y1="%i" x2="%i" y2="%i" style="%s" stroke-dasharray="%s"/>' % (
      graphic.start_x, graphic.start_y,
      graphic.end_x, graphic.end_y,
      style,
      SVG_LINE_STYLES.get(graphic.style)
     )


def _rectangle_paint(graphic):
    style = "stroke-width:%i;stroke:%s;fill:%s" % (
     graphic.line_width,
     graphic.line_color,
     graphic.fill_color
    )
    return '<rect x="%i" y="%i" width="%i" height="%i" style="%s" stroke-dasharray="%s"/>' % (
      graphic.x, graphic.y,
      graphic.width, graphic.height,
      style,
      SVG_LINE_STYLES.get(graphic.line_style)
     )


def _text_paint(graphic):
    anchor = None
    alignment = None
    if graphic.horizontal_align == "center":
        anchor = "middle"
    elif graphic.horizontal_align == "left":
        anchor = "start"
    elif graphic.horizontal_align == "right":
        anchor = "end"
    if graphic.vertical_align == "center":
        alignment = "middle"
    elif graphic.vertical_align == "top":
        alignment = "hanging"
    elif graphic.vertical_align == "bottom":
        alignment = "baseline"

    style = "font-family:%s;font-size:%i;color:%s" % (graphic.font, graphic.font_size, graphic.color)

    return '''<text x="%i" y="%i" text-anchor="%s" alignment-baseline="%s" style="%s">
        %s
    </text>''' % (
     graphic.x, graphic.y,
     anchor, alignment,
     style, graphic.text
    )
