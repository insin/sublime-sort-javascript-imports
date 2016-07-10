#!/usr/bin/env python3

if __name__ == '__main__':
    import unittest

    from sort_js_imports import sort_js_imports

    class TestSortJsImports(unittest.TestCase):
        def test_import_formats(self):
            """
            ``import 'foo'``, ``import bar from 'foo'`` and ``require('foo')``
            are supported.
            """
            input_lines = [
                'import "c"',
                'let b = require("b")',
                'import a from "a"',
            ]
            expected_output_lines = [
                'import a from "a"',
                'let b = require("b")',
                'import "c"',
            ]
            self.assertEqual(sort_js_imports(input_lines), expected_output_lines)

        def test_import_case(self):
            """
            Import sorting should be case-insensitve.
            """
            input_lines = [
                "import Route from 'react-router/lib/Route'",
                "import Router from 'react-router/lib/Router'",
                "import IndexRoute from 'react-router/lib/IndexRoute'",
                "import hashHistory from 'react-router/lib/hashHistory'",
            ]
            expected_output_lines = [
                "import hashHistory from 'react-router/lib/hashHistory'",
                "import IndexRoute from 'react-router/lib/IndexRoute'",
                "import Route from 'react-router/lib/Route'",
                "import Router from 'react-router/lib/Router'",
            ]
            self.assertEqual(sort_js_imports(input_lines), expected_output_lines)

        def test_sort_weightings(self):
            """
            Where top-level, parent and local imports are mixed together in the
            same block, top-level import sorts to the top, then parent imports
            from furthest to closest, then local imports from closest to
            furthest.
            """
            input_lines = [
                'import "./local"',
                'import "../oneup"',
                'import "../../twoup"',
                'import "toplevel"',
            ]
            expected_output_lines = [
                'import "toplevel"',
                'import "../../twoup"',
                'import "../oneup"',
                'import "./local"',
            ]
            self.assertEqual(sort_js_imports(input_lines), expected_output_lines)

        def test_import_groups(self):
            """
            Imports separated by blank lines are sorted within the groups they
            delineate.
            """
            input_lines = [
                'import a from "toplevel-b"',
                'import z from "toplevel-a"',
                '',
                'import "../../b"',
                'import "../../a"',
                'import "../b"',
                'import "../a"',
                '',
                'import "./b"',
                'import "./a"',
            ]
            expected_output_lines = [
                'import z from "toplevel-a"',
                'import a from "toplevel-b"',
                '',
                'import "../../a"',
                'import "../../b"',
                'import "../a"',
                'import "../b"',
                '',
                'import "./a"',
                'import "./b"',
            ]
            self.assertEqual(sort_js_imports(input_lines), expected_output_lines)

        def test_non_imports(self):
            """
            Non-imports mixed in with imports are moved to a separate block
            below the selection.
            """
            input_lines = [
                'import express from "express"',
                'let app = express()',
                'import bodyparser from "bodyparser"',
                '',
                'import utils from "./utils"',
                'import {secured, unsecured} from "./api"',
            ]
            expected_output_lines = [
                'import bodyparser from "bodyparser"',
                'import express from "express"',
                '',
                'import {secured, unsecured} from "./api"',
                'import utils from "./utils"',
                '',
                'let app = express()',
            ]
            self.assertEqual(sort_js_imports(input_lines), expected_output_lines)

    unittest.main(argv=['TestSortJsImports'])
