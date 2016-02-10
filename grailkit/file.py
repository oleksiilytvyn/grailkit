#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from grailkit.core import DataBase, DataBaseHost, DataBaseError


class GrailFileError(Exception):
    pass


class GrailFile:

    # database handler
    _db = None

    def __init__( self, file=None ):
        pass

    def entities( self ):
        return []

    def entity( self, id ):
        return GrailFileEntity()

    def add_entity( self, entity ):
        pass

    def update_entity( self, entity ):
        pass

    def remove_entity( self, id ):
        pass

    def set( self, entity_id, key, value, type = None ):
        pass

    def get( self, entity_id, key ):
        pass

    def optimize( self ):
        """Remove broken properties and entities."""
        pass

class GrailFileEntity:
    """Basic entity model, each entity can have many properties + some default fields"""

    TYPE_DEFAULT = 0
    TYPE_PROJECT = 1
    TYPE_LIBRARY = 2
    TYPE_BIBLE   = 3

    def __init__(): pass
    
    # properties

    def get( self, key, type = None ):
        return ""

    def set( self, key, value, type = None ):
        pass

    def has( self, key ):
        return True

    def remove( self, key ):
        pass

    # fields
    @property
    def id( self ):
        return 0

    @property
    def parent( self ):
        return 0

    @property
    def name( self ):
        return ""

    @property
    def type( self ):
        return ""

    @type.setter
    def type( self, type ): 
        pass

    @property
    def created( self ):
        return 0

    @property
    def modified( self ):
        return 0

    @property
    def content( self ):
        return ""

    @content.setter
    def content( self, content ):
        pass

    @property
    def search( self ):
        return ""

    @keywords.setter
    def keywords( self, keywords ):
        pass
