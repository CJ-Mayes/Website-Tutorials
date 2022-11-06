# Pre-requisite pip install Circlify and matplotlib in the terminal.
import csv
import circlify
import matplotlib.pyplot as plt

#Sample Data
data = [{'id': 'World', 'datum': 6964195249, 'children': [

              {'id': "North America", 'datum': 450448697, 'children':
                  [
                     {'id': "United States", 'datum': 308865000},
                     {'id': "Mexico", 'datum': 107550697},
                     {'id': "Canada", 'datum': 34033000}
                  ]},

              {'id': "South America", 'datum': 278095425, 'children':
                  [
                     {'id': "Brazil", 'datum': 192612000},
                     {'id': "Colombia", 'datum': 45349000},
                     {'id': "Argentina", 'datum': 40134425}
                  ]},

              {'id': "Europe", 'datum': 209246682, 'children':
                  [
                     {'id': "Germany", 'datum': 81757600},
                     {'id': "France", 'datum': 65447374},
                     {'id': "United Kingdom", 'datum': 62041708}
                  ]},

              {'id': "Africa", 'datum': 311929000, 'children':
                  [
                     {'id': "Nigeria", 'datum': 154729000},
                     {'id': "Ethiopia", 'datum': 79221000},
                     {'id': "Egypt", 'datum': 77979000}
                  ]},

              {'id': "Asia", 'datum': 2745929500, 'children':
                  [
                     {'id': "China", 'datum': 1336335000},
                     {'id': "India", 'datum': 1178225000},
                     {'id': "Indonesia", 'datum': 231369500}
              ]}

    ]}]


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
        abs(circle.y) + circle.r,
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

with open('countries.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    # World Level
    for circle in circles:
        if circle.level != 1:
            continue
        x, y, r = circle
        label = circle.ex["id"]
        print(label,x,y,r)
        printdata = [label, x, y, r, rank]
        rank = rank + 1
        writer.writerow(printdata)

        # Not needed for Tableau
        ax.add_patch(plt.Circle((x, y), r*padding_outer, alpha=0.5, linewidth=2, color="lightblue"))

        # Continent Level
        for circle in circles:
            if circle.level != 2:
              continue
            x, y, r = circle
            label = circle.ex["id"]
            print(label,x,y,r)
            printdata = [label, x, y, r, rank]
            rank = rank + 1
            writer.writerow(printdata)

            # Not needed for Tableau
            ax.add_patch(plt.Circle((x, y), r*padding_outer, alpha=0.5, linewidth=2, color="lightblue"))

        # Country Level
        for circle in circles:
            if circle.level != 3:
              continue
            x, y, r = circle
            label = circle.ex["id"]
            print(label,x,y,r)
            printdata = [label, x, y, r, rank]
            rank = rank + 1
            writer.writerow(printdata)

            # Not needed for Tableau
            ax.add_patch(plt.Circle((x, y), r*padding_inner, alpha=0.5, linewidth=2, color="#69b3a2"))
            plt.annotate(label, (x,y), ha='center', color="white")

# Show The Example Of The Graph We Will Be Recreating!
plt.show()
