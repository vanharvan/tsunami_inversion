import pygmt

# Region in 0–360 longitude
region = [120, 290, -60, 60]

# Create figure
fig = pygmt.Figure()

# Clip 10-min relief (prevents Windows crash)
grid = pygmt.grdcut("@earth_relief_10m", region=region)

# Bathymetry CPT
cpt = pygmt.makecpt(cmap="geo", continuous=True)

# Plot ocean relief
fig.grdimage(
    grid=grid,
    region=region,
    projection="R10i",  # Robinson projection (best for large oceans)
    shading=True,
    cmap=cpt,
)

# Add coastlines with grey land fill
fig.coast(
    land="gray70",                 # fill land with grey
    shorelines="0.5p,black",
    borders="1/0.5p,black",
)

# Frame with 0–360 longitudes
fig.basemap(
    region=region,
    projection="R10i",
    frame=[
        "xafg+u°",
        "yafg+u°",
        "+tPacific Basin Bathymetry (10-min)"
    ],
)

# Save output
fig.savefig("pacific_bathymetry_robinson_grey_land.png")
