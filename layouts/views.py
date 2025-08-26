from django.shortcuts import render
from django.views.generic import TemplateView


class LayoutsView(TemplateView):
    pass

layouts_horizontal_view = LayoutsView.as_view(template_name="layouts/layouts-horizontal.html")
layouts_detached_view = LayoutsView.as_view(template_name="layouts/layouts-detached.html")
layouts_column_view = LayoutsView.as_view(template_name="layouts/layouts-two-column.html")
layouts_hovered_view = LayoutsView.as_view(template_name="layouts/layouts-vertical-hovered.html")
layouts_vertical_view =LayoutsView.as_view(template_name="layouts/layouts-vertical.html")

