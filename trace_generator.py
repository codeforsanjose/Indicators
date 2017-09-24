import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

plotly.tools.set_credentials_file(username='manika15', api_key='dogNq5ILvZnKd5BzKOry')

class TraceGenerator():
    def __init__(self):
        pass

    def get_trace(self, values, years, name, color):
        trace = go.Scatter(
            x=years,
            y=values,
            name=name,
            line=dict(
                color=(color),
                width=4)
        )
        return trace

    def get_trace_bar(self, values, years, name, color):
        trace = go.Bar(
            x=years,
            y=values,
            name=name,
        )
        return trace
