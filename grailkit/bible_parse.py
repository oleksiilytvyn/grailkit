# -*- coding: UTF-8 -*-

import os
import xml.etree.ElementTree as etree

from grailkit.dna import DNA
from grailkit.bible import BibleError


class Parser(DNA):
    """Parse other file formats into grail bible format. Not implemented"""

    def __init__(self, file_in, file_out):
        self._db_create_query += """
            DROP TABLE IF EXISTS books;
            CREATE TABLE books(id INTEGER PRIMARY KEY AUTOINCREMENT, osisid TEXT, name TEXT, title TEXT, abbr TEXT );

            DROP TABLE IF EXISTS verses;
            CREATE TABLE verses( osisid TEXT, book INT, chapter INT, verse INT, text TEXT );
            """

        super(Parser, self).__init__(file_out, create=False)

        if not os.path.isfile(file_in):
            raise BibleError("Could not open file. File %s not found." % (file_in,))

        # read input file and write to output file
        self.parse_file(file_in)

    def set_property(self, key, value):
        """Set bible property"""

        self._set_property(0, key, value, force_type=str)

    def get_property(self, key, default=""):
        """Get bible property

        Args:
            key (str): property name
            default: default value if property not exists

        Returns:
            bible property
        """

        return self._get_property(0, key, default=default)

    def write_verse(self, osis_id, book_id, chapter, verse, text):
        self._db.execute("INSERT INTO verses VALUES(?, ?, ?, ?, ?)",
                         (osis_id, book_id, chapter, verse, text))

    def write_book(self, book_id, osis_id, name, title, abbr):
        self._db.execute("INSERT INTO books VALUES(?, ?, ?, ?, ?)",
                         (book_id, osis_id, name, title, abbr))

    def parse_file(self, file_in):
        """
        Args:
            file_in (str): path to file that will be parsed
        """
        raise NotImplementedError()


