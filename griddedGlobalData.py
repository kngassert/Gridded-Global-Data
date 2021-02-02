import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
from colour import Color
import matplotlib.image as image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


class GriddedDataPlot:
    def __init__(self, filename, separator):
        # index;lon;lat;data (presorted by lon then lat value)
        read_data = pd.read_csv(filename, header=0, sep=separator)
        num_lon = len(read_data['lon'].value_counts())
        num_lat = len(read_data['lat'].value_counts())
        num_elem = num_lon * num_lat
        if num_elem != len(read_data['lat']):
            print("ERROR: not a regular grid")

        # reshape to grid
        self.lon = read_data['lon'].to_numpy().reshape(num_lon, num_lat)
        self.lat = read_data['lat'].to_numpy().reshape(num_lon, num_lat)
        self.data = read_data['de'].to_numpy().reshape(num_lon, num_lat)

        if self.lon[0][0] != self.lon[0][1]:
            print("ERROR: remapping not correct")

    def draw_map_world(self, data2plot, proj, lat0, lon0, mincolor, maxcolor, clevels, colorbar_label, extendtext):
        m = Basemap(projection=proj, resolution='c', lon_0=lon0, lat_0=lat0)
        m.drawcoastlines(linewidth=0.5)
        m.drawcountries(linewidth=0.5)
        x, y = m(self.lon, self.lat)

        colors = list(mincolor.range_to(maxcolor, len(clevels) + 1))
        colors = [c.hex for c in colors]  # otherwise error reading colors when plotting

        # colorbar extend options
        if extendtext == 'min':
            colormap = mpl.colors.ListedColormap(colors[1:])
            colormap.set_under(colors[0])
        elif extendtext == 'max':
            colormap = mpl.colors.ListedColormap(colors[:-1])
            colormap.set_over(colors[-1])
        elif extendtext == 'both':
            colormap = mpl.colors.ListedColormap(colors[1:-1])
            colormap.set_under(colors[0])
            colormap.set_over(colors[-1])
        else:
            colormap = mpl.colors.ListedColormap(colors)

        m.contourf(x, y, data2plot, levels=clevels, cmap=colormap, extend=extendtext)
        m.colorbar(location='right', extendfrac='auto').set_label(colorbar_label, size=16)
        return m


# load data, presorted by lon, then lat, value
gridData = GriddedDataPlot('sampleData.txt', ';')

# plot
fig, ax = plt.subplots(figsize=(16, 9))

logo = image.imread('logo1.png')
imagebox = OffsetImage(logo, zoom=0.05)
ab = AnnotationBbox(imagebox, (0, 0), box_alignment=(0, 0))
ax.add_artist(ab)

colorLevels = np.arange(.5, 1.01, .1)
minColor = Color('#8CCBFE')
maxColor = Color('#0871B0')

colorbarLabel = 'Data values'
extendPref = 'min'  # max, min, both, neither (for colorbar)

gridData.draw_map_world(gridData.data, 'moll', 0, 0, minColor, maxColor, colorLevels, colorbarLabel, extendPref)

plt.title('Gridded Global Data\n', fontsize=24)
plt.show()

# plt.savefig('griddedGlobalData.png', dpi=96)


