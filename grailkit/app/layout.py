# -*- coding: UTF-8 -*-
"""
    grailkit.app.layout
    ~~~~~~~~~~~~~~~~~~~

    Layout management component

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
from .component import Component


class Layout(Component):
    """Component with layout management capabilities"""

    def __init__(self, *args, **kwargs):
        super(Layout, self).__init__(*args, **kwargs)

        self._components = []

    def append(self, component):
        """Append component to layout

        Args:
            component (grailkit.app.Component): component widget
        Raises:
            ValueError: if given value is not valid component
        """

        if not isinstance(component, Component):
            raise ValueError('Given value is not instance of Component')

        self._components.append(component)

    def remove(self, component):
        """Remove component from layout

        Args:
            component (grailkit.app.Component): component to be removed
        """

        self._components.remove(component)

    def insert(self, index, component):
        """Insert `component` into layout at position `index`"""

        self._components.insert(index, component)

    def on_draw(self):
        """Draw this component"""

        for component in self._components:
            component.on_draw()


class HLayout(Layout):
    """Horizontal layout"""

    def on_draw(self):
        """Draw components of layout"""

        shift = 0
        length = len(self._components)
        sizes = [self.width / length] * length

        for index, component in enumerate(self._components):
            component.x = shift
            component.y = 0
            component.width = sizes[index]
            component.height = self.height
            component.draw()

            shift += sizes[index]


class VLayout(Layout):
    """Vertical layout"""

    def on_draw(self):
        pass


class GridLayout(Layout):
    """Grid layout"""

    def on_draw(self):
        pass
