from typing import Dict

import folium
from matplotlib.figure import Figure
from pandas import DataFrame

import matplotlib.pyplot as plt


def generate_value_count_barh(target_column: str):
    def get_value_count_plot(df: DataFrame) -> Figure:
        fig = df[target_column].value_counts().plot.barh().get_figure()
        plt.close()
        return fig
    return get_value_count_plot


def get_basis_of_record_by_collection_code_plot(df: DataFrame) -> Figure:
    fig = df.groupby(["collectionCode", "basisOfRecord"])['basisOfRecord'].count().unstack().plot.barh(stacked=True).get_figure()
    plt.close()
    return fig


def get_elevation_plot(df: DataFrame) -> Figure:
    fig = df['elevation'].plot.hist().get_figure()
    plt.close()
    return fig


def get_collection_code_map(df: DataFrame) -> folium.Map:
    from bnhm.espm_module import assign_colors
    color_dict, html_key = assign_colors(df, "collectionCode")

    mapa = folium.Map(location=[37.359276, -122.179626], zoom_start=5)  # Folium is a useful library for generating
    # Google maps-like map visualizations.
    for r in df.iterrows():
        lat = r[1]['decimalLatitude']
        long = r[1]['decimalLongitude']
        folium.CircleMarker((lat, long), color=color_dict[r[1]['collectionCode']], popup=r[1]['collectionCode']).add_to(
            mapa)

    return mapa


def get_reserve_data() -> Dict:
    import requests
    from shapely.geometry import mapping
    from shapely import wkt

    url = 'https://ecoengine.berkeley.edu/api/layers/reserves/features/'
    reserves = requests.get(url, params={'page_size': 30}).json()
    station_urls = {
        'Blodgett': 'https://raw.githubusercontent.com/BNHM/spatial-layers/master/wkt/BlodgettForestResearchStation.wkt',
        'Sagehen': 'https://raw.githubusercontent.com/BNHM/spatial-layers/master/wkt/SagehenCreekFieldStation.wkt'
    }
    reserves['features'] += [
        {'type': "Feature", 'properties': {"name": name}, 'geometry': mapping(wkt.loads(requests.get(url).text))}
        for name, url in station_urls.items()]
    return reserves


def get_reserve_map(df: DataFrame, reserve_data: Dict) -> folium.Map:
    from bnhm.espm_module import assign_colors
    mapb = folium.Map([37.359276, -122.179626], zoom_start=5)

    color_dict, html_key = assign_colors(df, "collectionCode")

    points = folium.features.GeoJson(reserve_data)
    mapb.add_child(points)
    for r in df.iterrows():
        lat = r[1]['decimalLatitude']
        long = r[1]['decimalLongitude']
        folium.Circle((lat, long), 1, color=color_dict[r[1]['collectionCode']]).add_to(mapb)

    return mapb
