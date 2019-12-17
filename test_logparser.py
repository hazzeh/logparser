import unittest
import logparser
import textwrap
import tempfile
import io, sys

class TestLogparser(unittest.TestCase):
    def test_acceptance_test(self):
        """
        Acceptance test for log printer
        """
        log_input = textwrap.dedent("""\
            2019-4-1 13:32:40 [190] User3 logs in
            2019-4-1 13:33:45 [123] User1 logs in
            2019-4-1 13:33:45 [123] User1 goes to search page
            2019-4-1 13:33:46 [123] User1 types in search text
            2019-4-1 13:33:48 [256] User2 logs in
            2019-4-1 13:33:49 [190] User3 runs some job
            2019-4-1 13:33:50 [123] User1 clicks search button
            2019-4-1 13:33:53 [256] User2 does something
            2019-4-1 13:33:54 [123] ERROR: Some exception occured
            2019-4-1 13:33:56 [256] User2 logs off
            2019-4-1 13:33:57 [190] ERROR: Invalid input
            """)

        expected = textwrap.dedent("""\
            2019-4-1 13:33:45 [123] User1 goes to search page
            2019-4-1 13:33:46 [123] User1 types in search text
            2019-4-1 13:33:50 [123] User1 clicks search button
            2019-4-1 13:33:54 [123] ERROR: Some exception occured
            ----
            2019-4-1 13:32:40 [190] User3 logs in
            2019-4-1 13:33:49 [190] User3 runs some job
            2019-4-1 13:33:57 [190] ERROR: Invalid input
            ----
            """)

        with tempfile.NamedTemporaryFile(mode='w+t') as f:
            f.writelines(log_input)
            f.seek(0)
            output = io.StringIO()
            sys.stdout = output
            logparser.print_errors(f.name)
            sys.stdout = sys.__stdout__
    
        self.assertMultiLineEqual(expected, output.getvalue())

if __name__ == '__main__':
    unittest.main()