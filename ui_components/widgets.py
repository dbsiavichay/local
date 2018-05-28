import json

from django import forms
from django.contrib.gis.forms import BaseGeometryWidget
from django.contrib.gis.geos import Point
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils import six
from django.utils.http import urlencode

from mapwidgets.constants import STATIC_MAP_PLACEHOLDER_IMAGE
from mapwidgets.settings import MapWidgetSettings, mw_settings


def minify_if_not_debug(asset):
    """
        Transform template string `asset` by inserting '.min' if DEBUG=False
    """
    return asset.format("" if not mw_settings.MINIFED else ".min")


class BasePointFieldMapWidget(BaseGeometryWidget):
    settings_namespace = None
    settings = None

    def __init__(self, *args, **kwargs):
        attrs = kwargs.get("attrs")
        self.attrs = {}
        for key in ('geom_type', 'map_srid', 'map_width', 'map_height', 'display_raw'):
            self.attrs[key] = getattr(self, key)

        if isinstance(attrs, dict):
            self.attrs.update(attrs)

        self.custom_settings = False

        if kwargs.get("settings"):
            self.settings = kwargs.pop("settings")
            self.custom_settings = True

    def map_options(self):
        if not self.settings:  # pragma: no cover
            raise ImproperlyConfigured('%s requires either a definition of "settings"' % self.__class__.__name__)

        if not self.settings_namespace:  # pragma: no cover
            raise ImproperlyConfigured('%s requires either a definition of "settings_namespace"' % self.__class__.__name__)

        if self.custom_settings:
            custom_settings = MapWidgetSettings(app_settings=self.settings)
            return json.dumps(getattr(custom_settings, self.settings_namespace))
        return json.dumps(self.settings)


class GooglePointFieldWidget(BasePointFieldMapWidget):
    template_name = "ui_components/widgets/google_point_field_widget.html"
    settings = mw_settings.GooglePointFieldWidget
    settings_namespace = "GooglePointFieldWidget"

    @property
    def media(self):
        css = {
            "all": [
                minify_if_not_debug("mapwidgets/css/map_widgets{}.css"),
            ]
        }

        js = [
            "https://maps.googleapis.com/maps/api/js?libraries=places&key={}".format(mw_settings.GOOGLE_MAP_API_KEY)
        ]

        if not mw_settings.MINIFED:  # pragma: no cover
            js = js + [
                "mapwidgets/js/jquery_class.js",
                "mapwidgets/js/django_mw_base.js",
                "mapwidgets/js/mw_google_point_field.js",
            ]
        else:
            js = js + [
                "mapwidgets/js/mw_google_point_field.min.js"
            ]

        return forms.Media(js=js, css=css)

    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = dict()

        field_value = {}
        if isinstance(value,  Point):
            field_value["lng"] = value.x
            field_value["lat"] = value.y

        if value and isinstance(value, six.string_types):
            coordinates = self.deserialize(value)
            field_value["lng"] = getattr(coordinates, "x", None)
            field_value["lat"] = getattr(coordinates, "y", None)

        extra_attrs = {
            "options": self.map_options(),
            "field_value": json.dumps(field_value)
        }

        attrs.update(extra_attrs)
        self.as_super = super(GooglePointFieldWidget, self)
        return self.as_super.render(name, value, attrs)