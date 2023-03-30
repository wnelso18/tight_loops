"""Main module."""

import random
import ipyleaflet

class Map(ipyleaflet.Map):
    def __init__(self, center, zoom, **kwargs) -> None:

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True
        super().__init__(center=center, zoom=zoom, **kwargs)
    
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


def generate_random_string(length=15):
    """Generates a random string."""
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length)])


