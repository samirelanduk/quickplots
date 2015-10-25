import matplotlib.pyplot as plt

class Chart:
    """A generic chart object."""

    def show(self):
        """Show the chart in a separate window"""
        self._generate().show()


    def save(self, path):
        """Save the chart to file. This just uses matplotlib's savefig
        method so all the matplotlib file extensions are supported."""
        self._generate().savefig(path)



class Figure(Chart):
    """A figure with multiple charts"""

    def __init__(self, rows, columns, charts):

        self.rows = rows
        self.columns = columns
        self.charts = charts


    def _generate(self):
        fig = plt.figure()

        chart_no = 1
        for chart in self.charts:
            assert isinstance(chart, SingleChart)
            plt.subplot(self.rows, self.columns, chart_no)
            chart._paint_axes(plt)
            chart_no += 1
        return fig



class SingleChart(Chart):
    """A chart with a single plot area"""

    def __init__(self, title=""):

        self.title = title


    def _paint_axes(self, axes):
        try:
            axes.set_title(self.title)
        except AttributeError:
            axes.title(self.title)


    def _generate(self):
        fig, ax = plt.subplots()
        SingleChart._paint_axes(self, ax)
        return fig



class PieChart(SingleChart):
    """A pie chart"""

    def __init__(self, values, labels=None, colors=None, value_format=None, title=""):

        #Initialise generic chart info
        SingleChart.__init__(self, title=title)

        #Assign the core values of this piechart
        self.values = values

        #Sort out the colours and labels for each data point
        self.labels = labels
        self.colors = colors

        #Determine how the values should be formatted
        self.value_format = value_format


    def _paint_axes(self, axes):
        SingleChart._paint_axes(self, axes)
        axes.pie(self.values, labels=self.labels, colors=self.colors, autopct=self.value_format, startangle=90)
        axes.axis("equal")


    def _generate(self):
        fig = SingleChart._generate(self)
        PieChart._paint_axes(self, fig.axes[0])
        return fig



class AxisChart(SingleChart):
    """A generic axis-based chart.

    This class is the parent class of all chart types which have a y and x axis
    (line charts, scatter plots etc.) but not things like pie charts, which
    inherit directly from class SingleChart."""

    def __init__(self, xlabel=None, xticks=None,
    xticklabels=None, xlim=None, ylabel=None, yticks=None, yticklabels=None,
    ylim=None, grid=False, title=""):

        SingleChart.__init__(self, title=title)

        self.xlabel = xlabel
        self.xticks = xticks
        self.xticklabels = xticklabels
        self.xlim = xlim
        self.ylabel = ylabel
        self.yticks = yticks
        self.yticklabels = yticklabels
        self.ylim = ylim
        self.grid = grid


    def _paint_axes(self, axes):
        SingleChart._paint_axes(self, axes)

        #Assign title of x-axis
        if self.xlabel is not None:
            try:
                axes.set_xlabel(self.xlabel)
            except AttributeError:
                axes.xlabel(self.xlabel)

        #Assign xticks
        if self.xticks is not None:
            try:
                axes.set_xticks(self.xticks)
            except AttributeError:
                if self.xticklabels is not None:
                    axes.xticks(self.xticks, self.xticklabels)
                else:
                    axes.xticks(self.xticks)
        if self.xticklabels is not None:
            try:
                axes.set_xticklabels(self.xticklabels)
            except AttributeError:
                pass

        #Assign limits of x-axis
        try:
            axes.xlim(self.xlim)
        except AttributeError:
            axes.set_xlim(self.xlim)

        #Assign title of y-axis
        if self.ylabel is not None:
            try:
                axes.set_ylabel(self.ylabel)
            except AttributeError:
                axes.ylabel(self.ylabel)

        #Assign yticks
        if self.yticks is not None:
            try:
                axes.set_yticks(self.yticks)
            except AttributeError:
                if self.yticklabels is not None:
                    axes.yticks(self.yticks, self.yticklabels)
                else:
                    axes.yticks(self.yticks)
        if self.yticklabels is not None:
            try:
                axes.set_yticklabels(self.yticklabels)
            except:
                pass

        #Assign limits of y-axis
        try:
            axes.ylim(self.ylim)
        except AttributeError:
            axes.set_ylim(self.ylim)

        #Set the grid
        axes.grid(self.grid)


    def _generate(self):
        fig = SingleChart._generate(self)
        AxisChart._paint_axes(self, fig.axes[0])
        return fig



