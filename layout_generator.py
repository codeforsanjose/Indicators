import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

plotly.tools.set_credentials_file(username='manika15', api_key='dogNq5ILvZnKd5BzKOry')

class LayoutGenerator():
    def __init__(self):
        pass

    def get_layout(self, traces, years):
        layout = dict(title='Share of Households with Income >150k',
                      xaxis=dict(title='year', tickmode=years, nticks=5),
                      yaxis=dict(title='share of households', ticksuffix='%'),
                      width=1000,
                      height=450,
                      )
        fig = dict(data=traces, layout=layout)
        py.plot(fig, filename='styled-line')