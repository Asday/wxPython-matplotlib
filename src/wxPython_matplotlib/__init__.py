import matplotlib.backends.backend_wxagg
import matplotlib.figure
import numpy
import wx


datasets = [
    [
        ['A', 5],
        ['B', 12],
        ['C', 2],
    ],
    [
        ['D', 3],
        ['E', 2],
        ['F', 6],
    ],
    [
        ['Much', 2],
        ['Longer', 7],
        ['Data value', 3],
        ['Names', 9],
    ],
]


class PlotPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.NO_FULL_REPAINT_ON_RESIZE)

        self.figure = matplotlib.figure.Figure()
        self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(
            parent=self,
            id=wx.ID_ANY,
            figure=self.figure,
        )

        self.set_size()
        self.draw()

        self._resize_flag = False

        self.set_binds()

    def set_binds(self):
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def set_size(self):
        dimensions = tuple(self.GetSize())

        self.SetSize(dimensions)
        self.canvas.SetSize(dimensions)

        self.figure.set_size_inches([
            float(dimension) / self.figure.get_dpi()
            for dimension in dimensions
        ])

    def draw(self):
        self.canvas.draw()

    # Event handlers
    def on_idle(self, event):
        if self._resize_flag:
            self._resize_flag = False
            self.set_size()

    def on_size(self, event):
        self._resize_flag = True


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(
            parent=None,
            id=wx.ID_ANY,
            title=wx.EmptyString,
            pos=wx.DefaultPosition,
            size=wx.Size(500, 300),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )

        sizer_bg = wx.BoxSizer(wx.VERTICAL)
        self.panel_bg = wx.Panel(
            parent=self,
            id=wx.ID_ANY,
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            style=wx.TAB_TRAVERSAL,
        )
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        self.button_change = wx.Button(
            parent=self.panel_bg,
            id=wx.ID_ANY,
            label=u"Change data",
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            style=0,
        )
        sizer_main.Add(self.button_change, proportion=0, flag=wx.ALL, border=5)
        self.panel_matplotlib = PlotPanel(parent=self.panel_bg)
        sizer_main.Add(
            self.panel_matplotlib,
            proportion=1,
            flag=wx.EXPAND | wx.ALL,
            border=5,
        )
        self.panel_bg.SetSizer(sizer_main)
        self.panel_bg.Layout()
        sizer_main.Fit(self.panel_bg)
        sizer_bg.Add(self.panel_bg, proportion=1, flag=wx.EXPAND, border=5)
        self.SetSizer(sizer_bg)
        self.Layout()

        self.SetMinSize(self.GetSize())

        self.dataset_index = 0

        self.on_change()  # Kick off the initial figure rendering.

        self.setbinds()

    def select_next_dataset(self):
        self.dataset_index += 1

    @property
    def dataset(self):
        return datasets[self.dataset_index % len(datasets)]

    def setbinds(self):
        self.button_change.Bind(wx.EVT_BUTTON, self.on_change)

    # Event handlers
    def on_change(self, event=None):
        self.panel_matplotlib.figure.clf()  # clear figure
        axes = self.panel_matplotlib.figure.gca()  # get current axes

        self.select_next_dataset()

        datapoints = numpy.array(range(len(self.dataset)))
        values = numpy.array([
            int(datapoint) for label, datapoint in self.dataset
        ])
        labelpositions = numpy.array(range(len(self.dataset)))
        labeltext = numpy.array([label for label, datapoint in self.dataset])

        axes.barh(datapoints, values)
        axes.set_yticks(labelpositions)
        axes.set_yticklabels(labeltext)

        self.panel_matplotlib.draw()


class App(wx.App):
    def __init__(self):
        super(App, self).__init__()
        self.mainframe = MainFrame()
        self.mainframe.Show()
        self.MainLoop()
