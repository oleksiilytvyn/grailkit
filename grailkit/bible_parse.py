# -*- coding: UTF-8 -*-
"""
    grailkit.bible_parse
    ~~~~~~~~~~~~~~~~~~~~

    Parse other bible formats into grail bible format.
"""
import os
import xml.etree as etree

from grailkit.dna import DNA
from grailkit.bible import BibleError


class Parser(DNA):
    """Basic implementation of parser"""

    def __init__(self, file_in, file_out):
        """Parse `file_in` into grail file `file_out`

        Args:
            file_in (str): path to input file
            file_out (str): path to output file
        """

        self._db_create_query += """
            DROP TABLE IF EXISTS books;
            CREATE TABLE books(id INTEGER PRIMARY KEY AUTOINCREMENT, osisid TEXT, name TEXT, title TEXT, abbr TEXT );

            DROP TABLE IF EXISTS verses;
            CREATE TABLE verses( osisid TEXT, book INT, chapter INT, verse INT, text TEXT );
            """

        super(Parser, self).__init__(file_out, create=True)

        if not os.path.isfile(file_in):
            raise BibleError("Could not open file. File %s not found." % (file_in,))

        # read input file and write to output file
        self.parse_file(file_in)

    def set_property(self, key, value):
        """Set bible property

        Args:
            key (str): property key
            value (str): property value
        """

        self._set(0, key, value, force_type=str)

    def get_property(self, key, default=""):
        """Get bible property

        Args:
            key (str): property name
            default (str): default value if property not exists

        Returns:
            bible property
        """

        return self._get(0, key, default=default)

    def write_verse(self, osis_id, book_id, chapter, verse, text):
        """Add verse to file

        Args:
            osis_id (str): OSIS identifier
            book_id (int): book number
            chapter (int): chapter number
            verse (int): verse number
            text (str): text of verse
        """

        self._db.execute("INSERT INTO verses VALUES(?, ?, ?, ?, ?)",
                         (osis_id, book_id, chapter, verse, text))

    def write_book(self, book_id, osis_id, name, title, abbr):
        """Add book to file

        Args:
            book_id (int): book number
            osis_id (str): OSIS identifier
            name (str): short book name
            title (str): full name of book
            abbr (str): string with abbreviations of book name separated by comma
        """
        self._db.execute("INSERT INTO books VALUES(?, ?, ?, ?, ?)",
                         (book_id, osis_id, name, title, abbr))

    def parse_file(self, file_in):
        """Abstract method. Implement this method in sub class.

        Args:
            file_in (str): path to file that will be parsed
        """
        raise NotImplementedError()


