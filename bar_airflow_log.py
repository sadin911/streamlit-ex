# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 13:49:45 2023

@author: chonlatid.d
"""
import pandas as pd
import warnings
import re
import cx_Oracle
import uuid
from sqlalchemy import create_engine
import yaml
import argparse
import datetime

#%%
df0 = pd.read_csv('your_data.csv')
#%%
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Spectral6
#%%
# Group the data by subject and calculate the sum of num_norm and num_susp
grouped_data = df0.groupby('subject').sum()[['num_norm', 'num_susp']]

# Calculate the total count for each subject
grouped_data['total'] = grouped_data.sum(axis=1)

# Calculate the percentage of num_norm and num_susp
grouped_data['norm_percentage'] = grouped_data['num_norm'] / grouped_data['total'] * 100
grouped_data['susp_percentage'] = grouped_data['num_susp'] / grouped_data['total'] * 100

# Create a ColumnDataSource from the grouped data
source = ColumnDataSource(grouped_data)

# Create the figure
p = figure(x_range=grouped_data.index.tolist(), title='Percentage of num_norm and num_susp by Subject',
           toolbar_location=None, tools='', sizing_mode='stretch_width')

# Add the bars for num_norm and num_susp
p.vbar(x='subject', top='norm_percentage', width=0.5, source=source, color='green', legend_label='num_norm')
p.vbar(x='subject', top='susp_percentage', width=0.5, source=source, color='red', legend_label='num_susp', bottom='norm_percentage')

# Add hover tooltips
hover = HoverTool(tooltips=[('Subject', '@subject'), ('num_norm', '@num_norm{0}'), ('num_susp', '@num_susp{0}')])
p.add_tools(hover)

# Customize the plot
p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.major_label_orientation = 1.2

# Display the plot using Streamlit
st.bokeh_chart(p, use_container_width=True)