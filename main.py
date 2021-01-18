import io
import json
import itertools
import pandas as pd
from jinja2 import Template
from functools import partial
from os.path import dirname, join
from collections import OrderedDict
import datetime as dt
import pdb

#Bokeh
from bokeh import events
from bokeh.io import curdoc
from bokeh.resources import CDN
from bokeh.embed import json_item
from bokeh.driving import linear
from bokeh.plotting import figure
from bokeh.models import ( ColumnDataSource, Select, CustomJS, 
                           CheckboxGroup, Slider, LinearAxis, Select,
                           Toggle, Label, Div, TextInput, DatetimeTickFormatter, 
                           Axis, Range1d, CrosshairTool, HoverTool, SaveTool, PanTool, WheelZoomTool, LassoSelectTool, BoxAnnotation)
from bokeh.layouts import row, column, gridplot

#Custom Modules
from plot_utils import *
from custom_js import *

#Data Source
df_ = pd.read_csv(join(dirname(__file__), './anomalies.csv'))
df_ = df_.fillna(df_.mean())
df_['timestamp'] = pd.to_datetime(df_['timestamp'],unit='ms')
fig = figure(tools="pan,wheel_zoom,box_zoom,undo,redo,reset,crosshair", y_axis_location='right', name='Anomaly Detection', css_classes=['plot'])

df1 = df_[0:149]
live = df_[150:]

df = ColumnDataSource(df1)

#fig.circle(df.data['timestamp'], df.data['reconstruction_error'], size=5, color="navy", alpha=0.5)
fig.line(x='timestamp', y='reconstruction_error', alpha=0.2, line_width=3, color='navy', source=df, width='scaled_width')

fig.xaxis.formatter=DatetimeTickFormatter(days=['%b %d'])


an = BoxAnnotation(bottom=0.1, fill_alpha=0.1, fill_color='firebrick')
fig.add_layout(an)


df_ = live.rename(columns={'index': 'level_0'})
df_ = df_.reset_index()
N = len(df_)
def simulate_tick_data():
    for i in range(0, N):
        yield df_.iloc[i]

tick = simulate_tick_data()
@linear()
def stream(step):
    new_data = next(tick)
    df.stream(new_data)

curdoc().add_periodic_callback(stream, 1000)

gp = gridplot([[fig]], sizing_mode='stretch_both', toolbar_location='below')


curdoc().add_root(gp)

    
