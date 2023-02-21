"""
pip install statsbombpy
pip install pandas
pip install numpy

example code for a match in Statsbomb
"""
import json
from mplsoccer import Pitch
from statsbombpy import sb
import pandas as pd
import numpy as np

from kloppy import statsbomb

match_events = statsbomb.load_open_data(
    match_id=22912,

    # Optional arguments
    coordinates="statsbomb"
)
events = match_events.to_pandas()
events.to_csv('events.csv', index=False)
