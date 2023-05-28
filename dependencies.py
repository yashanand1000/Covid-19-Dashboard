'''
file: dependencies.py
author: @vincit0re @yashanand1000
brief: This file contains all the dependencies required for the app to run.
date: 2023-04-27
'''

'''All the dependencies are imported here'''
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import plotly.express as px
import os
import geojson
import pandas as pd
from datetime import datetime
from datetime import date
from bs4 import BeautifulSoup
from requests_html import HTMLSession