import os.path
import unittest
import sys

sys.path.insert(0, ".")
from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)
from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)
from coalib.bearlib.languages.documentation.DocumentationExtraction import (
    extract_documentation,
    extract_documentation_with_docstyle)
from coalib.misc.Compatability import FileNotFoundError
from coalib.results.TextRange import TextRange


# TODO Insert alternate-style (for doxygen) comments between normal ones to
#      assert for order. (Python, cpp)

class DocumentationExtractionTest(unittest.TestCase):
    def test_extract_documentation_with_docstyle_invalid_input(self):
        with self.assertRaises(ValueError):
            extract_documentation_with_docstyle(
                "",
                DocstyleDefinition("C",
                                   "default",
                                   [["A", "B", "C", "D"]]))

        with self.assertRaises(ValueError):
            extract_documentation_with_docstyle(
                "",
                DocstyleDefinition("C",
                                   "default",
                                   [["A", "B"]]))

        with self.assertRaises(ValueError):
            extract_documentation_with_docstyle(
                "",
                DocstyleDefinition("C",
                                   "default",
                                   [["A"]]))

    def test_extract_documentation_invalid_input(self):
        with self.assertRaises(FileNotFoundError):
            tuple(extract_documentation("", "PYTHON", "INVALID"))

    @staticmethod
    def load_testdata(language):
        filename = (os.path.dirname(os.path.realpath(__file__)) +
                    "/documentation_extraction_testdata/data" + language)
        with open(filename, "r") as fl:
            data = fl.read()

        return data

    def test_extract_documentation_C(self):
        data = DocumentationExtractionTest.load_testdata(".c")

        # No built-in documentation for C.
        with self.assertRaises(KeyError):
            tuple(extract_documentation(data, "C", "default"))

        docstyle_C_doxygen = DocstyleDefinition.load("C", "doxygen")

        self.assertEqual(tuple(extract_documentation(data, "C", "doxygen")),
                         (DocumentationComment(
                              ("\n"
                               " This is the main function.\n"
                               "\n"
                               " @returns Your favorite number.\n"),
                              docstyle_C_doxygen,
                              docstyle_C_doxygen.markers[0],
                              TextRange.from_values(3, 1, 7, 4)),
                          DocumentationComment(
                              (" foobar = barfoo.\n"
                               " @param x whatever...\n"),
                              docstyle_C_doxygen,
                              docstyle_C_doxygen.markers[0],
                              TextRange.from_values(15, 1, 17, 4))))

    def test_extract_documentation_CPP(self):
        data = DocumentationExtractionTest.load_testdata(".cpp")

        # No built-in documentation for C++.
        with self.assertRaises(KeyError):
            tuple(extract_documentation(data, "CPP", "default"))

        docstyle_CPP_doxygen = DocstyleDefinition.load("CPP", "doxygen")

        self.assertEqual(tuple(extract_documentation(data, "CPP", "doxygen")),
                         (DocumentationComment(
                              ("\n"
                               " This is the main function.\n"
                               " @returns Exit code.\n"
                               "          Or any other number.\n"),
                              docstyle_CPP_doxygen,
                              docstyle_CPP_doxygen.markers[0],
                              TextRange.from_values(4, 1, 8, 4)),
                          DocumentationComment(
                              (" foobar\n"
                               " @param xyz\n"),
                              docstyle_CPP_doxygen,
                              docstyle_CPP_doxygen.markers[0],
                              TextRange.from_values(15, 1, 17, 4)),
                          DocumentationComment(
                              " Some alternate style of documentation\n",
                              docstyle_CPP_doxygen,
                              docstyle_CPP_doxygen.markers[2],
                              TextRange.from_values(22, 1, 22, 42)),
                          DocumentationComment(
                              (" Should work\n"
                               "\n"
                               " even without a function standing below.\n"
                               "\n"
                               " @param foo WHAT PARAM PLEASE!?\n"),
                              docstyle_CPP_doxygen,
                              docstyle_CPP_doxygen.markers[2],
                              TextRange.from_values(26, 1, 30, 36))))

    @unittest.skip("INFINITE LOOP")
    def test_extract_documentation_PYTHON3(self):
        data = DocumentationExtractionTest.load_testdata(".py")

        PYTHON3_marker1 = ('"""', '', '"""')
        PYTHON3_marker2 = ('##', '#', '#')
        docstyle_PYTHON3_default = DocstyleDefinition(
            "PYTHON3",
            "default",
            (PYTHON3_marker1,))

        docstyle_PYTHON3_doxygen = DocstyleDefinition(
            "PYTHON3",
            "doxygen",
            (PYTHON3_marker1, PYTHON3_marker2))

        expected = (DocumentationComment(
                        ("\n"
                         "Module description.\n"
                         "\n"
                         "Some more foobar-like text.\n"),
                        docstyle_PYTHON3_default,
                        PYTHON3_marker1,
                        (0, 56)),
                    DocumentationComment(
                        ("\n"
                         "A nice and neat way of documenting code.\n"
                         ":param radius: The explosion radius.\n"),
                        docstyle_PYTHON3_default,
                        PYTHON3_marker1,
                        (92, 189)),
                    DocumentationComment(
                        ("\n"
                         "Docstring with layouted text.\n"
                         "\n"
                         "layouts inside docs are not preserved for these "
                         "documentation styles.\n"
                         "this is intended.\n"),
                        docstyle_PYTHON3_default,
                        PYTHON3_marker1,
                        (200, 330)),
                    DocumentationComment(
                        (" Docstring directly besides triple quotes.\n"
                         "Continues here. "),
                        docstyle_PYTHON3_default,
                        PYTHON3_marker1,
                        (332, 401)))

        self.assertEqual(
            tuple(extract_documentation(data, "PYTHON3", "default")),
            expected)

        # Change only the docstyle in expected results.
        expected = tuple(DocumentationComment(r.documentation,
                                              docstyle_PYTHON3_doxygen_simple,
                                              r.range)
                         for r in expected)
        expected += (DocumentationComment(
                         (" Alternate documentation style in doxygen.\n"
                          "  Subtext\n"
                          " More subtext (not correctly aligned)\n"
                          "      sub-sub-text\n"
                          "\n"),
                      docstyle_PYTHON3_doxygen,
                      PYTHON3_marker2,
                      (404, 521)),)

        self.assertEqual(
            tuple(extract_documentation(data, "PYTHON3", "doxygen")),
            expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