class Names(object):
    """This class holds book names and abbreviations
    to simplify parsing of bible formats
    """

    # format: Name, Long name, List of abbreviations
    _books = [
        ["Genesis", "Genesis", ["Gen", "Ge", "Gn"]],
        ["Exodus", "Exodus", ["Exo", "Ex", "Exod"]],
        ["Leviticus", "Leviticus", ["Lev", "Le", "Lv"]],
        ["Numbers", "Numbers", ["Num", "Nu", "Nm", "Nb"]],
        ["Deuteronomy", "Deuteronomy", ["Deut", "Dt"]],
        ["Joshua", "Josh", ["Josh", "Jos", "Jsh"]],
        ["Judges", "Judges", ["Judg", "Jdg", "Jg", "Jdgs"]],
        ["Ruth", "Ruth", ["Rth", "Ru"]],
        ["1 Samuel", "First Samuel",
            ["1 Sam", "1 Sa", "1Samuel", "1S", "I Sa", "1 Sm", "1Sa", "I Sam", "1Sam", "I Samuel",
             "1st Samuel", "First Samuel"]],
        ["2 Samuel", "Second Samuel",
            ["2 Sam", "2 Sa", "2S", "II Sa", "2 Sm", "2Sa", "II Sam", "2Sam", "II Samuel",
             "2Samuel", "2nd Samuel", "Second Samuel"]],
        ["1 Kings", "First Kings",
            ["1 Kgs", "1 Ki", "1K", "I Kgs", "1Kgs", "I Ki", "1Ki", "I Kings", "1Kings", "1st Kgs",
             "1st Kings", "First Kings", "First Kgs", "1Kin"]],
        ["2 Kings", "Second Kings",
            ["2 Kgs", "2 Ki", "2K", "II Kgs", "2Kgs", "II Ki", "2Ki", "II Kings", "2Kings",
             "2nd Kgs", "2nd Kings", "Second Kings", "Second Kgs", "2Kin"]],
        ["1 Chronicles", "First Chronicles",
            ["1 Chron", "1 Ch", "I Ch", "1Ch", "1 Chr", "I Chr", "1Chr", "I Chron", "1Chron",
             "I Chronicles", "1Chronicles", "1st Chronicles", "First Chronicles"]],
        ["2 Chronicles", "Second Chronicles",
            ["2 Chron", "2 Ch", "II Ch", "2Ch", "II Chr", "2Chr", "II Chron", "2Chron",
             "II Chronicles", "2Chronicles", "2nd Chronicles", "Second Chronicles"]],
        ["Ezra", "Ezra", ["Ezra", "Ezr"]],
        ["Nehemiah", "Nehemiah", ["Neh", "Ne"]],
        ["Additions to Esther", "The Rest of Esther",
            ["Add Esth", "Add Es", "Rest of Esther", "The Rest of Esther", "AEs", "AddEsth"]],
        ["Job", "Job", ["Job", "Jb"]],
        ["Psalms of Solomon", "Psalms of Solomon", ["Ps Solomon", "Ps Sol", "Psalms Solomon", "PsSol"]],
        ["Proverbs", "Proverbs", ["Prov", "Pr", "Prv"]],
        ["Sirach", "Sirach", ["Sirach", "Sir", "Ecclesiasticus", "Ecclus"]],
        ["Song of Three", "Song of Three Youths",
            ["Song Thr", "The Song of Three Youths", "Pr Az", "Prayer of Azariah",
             "Azariah", "The Song of the Three Holy Children", "The Song of Three Jews",
             "Song of the Three Holy Children", "Song of Thr", "Song of Three Children",
             "Song of Three Jews"]],
        ["Isaiah", "Isaiah", ["Isa", "Is"]],
        ["Letter of Jeremiah", "Letter of Jeremiah", ["Let Jer", "Let Jer", "LJe", "Ltr Jer"]],
        ["Lamentations", "Lamentations", ["Lam", "La"]],
        ["Ezekiel", "Ezekiel", ["Ezek", "Eze", "Ezk"]],
        ["Daniel", "Daniel", ["Dan", "Da", "Dn"]],
        ["Hosea", "Hosea", ["Hos", "Ho"]],
        ["Joel", "Joel", ["Joel", "Joe", "Jl"]],
        ["Amos", "Amos", ["Amos", "Am"]],
        ["Obadiah", "Obadiah", ["Obad", "Ob"]],
        ["Jonah", "Jonah", ["Jnh", "Jon"]],
        ["Nahum", "Nahum", ["Nah", "Na"]],
        ["Micah", "Micah", ["Micah", "Mic"]],
        ["Habakkuk", "Habakkuk", ["Hab", "Hab"]],
        ["Zephaniah", "Zephaniah", ["Zeph", "Zep", "Zp"]],
        ["Ephesians", "Ephesians", ["Ephes", "Eph"]],
        ["Haggai", "Haggai", ["Haggai", "Hag", "Hg"]],
        ["Zechariah", "Zechariah", ["Zech", "Zec", "Zc"]],
        ["Malachi", "Malachi", ["Mal", "Mal", "Ml"]],
        ["Matthew", "Matthew", ["Matt", "Mt"]],
        ["Mark", "Mark", ["Mrk", "Mk", "Mr"]],
        ["Luke", "Luke", ["Luk", "Lk"]],
        ["3 John", "Third John",
            ["3 John", "3 Jn", "III Jn", "3Jn", "III Jo", "3Jo", "III Joh", "3Joh", "III Jhn",
             "3 Jhn", "3Jhn", "III John", "3John", "3rd John", "Third John"]],
        ["Acts", "Acts", ["Acts", "Ac"]],
        ["Romans", "Romans", ["Rom", "Ro", "Rm"]],
        ["1 Corinthians", "First Corinthians",
            ["1 Cor", "1 Co", "I Co", "1Co", "I Cor", "1Cor", "I Corinthians", "1Corinthians",
             "1st Corinthians", "First Corinthians"]],
        ["2 Corinthians", "Second Corinthians",
            ["2 Cor", "2 Co", "II Co", "2Co", "II Cor", "2Cor", "II Corinthians", "2Corinthians",
             "2nd Corinthians", "Second Corinthians"]],
        ["Galatians", "Galatians", ["Gal", "Ga"]],
        ["Philemon", "Philemon", ["Philem", "Phm", "Phlm"]],
        ["Colossians", "Colossians", ["Col", "Col"]],
        ["1 Thessalonians", "First Thessalonians",
            ["1 Thess", "1 Th", "I Th", "1Th", "I Thes", "1Thes", "I Thess", "1Thess",
             "I Thessalonians", "1Thessalonians", "1st Thessalonians", "First Thessalonians"]],
        ["2 Thessalonians", "Second Thessalonians",
            ["2 Thess", "2 Th", "II Th", "2Th", "II Thes", "2Thes", "II Thess", "2Thess",
             "II Thessalonians", "2Thessalonians", "2nd Thessalonians", "Second Thessalonians"]],
        ["1 Timothy", "First Timothy",
            ["1 Tim", "1 Ti", "I Ti", "1Ti", "I Tim", "1Tim", "I Timothy", "1Timothy", "1st Timothy", "First Timothy"]],
        ["2 Timothy", "Second Timothy",
            ["2 Tim", "2 Ti", "II Ti", "2Ti", "II Tim", "2Tim", "II Timothy", "2Timothy",
             "2nd Timothy", "Second Timothy"]],
        ["Titus", "Titus", ["Titus", "Tit"]],
        ["Philemon", "Philemon", ["Philem", "Phm", "Phlm"]],
        ["Hebrews", "Hebrews", ["Hebrews", "Heb"]],
        ["James", "James", ["James", "Jas", "Jm"]],
        ["1 Peter", "First Peter",
            ["1 Pet", "1 Pe", "I Pe", "1Pe", "I Pet", "1Pet", "I Pt", "1 Pt", "1Pt", "I Peter",
             "1Peter", "1st Peter", "First Peter"]],
        ["2 Peter", "Second Peter",
            ["2 Pet", "2 Pe", "II Pe", "2Pe", "II Pet", "2Pet", "II Pt", "2 Pt", "2Pt", "II Peter",
             "2Peter", "2nd Peter", "Second Peter"]],
        ["1 John", "First John",
            ["1 John", "1 Jn", "I Jn", "1Jn", "I Jo", "1Jo", "I Joh", "1Joh", "I Jhn", "1 Jhn",
             "1Jhn", "I John", "1John", "1st John", "First John"]],
        ["2 John", "Second John",
            ["2 John", "2 Jn", "II Jn", "2Jn", "II Jo", "2Jo", "II Joh", "2Joh", "II Jhn",
             "2 Jhn", "2Jhn", "II John", "2John", "2nd John", "Second John"]],
        ["3 John", "Third John",
            ["3 Jn", "III Jn", "3Jn", "III Jo", "3Jo", "III Joh", "3Joh", "III Jhn",
             "3 Jhn", "3Jhn", "III John", "3John", "3rd John"]],
        ["Jude", "Jude", ["Jude", "Jud"]],
        ["Revelation", "The Revelation", ["Rev", "Re"]]
        ]

    # OSIS book names with reference too book description
    _osis_book_names = {
        "Gen": 0, "Exod": 1, "Lev": 2, "Num": 3, "Deut": 4,
        "Josh": 5, "Judg": 6, "Ruth": 7, "1Sam": 8, "2Sam": 9,
        "1Kgs": 10, "2Kgs": 11, "1Chr": 12, "2Chr": 13, "Ezra": 14,
        "Neh": 15, "Esth": 16, "Job": 17, "Ps": 18, "Prov": 19,
        "Eccl": 20, "Song": 21, "Isa": 22, "Jer": 23, "Lam": 24,
        "Ezek": 25, "Dan": 26, "Hos": 27, "Joel": 28, "Amos": 29,
        "Obad": 30, "Jonah": 31, "Nah": 32, "Mic": 33, "Hab": 34,
        "Zeph": 35, "Eph": 36, "Hag": 37, "Zech": 38, "Mal": 39,
        "Matt": 40, "Mark": 41, "Luke": 42, "John": 43, "Acts": 44,
        "Rom": 45, "1Cor": 46, "2Cor": 47, "Gal": 48, "Phil": 49,
        "Col": 50, "1Thess": 51, "2Thess": 52, "1Tim": 53, "2Tim": 54,
        "Titus": 55, "Phlm": 56, "Heb": 57, "Jas": 58, "1Pet": 59,
        "2Pet": 60, "1John": 61, "2John": 62, "3John": 63, "Jude": 64, "Rev": 65
        }

    @classmethod
    def osis(cls, osis_id):
        """Get book info by OSIS id

        Args:
            osis_id (str): OSIS identifier
        """

        if osis_id in cls._osis_book_names:
            return cls._books[cls._osis_book_names[osis_id]]
        else:
            return None


