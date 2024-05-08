from dash import Dash, html, dash_table,dcc, callback, Output, Input

import pandas as pd

import geopandas as gpd

import plotly.express as px





def load_ev_data():
    df = pd.read_csv('Data/Electric_Vehicle_Population_Data.csv')
    #Now we need to convert our dataframe into shapely data inside 
    # a geo dataframe.

    df = df.dropna().copy()
    #Converting from string to shapely data.
    df['Vehicle Location'] =  gpd.GeoSeries.from_wkt(df['Vehicle Location'])
    #Converting to geodataframe
    geo_df = gpd.GeoDataFrame(df,geometry = 'Vehicle Location')

    

    return geo_df


geo_df = load_ev_data()
myCenter = geo_df.dissolve().centroid




def plot_owner_locations(geo_df , num_samples):

    A = geo_df.sample(num_samples,random_state = 0).copy()
    # myCenter = geo_df.dissolve().centroid

    

    fig  = px.scatter_geo(A, lat = A.geometry.y, lon = A.geometry.x, center = {'lon' : myCenter.x[0],'lat': myCenter.y[0]})
    fig.update_layout(
        title = 'EV and Hybrid Car Owner Locations where Vehicle is registered with the Washington State Department of Licensing',
        geo_scope='usa',
        
    )

    fig.update_geos(fitbounds="locations")

    return fig






option_list = geo_df['Make']\
    .value_counts().sort_values(ascending = False).index[0:5]


app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='Dashboard'),
    html.Hr(),
    html.Div(
        children='This is a dashboard displaying the locations of \
            electric vehicles registered with the \
                Washington State DMV, filtered by the car\'s make'),
    html.Hr(),
    dcc.RadioItems(options=option_list,
         value=option_list[0], id='controls-and-radio-item'), #label (1) ; Sends to (2)
         dcc.Graph(figure={}, id='controls-and-graph') ])





@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_map(make_chosen):

    geo_df_slice = geo_df[geo_df['Make'] ==  make_chosen]
    fig  = plot_owner_locations(geo_df_slice, 100)
    return fig


if __name__ == '__main__':
    app.run(debug=True)