class OSISParser(Parser):
    """Parse OSIS bible. Not implemented"""

    _osis_book_names = {"Gen": ["Genesis", ["Gen", "Ge", "Gn"]],
                        "Exod": ["Exodus", ["Exo", "Ex", "Exod"]],
                        "Lev": ["Leviticus", ["Lev", "Le", "Lv"]],
                        "Num": ["Numbers", ["Num", "Nu", "Nm", "Nb"]],
                        "Deut": ["Deuteronomy", ["Deut", "Dt"]],
                        "Josh": ["Joshua", ["Josh", "Jos", "Jsh"]],
                        "Judg": ["Judges", ["Judg", "Jdg", "Jg", "Jdgs"]],
                        "Ruth": ["Ruth", ["Rth", "Ru"]],
                        "1Sam": ["1 Samuel",
                                 ["1 Sam", "1 Sa", "1Samuel", "1S", "I Sa", "1 Sm", "1Sa", "I Sam", "1Sam", "I Samuel",
                                  "1st Samuel", "First Samuel"]],
                        "2Sam": ["2 Samuel",
                                 ["2 Sam", "2 Sa", "2S", "II Sa", "2 Sm", "2Sa", "II Sam", "2Sam", "II Samuel",
                                  "2Samuel", "2nd Samuel", "Second Samuel"]],
                        "1Kgs": ["1 Kings",
                                 ["1 Kgs", "1 Ki", "1K", "I Kgs", "1Kgs", "I Ki", "1Ki", "I Kings", "1Kings", "1st Kgs",
                                  "1st Kings", "First Kings", "First Kgs", "1Kin"]],
                        "2Kgs": ["2 Kings",
                                 ["2 Kgs", "2 Ki", "2K", "II Kgs", "2Kgs", "II Ki", "2Ki", "II Kings", "2Kings",
                                  "2nd Kgs", "2nd Kings", "Second Kings", "Second Kgs", "2Kin"]],
                        "1Chr": ["1 Chronicles",
                                 ["1 Chron", "1 Ch", "I Ch", "1Ch", "1 Chr", "I Chr", "1Chr", "I Chron", "1Chron",
                                  "I Chronicles", "1Chronicles", "1st Chronicles", "First Chronicles"]],
                        "2Chr": ["2 Chronicles",
                                 ["2 Chron", "2 Ch", "II Ch", "2Ch", "II Chr", "2Chr", "II Chron", "2Chron",
                                  "II Chronicles", "2Chronicles", "2nd Chronicles", "Second Chronicles"]],
                        "Ezra": ["Ezra", ["Ezra", "Ezr"]],
                        "Neh": ["Nehemiah", ["Neh", "Ne"]],
                        "Esth": ["Additions to Esther",
                                 ["Add Esth", "Add Es", "Rest of Esther", "The Rest of Esther", "AEs", "AddEsth"]],
                        "Job": ["Job", ["Job", "Job", "Jb"]],
                        "Ps": ["Psalms of Solomon", ["Ps Solomon", "Ps Sol", "Psalms Solomon", "PsSol"]],
                        "Prov": ["Proverbs", ["Prov", "Pr", "Prv"]],
                        "Eccl": ["Sirach", ["Sirach", "Sir", "Ecclesiasticus", "Ecclus"]],
                        "Song": ["Song of Three Youths",
                                 ["Song of Three", "Song Thr", "The Song of Three Youths", "Pr Az", "Prayer of Azariah",
                                  "Azariah", "The Song of the Three Holy Children", "The Song of Three Jews",
                                  "Song of the Three Holy Children", "Song of Thr", "Song of Three Children",
                                  "Song of Three Jews"]],
                        "Isa": ["Isaiah", ["Isa", "Is"]],
                        "Jer": ["Letter of Jeremiah", ["Let Jer", "Let Jer", "LJe", "Ltr Jer"]],
                        "Lam": ["Lamentations", ["Lam", "La"]],
                        "Ezek": ["Ezekiel", ["Ezek", "Eze", "Ezk"]],
                        "Dan": ["Daniel", ["Dan", "Da", "Dn"]],
                        "Hos": ["Hosea", ["Hos", "Ho"]],
                        "Joel": ["Joel", ["Joel", "Joe", "Jl"]],
                        "Amos": ["Amos", ["Amos", "Am"]],
                        "Obad": ["Obadiah", ["Obad", "Ob"]],
                        "Jonah": ["Jonah", ["Jnh", "Jon"]],
                        "Nah": ["Nahum", ["Nah", "Na"]],
                        "Mic": ["Micah", ["Micah", "Mic"]],
                        "Hab": ["Habakkuk", ["Hab", "Hab"]],
                        "Zeph": ["Zephaniah", ["Zeph", "Zep", "Zp"]],
                        "Eph": ["Ephesians", ["Ephes", "Eph"]],
                        "Hag": ["Haggai", ["Haggai", "Hag", "Hg"]],
                        "Zech": ["Zechariah", ["Zech", "Zec", "Zc"]],
                        "Mal": ["Malachi", ["Mal", "Mal", "Ml"]],
                        "Matt": ["Matthew", ["Matt", "Mt"]],
                        "Mark": ["Mark", ["Mrk", "Mk", "Mr"]],
                        "Luke": ["Luke", ["Luk", "Lk"]],
                        "John": ["3 John",
                                 ["3 John", "3 Jn", "III Jn", "3Jn", "III Jo", "3Jo", "III Joh", "3Joh", "III Jhn",
                                  "3 Jhn", "3Jhn", "III John", "3John", "3rd John", "Third John"]],
                        "Acts": ["Acts", ["Acts", "Ac"]],
                        "Rom": ["Romans", ["Rom", "Ro", "Rm"]],
                        "1Cor": ["1 Corinthians",
                                 ["1 Cor", "1 Co", "I Co", "1Co", "I Cor", "1Cor", "I Corinthians", "1Corinthians",
                                  "1st Corinthians", "First Corinthians"]],
                        "2Cor": ["2 Corinthians",
                                 ["2 Cor", "2 Co", "II Co", "2Co", "II Cor", "2Cor", "II Corinthians", "2Corinthians",
                                  "2nd Corinthians", "Second Corinthians"]],
                        "Gal": ["Galatians", ["Gal", "Ga"]],
                        "Phil": ["Philemon", ["Philem", "Phm", "Phlm"]],
                        "Col": ["Colossians", ["Col", "Col"]],
                        "1Thess": ["1 Thessalonians",
                                   ["1 Thess", "1 Th", "I Th", "1Th", "I Thes", "1Thes", "I Thess", "1Thess",
                                    "I Thessalonians", "1Thessalonians", "1st Thessalonians", "First Thessalonians"]],
                        "2Thess": ["2 Thessalonians",
                                   ["2 Thess", "2 Th", "II Th", "2Th", "II Thes", "2Thes", "II Thess", "2Thess",
                                    "II Thessalonians", "2Thessalonians", "2nd Thessalonians", "Second Thessalonians"]],
                        "1Tim": ["1 Timothy", ["1 Tim", "1 Ti", "I Ti", "1Ti", "I Tim", "1Tim", "I Timothy", "1Timothy",
                                               "1st Timothy", "First Timothy"]],
                        "2Tim": ["2 Timothy",
                                 ["2 Tim", "2 Ti", "II Ti", "2Ti", "II Tim", "2Tim", "II Timothy", "2Timothy",
                                  "2nd Timothy", "Second Timothy"]],
                        "Titus": ["Titus", ["Titus", "Tit"]],
                        "Phlm": ["Philemon", ["Philem", "Phm", "Phlm"]],
                        "Heb": ["Hebrews", ["Hebrews", "Heb"]],
                        "Jas": ["James", ["James", "Jas", "Jm"]],
                        "1Pet": ["1 Peter",
                                 ["1 Pet", "1 Pe", "I Pe", "1Pe", "I Pet", "1Pet", "I Pt", "1 Pt", "1Pt", "I Peter",
                                  "1Peter", "1st Peter", "First Peter"]],
                        "2Pet": ["2 Peter",
                                 ["2 Pet", "2 Pe", "II Pe", "2Pe", "II Pet", "2Pet", "II Pt", "2 Pt", "2Pt", "II Peter",
                                  "2Peter", "2nd Peter", "Second Peter"]],
                        "1John": ["1 John",
                                  ["1 John", "1 Jn", "I Jn", "1Jn", "I Jo", "1Jo", "I Joh", "1Joh", "I Jhn", "1 Jhn",
                                   "1Jhn", "I John", "1John", "1st John", "First John"]],
                        "2John": ["2 John",
                                  ["2 John", "2 Jn", "II Jn", "2Jn", "II Jo", "2Jo", "II Joh", "2Joh", "II Jhn",
                                   "2 Jhn", "2Jhn", "II John", "2John", "2nd John", "Second John"]],
                        "3John": ["3 John",
                                  ["3 John", "3 Jn", "III Jn", "3Jn", "III Jo", "3Jo", "III Joh", "3Joh", "III Jhn",
                                   "3 Jhn", "3Jhn", "III John", "3John", "3rd John", "Third John"]],
                        "Jude": ["Jude", ["Jude", "Jud"]],
                        "Rev": ["Revelation", ["Rev", "Re", "The Revelation"]]
                        }

    def __init__(self, file_in, file_out):
        """
        Args:
            file_in:
            file_out:

        Returns:

        """
        super(OSISParser, self).__init__(file_in, file_out)

    def _get_book_info(self, osis_id):

        if osis_id in self._osis_book_names:
            book = self._osis_book_names[osis_id]

            return [book[0], book[0], book[1]]

        return [osis_id, osis_id, osis_id]

    def parse_file(self, file_in):

        tree = etree.parse(file_in)
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

        self.set_property('version', 1)

    def _parse_header(self, node):

        for headnode in node:
            if headnode.tag.split('}')[-1] == 'work':
                self._parse_header_property(headnode)

    def _parse_header_property(self, node):
        """
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

            # chick if this property is valid
            if name in ids:
                key = ids[name] if ids[name] != "" else name
                value = prop.text if prop.text else ""

                self.set_property(key, value)


class SwordParser(Parser):
    """Parse Sword bible. Not implemented"""

    # TO-DO: implement this class
    def __init__(self, file_in, file_out):
        super(SwordParser, self).__init__(file_in, file_out)


class CSVParser(Parser):
    """Parse CSV bible. Not implemented"""

    # TO-DO: implement this class
    def __init__(self, file_in, file_out):
        super(CSVParser, self).__init__(file_in, file_out)
