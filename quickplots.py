import matplotlib.pyplot as plt

class Chart:
    """A generic chart object."""

    def __init__(self, title=""):
        self.set_title(title)


    def set_title(self, title):
        """Change the title of the chart"""
        self.title = title


    def _generate(self):
        """Get a matplotlib figure representation of this chart"""
        fig, ax = plt.subplots()
        ax.set_title(self.title)
        return fig


    def show(self):
        """Show the chart in a separate window"""
        self._generate().show()


    def save(self, path):
        """Save the chart to file. This just uses matplotlib's savefig
        method so all the matplotlib file extensions are supported."""
        self._generate().savefig(path)



class PieChart(Chart):

    def __init__(self, values, labels=None, colors=None, value_format=None, title=""):
        #Initialise generic chart info
        Chart.__init__(self, title=title)

        #Assign the core values of this piechart
        self.values = values

        #Sort out the colours and labels for each data point
        self.labels = labels
        self.colors = colors

        #Determine how the values should be formatted
        self.value_format = value_format


    def _generate(self):
        fig = Chart._generate(self)

        fig.axes[0].pie(self.values, labels=self.labels, colors=self.colors, autopct=self.value_format, startangle=90)
        fig.axes[0].axis("equal")
        return fig



class AxisChart(Chart):
    """A generic axis-based chart.

    This class is the parent class of all chart tyoes which have a y and x axis
    (line charts, scatter plots etc.) but not things like pie charts, which
    inherit directly from class Chart."""

    def __init__(self, xlabel=None, xticks=None, xticklabels=None, xlim=None, ylabel=None, yticks=None, yticklabels=None, ylim=None, grid=False, title=""):
        Chart.__init__(self, title=title)

        self.xlabel = xlabel
        self.xticks = xticks
        self.xticklabels = xticklabels
        self.xlim = xlim
        self.ylabel = ylabel
        self.yticks = yticks
        self.yticklabels = yticklabels
        self.ylim = ylim
        self.grid = grid


    def _generate(self):
        fig = Chart._generate(self)
        if self.xlabel is not None:
            fig.axes[0].set_xlabel(self.xlabel)
        if self.xticks is not None:
            fig.axes[0].set_xticks(self.xticks)
        if self.xticklabels is not None:
            fig.axes[0].set_xticklabels(self.xticklabels)
        fig.axes[0].set_xlim(self.xlim)
        if self.ylabel is not None:
            fig.axes[0].set_ylabel(self.ylabel)
        if self.yticks is not None:
            fig.axes[0].set_yticks(self.yticks)
        if self.yticklabels is not None:
            fig.axes[0].set_yticklabels(self.yticklabels)
        fig.axes[0].set_ylim(self.ylim)
        fig.axes[0].grid(self.grid)

        return fig
