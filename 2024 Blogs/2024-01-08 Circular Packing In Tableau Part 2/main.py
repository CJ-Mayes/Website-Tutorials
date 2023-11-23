"""
This first bit of code is new, it takes a data.csv file and converts the columns into the json we need
"""

import pandas as pd
import os
import json
import circlify
import matplotlib.pyplot as plt

def find_children(df, parent_id):
    children_list = df[df["parent"] == parent_id].to_dict('records')
    for child in children_list:
        child['id'] = child.pop('id')
        child['datum'] = child.pop('datum')
        child['children'] = find_children(df, child["id"])
        del child['parent']   # delete parent field from child
    return children_list

# Get current working directory
cwd = os.getcwd()

# Read the dataframe from csv
df = pd.read_csv(os.path.join(cwd, 'data.csv'))

# Now manually set the first level elements (where parent is NaN or None)
df.fillna('None', inplace=True)
df['parent'] = df['parent'].astype(str)

output = []
for _, row in df[df["parent"] == 'None'].iterrows():
    node = dict(row)
    node.pop('parent')   # delete parent field from node
    output.append({
        'id': node['id'],
        'datum': node['datum'],
        'children': find_children(df, node['id'])
    })

# Print final json output
print(json.dumps(output, indent=2))
data = output

"""
The next bit of code is all about translating this Json into the format we want to use,
Let's make sure our datum values are considered actual values
"""

def convert_datum_to_integer(node):
    node['datum'] = int(node['datum'])
    for child in node.get('children', []):
        convert_datum_to_integer(child)

# Convert "datum" field to integers
for item in data:
    convert_datum_to_integer(item)

# Print the updated data
print(json.dumps(data, indent=4))

"""
The last bit of code is about converting the circles into x,y and radius co-ordinates ready for Tableau
"""

import pandas as pd

# Compute circle positions thanks to the circlify() function
# The maximum radius is set to 1.
circles = circlify.circlify(
    data,
    show_enclosure=False,
    target_enclosure=circlify.Circle(x=0, y=0, r=1)
)

# To ensure in Tableau the sizing works the fig size is the same x*y.
fig, ax = plt.subplots(figsize=(10,10))

# Add axes
ax.axis('on')

# Find axis boundaries, lim will be 1.0 with current settings
lim = max(
    max(
        abs(circle.x) + circle.r,
        abs(circle.y) + circle.r
    )
    for circle in circles
)
plt.xlim(-lim, lim)
plt.ylim(-lim, lim)

# Amend Radius zone, Make sure Inner pad always > than Outer pad
padding_outer = 1
padding_inner = 1

header = ['ID', 'X co-ord', 'Y-cord', 'Radius', 'Rank']
rank = 1

# Create an empty DataFrame
df = pd.DataFrame(columns=header)

# World Level
for circle in circles:
    if circle.level != 1:
        continue
    x, y, r = circle
    label = circle.ex["id"]
    print(label, x, y, r)
    printdata = [label, x, y, r, rank]
    rank = rank + 1
    df.loc[len(df)] = printdata

    # Not needed for Tableau
    ax.add_patch(plt.Circle((x, y), r*padding_outer, alpha=0.5, linewidth=2, color="lightblue"))

    # Continent Level
    for circle in circles:
        if circle.level != 2:
            continue
        x, y, r = circle
        label = circle.ex["id"]
        print(label, x, y, r)
        printdata = [label, x, y, r, rank]
        rank = rank + 1
        df.loc[len(df)] = printdata

        # Not needed for Tableau
        ax.add_patch(plt.Circle((x, y), r*padding_outer, alpha=0.5, linewidth=2, color="lightblue"))

    # Country Level
    for circle in circles:
        if circle.level != 3:
            continue
        x, y, r = circle
        label = circle.ex["id"]
        print(label, x, y, r)
        printdata = [label, x, y, r, rank]
        rank = rank + 1
        df.loc[len(df)] = printdata

        # Not needed for Tableau
        ax.add_patch(plt.Circle((x, y), r*padding_inner, alpha=0.5, linewidth=2, color="#69b3a2"))
        plt.annotate(label, (x,y), ha='center', color="white")

# Show The Example Of The Graph We Will Be Recreating!
plt.show()

# Print the DataFrame
print(df)
df.to_csv('output_data.csv')
