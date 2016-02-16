#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

from grailkit.db import DataBaseHost, DataBaseError, DataBase


class GrailFileError(Exception):
    """Base class for GrailFile Errors"""
    pass


class GrailFile:
    """Grail file parser"""

    # database handler
    _db = None
    # file extension
    _file_extension = ".grail"

    def __init__(self, file_path=None, create=False):
        """Open a *.grail file

        Args:
            file_pathstr): path to file
            create (bool): create file if not exists

        Raises:
            GrailFileError: if file can't be parsed or not exists
        """

        if self.validate(file_path):
            raise GrailFileError("Grail file could not be opened.")
        else:
            self._db = DataBaseHost.get(file_path)

    def entities(self):
        return []

    def entity(self, id):
        return GrailFileEntity()

    def add_entity(self, entity):
        pass

    def update_entity(self, entity):
        pass

    def remove_entity(self, id):
        pass

    def set(self, entity_id, key, value, force_type=None):
        pass

    def get(self, entity_id, key):
        pass

    def optimize(self):
        """Remove broken properties and entities."""
        pass

    def validate(self, file_path):
        """Validate file to be proper grail file

        Args:
            file_path (str): path to file
        """
        if not os.path.isfile(file_path):
            return False

        # if file doesn't have proper extension
        if os.path.splitext(file_path)[1] != self._file_extension:
            return False

        return True


class GrailFileEntity:
    """Basic entity model, each entity can have many properties + some default fields"""

    TYPE_DEFAULT = 0
    TYPE_PROJECT = 1
    TYPE_LIBRARY = 2
    TYPE_BIBLE = 3
    TYPE_CUE = -1
    TYPE_FILE = -1

    def __init__(): pass

    # properties

    def get(self, key, type=None):
        return ""

    def set(self, key, value, type=None):
        pass

    def has(self, key):
        return True

    def remove(self, key):
        pass

    # fields
    @property
    def id(self):
        return 0

    @property
    def parent(self):
        return 0

    @property
    def name(self):
        return ""

    @property
    def type(self):
        return ""

    @type.setter
    def type(self, type):
        pass

    @property
    def created(self):
        return 0

    @property
    def modified(self):
        return 0

    @property
    def content(self):
        return ""

    @content.setter
    def content(self, content):
        pass

    @property
    def search(self):
        return ""

    @keywords.setter
    def keywords(self, keywords):
        pass
