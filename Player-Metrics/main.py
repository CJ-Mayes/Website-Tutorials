import matplotlib.pyplot as plt

from mplsoccer import PyPizza, add_image, FontManager

# You can add your own labels should you want
# parameter list
params = [
    "Field A", "Field B", "Field C", "Field D", "Field E",
    "Field F", "Field G", "Field H",
    "Field I", "Field J", "Field K", "Field L"
]

# parameter list
#params = [""]*12

# values for corresponding parameters
# Values can be found on fbref website (supplied by StatsBomb)

# To build the template we set the values to zero
values = [0]*12

# instantiate PyPizza class
baker = PyPizza(
    params=params,                  # list of parameters
    straight_line_color="#000000",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_lw=1,               # linewidth of last circle
    other_circle_color="#000000",   # Inner circle dashed line color
    other_circle_lw=1,              # linewidth for other circles
    other_circle_ls="-.",           # linestyle for other circles
    background_color="#FFFFFF"      # Add a background colour - match to background of Tableau viz
)

fig, ax = baker.make_pizza(
    values,              # list of values
    figsize=(8,8),   # adjust figsize according to your need
    param_location=110,
    kwargs_values=dict(alpha=0),
    kwargs_slices=dict(
        facecolor="white",  #color the background of the circle
        zorder=2, linewidth=1
    ),
    color_blank_space="same",  # use same color to fill blank space
    blank_alpha=0.4  # alpha for blank-space colors
)
plt.show() #Graph to save down
