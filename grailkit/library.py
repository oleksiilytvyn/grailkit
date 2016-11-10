# -*- coding: UTF-8 -*-
"""
    grailkit.library
    ~~~~~~~~~~~~~~~~

    Interface to Grail library file
"""

from grailkit.dna import DNA, DNAError


class LibraryError(DNAError):
    """Library error of any kind"""

    pass


class Library(DNA):
    """Manage library file"""

    # file extension
    _file_extension = ".grail-library"

    def __init__(self, file_path, create=False):
        """Open or create a project

        Args:
            file_path (str): path to file
        """
        super(Library, self).__init__(file_path, create=create)

        if create:
            self._create("Grail Library",
                         parent=0,
                         entity_type=DNA.TYPE_LIBRARY)

        if not self.root():
            raise LibraryError("Library entity not found in file %s" % (file_path,))

    def create(self, name, entity_type=DNA.TYPE_ABSTRACT):
        """Create new library entity

        Returns: new item
        """

        item = self._create(name,
                            parent=self.root().id,
                            entity_type=entity_type,
                            factory=False)

        return item

    def root(self):
        """Get a library entity

        Returns: root item of library
        """

        root = self._entities(filter_type=DNA.TYPE_LIBRARY, filter_parent=0)

        return root[0] if len(root) > 0 else None

    def remove(self, entity_id):
        """Remove entity from library

        Args:
            entity_id (int): id of entity
        """

        self._remove(entity_id)

    def items(self, filter_type=False, filter_keyword=False):
        """Returns list of library items

        Args:
            filter_type: limit result set by type, pass False to disable filter
            filter_keyword (str): limit result set by keyword, pass False to disable filter
        """

        return self._entities(
            filter_type=filter_type,
            filter_parent=self.root().id,
            filter_keyword=filter_keyword)

    def item(self, entity_id):
        """Return library item by id

        Args:
            entity_id (int): entity identifier
        """

        return self._entity(entity_id)

    def find(self, keyword, filter_type=False, filter_parent=False):
        """Find entities by keyword in library and return list of entities found"""

        return self._entities(
            filter_type=filter_type,
            filter_parent=filter_parent,
            filter_keyword=keyword)
