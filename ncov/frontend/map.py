import geojson
from urllib.request import  urlopen
import plotly.graph_objects as go
from plotly.offline import plot

from .getdata import romania


def romania_map():
    with open("frontend/counties.json", "r", encoding="utf-8") as f:
        geometry = geojson.load(f)

    for k in range(len(geometry['features'])):
        geometry['features'][k]['id'] = k


    df = romania()

    locations = [0+k for k in range(42)]
    text = [feat['properties']['name'] for feat in geometry['features'] if feat['id'] in locations]  # province names
    z={}
    for i in range(len(text)):

        z[text[i]] =0


    for i in df.values:
        z[i[1]] = i[2]

    new_z = list(z.values())




    fig = go.Figure([
        go.Choropleth(
            geojson=geometry,
            colorscale='reds',
            locations=locations,
            text=text,
            z = new_z,






        )])


    fig.update_geos(
        fitbounds="locations",
        resolution=50,
        visible=True,
        showframe=False,
        projection={"type": "mercator"},
    )
    plot_div = plot(fig, include_plotlyjs=False, output_type='div', config={'displayModeBar': False})

    return plot_div