class OSISParser(Parser):
    """Parse OSIS bible format file."""

    def __init__(self, file_in, file_out):
        """Parse a OSIS file into grail file format bible

        Args:
            file_in (str): input file
            file_out (str): output file
        """

        super(OSISParser, self).__init__(file_in, file_out)

    def _get_book_info(self, osis_id):
        """Get info of book using OSIS identifier

        Args:
            osis_id (str): OSIS identifier
        Returns:
            array that consists of three items
            first item is short name of book
            second item is full name of book
            and third is abbreviations separated by comma
        """

        book = Names.osis(osis_id)

        return [book[0], book[1], ", ".join(book[2])] if book else [osis_id, osis_id, osis_id]

    def parse_file(self, file_in):
        """Parse input file

        Args:
            file_in (str): path to file to be parsed
        """

        tree = etree.ElementTree.parse(file_in)
        root = tree.getroot()

        book = 0

        for book_node in root[0]:
            tag = book_node.tag.split('}')[-1]

            if tag == 'header':
                self._parse_header(book_node)

            if tag == 'div' and book_node.attrib['type'] and book_node.attrib['type'] == 'book':
                book += 1
                book_osisid = book_node.attrib['osisID']
                book_info = self._get_book_info(book_osisid)

                self.write_book(book, book_osisid, book_info[0], book_info[1], book_info[2])

                for chapter_node in book_node:
                    for verse_node in chapter_node:
                        if verse_node.tag.split('}')[-1] == 'verse':
                            osis_id = verse_node.attrib['osisID']
                            verse_id = osis_id.split('.')

                            self.write_verse(osis_id, book, int(verse_id[1]), int(verse_id[2]), verse_node.text)

        self.set_property('version', '1.0')

    def _parse_header(self, node):
        """Parse osis header node

        Args:
            node: header xml node
        """

        for headnode in node:
            if headnode.tag.split('}')[-1] == 'work':
                self._parse_header_property(headnode)

    def _parse_header_property(self, node):
        """Parse header property

        Args:
            node: node of header
        """
        for prop in node:
            name = prop.tag.split('}')[-1]
            ids = {
                'date': '',
                'title': '',
                'subject': '',
                'language': '',
                'publisher': '',
                'rights': 'copyright',
                'identifier': '',
                'description': ''
                }

            # check if this property is valid
            if name in ids:
                key = ids[name] if ids[name] != "" else name
                value = prop.text if prop.text else ""

                self.set_property(key, value)
