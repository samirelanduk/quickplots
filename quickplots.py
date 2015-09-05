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
