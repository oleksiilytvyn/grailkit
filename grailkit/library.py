# -*- coding: UTF-8 -*-
"""
    grailkit.library
    ~~~~~~~~~~~~~~~~

    Interface to library file
"""
from grailkit.dna import DNA, DNAError


class LibraryError(DNAError):
    pass


class Library(DNA):
    """Manage library"""

    TYPE_SONG = 0
    TYPE_FILE = 1
    TYPE_MEDIA = 2

    TYPES = (TYPE_SONG, TYPE_FILE, TYPE_MEDIA)

    # file extension
    _file_extension = ".grail-library"

    def __init__(self, file_path):
        """Open or create a project

        Args:
            file_path (str): path to file
        """
        super(Library, self).__init__(file_path, create=False)

        root = self._entities(filter_type=DNA.TYPE_LIBRARY, filter_parent=0)

        if len(root) == 0:
            raise LibraryError("Library entity not found in %s file" % (file_path,))

        self._root = root

    def create(self):
        """Create new library entity"""
        item = self._create(parent=self._root.id)

        return item

    def remove(self, entity_id):
        """Remove entity from library"""
        self._remove(entity_id)

    def items(self, filter_type=False, filter_keyword=False):
        return self._entities(
            filter_type=filter_type,
            filter_parent=self._root.id,
            filter_keyword=filter_keyword)

    def item(self, entity_id):
        return self._entity(entity_id)