class SingleSeriesAxisChart(AxisChart):
    """This class represents charts with axis which have only one series on them"""

    def __init__(self, xdata=None, ydata=None, xlabel=None, xticks=None,
    xticklabels=None, xlim=None, ylabel=None, yticks=None, yticklabels=None,
    ylim=None, grid=False, title=""):

        AxisChart.__init__(self, xlabel=xlabel, xticks=xticks,
        xticklabels=xticklabels, xlim=xlim, ylabel=ylabel, yticks=yticks,
        yticklabels=yticklabels, ylim=ylim, grid=grid, title=title)

        self.xdata = xdata
        self.ydata = ydata


    def _paint_axes(self, axes):
        AxisChart._paint_axes(self, axes)


    def _generate(self):
        fig = AxisChart._generate(self)
        SingleSeriesAxisChart._paint_axes(self, fig.axes[0])
        return fig



class MultiSeriesAxisChart(AxisChart):
    """This class represents charts with axis which have only multiple series on them"""

    def __init__(self, charts, xlabel=None, xticks=None,
    xticklabels=None, xlim=None, ylabel=None, yticks=None, yticklabels=None,
    ylim=None, grid=False, title=""):

        AxisChart.__init__(self, xlabel=xlabel, xticks=xticks,
        xticklabels=xticklabels, xlim=xlim, ylabel=ylabel, yticks=yticks,
        yticklabels=yticklabels, ylim=ylim, grid=grid, title=title)

        self.charts = charts


    def _paint_axes(self, axes):
        for chart in self.charts:
            assert isinstance(chart, SingleSeriesAxisChart)


    def _generate(self):
        fig = AxisChart._generate(self)
        MultiSeriesAxisChart._paint_axes(self, fig.axes[0])
        return fig




class LineChart(SingleSeriesAxisChart):

    def __init__(self, xdata, ydata, line_color=None, line_width=1, xlabel=None,
    xticks=None, xticklabels=None, xlim=None, ylabel=None, yticks=None,
    yticklabels=None, ylim=None, grid=False, title=""):

        SingleSeriesAxisChart.__init__(self, xdata=xdata, ydata=ydata,
        xlabel=xlabel, xticks=xticks, xticklabels=xticklabels, xlim=xlim,
        ylabel=ylabel, yticks=yticks, yticklabels=yticklabels, ylim=ylim,
        grid=grid, title=title)

        self.line_color = line_color
        self.line_width = line_width


    def _paint_axes(self, axes):
        SingleSeriesAxisChart._paint_axes(self, axes)
        axes.plot(self.xdata, self.ydata, color=self.line_color, linewidth=self.line_width)


    def _generate(self):
        fig = SingleSeriesAxisChart._generate(self)
        LineChart._paint_axes(self, fig.axes[0])
        return fig



class BarChart(SingleSeriesAxisChart):

    def __init__(self, xdata, ydata, width=0.8, align="center", fill_color=None,
    line_width=None, edge_color=None, xlabel=None, xticks=None, xticklabels=None,
    xlim=None, ylabel=None, yticks=None, yticklabels=None, ylim=None, grid=False, title=""):

        SingleSeriesAxisChart.__init__(self, xdata=xdata, ydata=ydata,
        xlabel=xlabel, xticks=xticks, xticklabels=xticklabels, xlim=xlim,
        ylabel=ylabel, yticks=yticks, yticklabels=yticklabels, ylim=ylim,
        grid=grid, title=title)

        self.width = width
        self.align = align
        self.fill_color = fill_color
        self.line_width = line_width
        self.edge_color = edge_color


    def _paint_axes(self, axes):
        SingleSeriesAxisChart._paint_axes(self, axes)
        axes.bar(self.xdata, self.ydata, width=self.width, align=self.align,
        color=self.fill_color, linewidth=self.line_width, edgecolor=self.edge_color)


    def _generate(self):
        fig = SingleSeriesAxisChart._generate(self)
        BarChart._paint_axes(self, fig.axes[0])
        return fig



class ScatterChart(SingleSeriesAxisChart):

    def __init__(self, xdata, ydata, marker="x", color="b", edge_color=None,
    edge_width=1, area=30, xlabel=None, xticks=None, xticklabels=None, xlim=None,
    ylabel=None, yticks=None, yticklabels=None, ylim=None, grid=False, title=""):

        SingleSeriesAxisChart.__init__(self, xdata=xdata, ydata=ydata,
        xlabel=xlabel, xticks=xticks, xticklabels=xticklabels, xlim=xlim,
        ylabel=ylabel, yticks=yticks, yticklabels=yticklabels, ylim=ylim,
        grid=grid, title=title)

        self.marker = marker
        self.color = color
        self.edge_color = edge_color
        self.edge_width = edge_width
        self.area = area


    def _paint_axes(self, axes):
        SingleSeriesAxisChart._paint_axes(self, axes)
        print("Painting scatter")
        axes.scatter(self.xdata, self.ydata, marker=self.marker, c=self.color,
        edgecolor=self.edge_color, linewidth=self.edge_width, s=self.area)


    def _generate(self):
        fig = SingleSeriesAxisChart._generate(self)
        ScatterChart._paint_axes(self, fig.axes[0])
        return fig
