"""Main module."""

import random
import ipyleaflet
import ipywidgets as widgets
from ipyleaflet import WidgetControl

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
        
        if "add_toolbar" not in kwargs:
            kwargs["add_toolbar"] = True

        if kwargs["add_toolbar"]:
            self.add_toolbar()

    
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
    
    def add_vector(self, data, **kwargs):
        """Adds a vector layer to the map."""
        import geopandas as gpd
        import json
        gdf = gpd.read_file(data)
        data = json.loads(gdf.to_json())
        geojson = ipyleaflet.GeoJSON(data=data, **kwargs)
        self.add_layer(geojson)
        return geojson
    
    def add_raster(self, url, name='Raster', fit_bounds=True, **kwargs):
        """Adds a raster layer to the map.

            Args:
                url (str): The URL of the raster.
                name (str): The name of the raster.
                fit_bounds (bool): Whether to fit the map bounds to the raster.
        """
        import httpx

        titiler_endpoint = "https://titiler.xyz" 

        r = httpx.get(
            f"{titiler_endpoint}/cog/info",
            params = {
                "url": url,
            }
        ).json()

        bounds = r["bounds"]

        r = httpx.get(
            f"{titiler_endpoint}/cog/tilejson.json",
            params = {
                "url": url,
            }
        ).json()

        tile = r["tiles"][0]

        self.add_tile_layer(url=tile, name=name, attribution="raster", **kwargs)

        if fit_bounds:
            bbox = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]
            self.fit_bounds(bbox)

    def add_local_raster(self, filename, name='Local Raster', **kwargs):
        try:
            import localtilesserver
        except ImportError:
            raise ImportError("Please install localtilesserver: pip install localtilesserver")
        
    def opacity_slider(self, value=0.1, min=0, max=1, position="bottomright"):
        """Adds an opacity slider to the map.
        
        Args:   
            value (float): The initial value of the slider.
            min (float): The minimum value of the slider.
            max (float): The maximum value of the slider.
            position (str): The position of the slider.
        """
        
        slider = widgets.FloatSlider(value=value, min=min ,max=max)
        widgets.jslink((self.layers[1], 'opacity'), (slider, 'value'))
        control = WidgetControl(widget=slider, position=position)
        self.add_control(control)

    def add_image(self, url, width, height, position="bottomleft"):
        """Adds an image to the map.
        
        Args:
            url (str): The URL of the image.
            width (str): The width of the image.
            height (str): The height of the image.
            position (str): The position of the image.
        """

        widget = widgets.HTML(value=f"<img src={url} width='{width}' height='{height}'>")
        control = WidgetControl(widget=widget, position = position)
        self.add_control(control)

    def add_toolbar(self, position="topright"):
        

        widget_width = "250px"
        padding = "0px 0px 0px 5px"  # upper, right, bottom, left

        toolbar_button = widgets.ToggleButton(
            value=False,
            tooltip="Toolbar",
            icon="wrench",
            layout=widgets.Layout(width="28px", height="28px", padding=padding),
        )

        close_button = widgets.ToggleButton(
            value=False,
            tooltip="Close the tool",
            icon="times",
            button_style="primary",
            layout=widgets.Layout(height="28px", width="28px", padding=padding),
        )

        toolbar = widgets.HBox([toolbar_button])

        def toolbar_click(change):
            if change["new"]:
                toolbar.children = [toolbar_button, close_button]
            else:
                toolbar.children = [toolbar_button]
                
        toolbar_button.observe(toolbar_click, "value")

        def close_click(change):
            if change["new"]:
                toolbar_button.close()
                close_button.close()
                toolbar.close()
                
        close_button.observe(close_click, "value")

        rows = 2
        cols = 2
        grid = widgets.GridspecLayout(rows, cols, grid_gap="0px", layout=widgets.Layout(width="65px"))

        icons = ["folder-open", "map", "bluetooth", "area-chart"]

        for i in range(rows):
            for j in range(cols):
                grid[i, j] = widgets.Button(description="", button_style="primary", icon=icons[i*rows+j], 
                                            layout=widgets.Layout(width="28px", padding="0px"))
                
        toolbar = widgets.VBox([toolbar_button])

        def toolbar_click(change):
            if change["new"]:
                toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
            else:
                toolbar.children = [toolbar_button]
                
        toolbar_button.observe(toolbar_click, "value")



        output = widgets.Output()
        output_ctrl = WidgetControl(widget=output, position="bottomright")
        self.add_control(output_ctrl)

        basemap = widgets.Dropdown(

            options = ["Satellite", "Roadmap"],
            value = None,
            description = "Basemap",
            style = {"description_width": "initial"},
            layout=widgets.Layout(width="250px")
        )
        
        
        basemap_ctrl = WidgetControl(widget=basemap, position="topright")

        def change_basemap(change):
            if change['new']:
                with output:
                    print(basemap.value)
                self.add_basemap(basemap.value)

        basemap.observe(change_basemap, names="value")

        def tool_click(b):
            with output:
                print(f"{b.icon} clicked")

                if b.icon == "map":
                    if basemap_ctrl not in self.controls:
                        self.add(basemap_ctrl)
        for i in range(rows):
            for j in range(cols):
                tool = grid[i, j]
                tool.on_click(tool_click)

        toolbar_ctrl = ipyleaflet.WidgetControl(widget=toolbar, position=position)

        self.add_control(toolbar_ctrl)












# def generate_random_string(length=15):
#     """Generates a random string."""
#     return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length)])
