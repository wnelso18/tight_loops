"""Main module."""

import random
import ipyleaflet

class Map(ipyleaflet.Map):
    def __init__(self, center=(0,0), zoom=2, **kwargs) -> None:

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True
        super().__init__(center=center, zoom=zoom, **kwargs)

        if "layers_control" not in kwargs:
            kwargs["layers_control"] = True

        if kwargs["layers_control"]:
            self.add_layers_control()

        if "fullscreen_control" not in kwargs:
            kwargs["fullscreen_control"] = True
        
        if kwargs["fullscreen_control"]:
            self.add_fullscreen_control()
    
    def add_search_control(self, url = 'https://nominatim.openstreetmap.org/search?format=json&q={s}', position="topleft", **kwargs):
        """Adds a search control to the map."""
        search_control = ipyleaflet.SearchControl(url=url, position=position, **kwargs)
        self.add_control(search_control)
        return search_control
    
    def add_draw_control(self, **kwargs):
        """Adds a draw control to the map."""
        draw_control = ipyleaflet.DrawControl(**kwargs)
        draw_control.polyline =  {
            "shapeOptions": {
                "color": "#6bc2e5",
                "weight": 8,
                "opacity": 1.0
            }
        }
        draw_control.polygon = {
            "shapeOptions": {
                "fillColor": "#6be5c3",
                "color": "#6be5c3",
                "fillOpacity": 1.0
            },
            "drawError": {
                "color": "#dd253b",
                "message": "Oups!"
            },
            "allowIntersection": False
        }
        draw_control.circle = {
            "shapeOptions": {
                "fillColor": "#efed69",
                "color": "#efed69",
                "fillOpacity": 1.0
            }
        }
        draw_control.rectangle = {
            "shapeOptions": {
                "fillColor": "#fca45d",
                "color": "#fca45d",
                "fillOpacity": 1.0
            }
        }
        self.add_control(draw_control)
        return draw_control

    def add_layers_control(self, position= "topright", **kwargs):
        """Adds a layers control to the map."""
        layers_control = ipyleaflet.LayersControl(position=position, **kwargs)
        self.add_control(layers_control)
        return layers_control
    
    def add_fullscreen_control(self, **kwargs):
        """Adds a fullscreen control to the map."""
        fullscreen_control = ipyleaflet.FullScreenControl(**kwargs)
        self.add_control(fullscreen_control)
        return fullscreen_control
    
    def add_tile_layer(self, url, name, attribution, **kwargs):
        """Adds a tile layer to the map."""
        tile_layer = ipyleaflet.TileLayer(url=url, name=name, attribution=attribution, **kwargs)
        self.add_layer(tile_layer)
        return tile_layer
    
    def add_basemap(self, basemap, **kwargs):
        
        import xyzservices.providers as xyz

        if basemap.lower() == "roadmap":
            url = "http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}"
            self.add_tile_layer(url, name=basemap, attribution="Google")

        elif basemap.lower() == "satellite":
            url = "http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}"
            self.add_tile_layer(url, name=basemap, attribution="Google")

        else:
            try:
                basemap = eval(f"xyz.{basemap}")
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_layer(url, name=basemap.name, attribution=attribution, **kwargs)
            except:
                raise ValueError("Invalid basemap name.")
            
    def add_geojson(self, data, **kwargs):
        """Adds a GeoJSON layer to the map."""

        isinstance(data, str)
        import json
        with open(data, "r") as f:
            data = json.load(f)

        geojson = ipyleaflet.GeoJSON(data=data, **kwargs)
        self.add_layer(geojson)
        return geojson
    
    def add_shp(self, data, **kwargs):
        """Adds a Shapefile layer to the map."""
        import geopandas as gpd
        import json
        gdf = gpd.read_file(data)
        data = json.loads(gdf.to_json())
        geojson = ipyleaflet.GeoJSON(data=data, **kwargs)
        self.add_layer(geojson)
        return geojson
        

def generate_random_string(length=15):
    """Generates a random string."""
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length)])


