import unittest
import logparser
import textwrap
import tempfile
import io, sys

class TestLogparser(unittest.TestCase):
    def test_acceptance_test(self):
        """
        Acceptance test for log printer.
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

        self.assertLog(log_input, expected)

    def test_handle_error_in_non_error_message(self):
        """
        Output should not be printed if message does not start with 'ERROR:'.
        """
        log_input = textwrap.dedent("""\
            2019-4-1 13:32:40 [190] Some ERROR: occured
            """)

        expected = ""

        self.assertLog(log_input, expected)

    def test_same_pids(self):
        """
        Same pid with multiple errors should produce multiple printouts
        if they pid are after error line.
        """
        log_input = textwrap.dedent("""\
            2019-4-1 13:33:45 [100] User1 logs in
            2019-4-1 13:33:55 [100] User1 goes to search page
            2019-4-1 13:33:56 [100] ERROR: Some exception occured
            2019-4-2 13:33:45 [100] User2 logs in
            2019-4-2 13:33:55 [100] User2 goes to search page
            2019-4-2 13:33:56 [100] ERROR: Some other exception occured
            """)

        expected = textwrap.dedent("""\
            2019-4-1 13:33:45 [100] User1 logs in
            2019-4-1 13:33:55 [100] User1 goes to search page
            2019-4-1 13:33:56 [100] ERROR: Some exception occured
            ----
            2019-4-2 13:33:45 [100] User2 logs in
            2019-4-2 13:33:55 [100] User2 goes to search page
            2019-4-2 13:33:56 [100] ERROR: Some other exception occured
            ----
            """)

        self.assertLog(log_input, expected)

    def test_max_4_lines(self):
        """
        Only the last 4 lines should be included in the printout.
        """
        log_input = textwrap.dedent("""\
            2019-4-1 13:33:45 [100] Error line 1
            2019-4-1 13:33:45 [200] Nonerror
            2019-4-1 13:33:55 [100] Error line 2
            2019-4-2 13:33:55 [200] Nonerror
            2019-4-1 13:33:55 [100] Error line 3
            2019-4-1 13:33:55 [100] Error line 4
            2019-4-1 13:33:55 [100] Error line 5
            2019-4-2 13:33:56 [100] ERROR: Some other exception occured
            """)

        expected = textwrap.dedent("""\
            2019-4-1 13:33:55 [100] Error line 3
            2019-4-1 13:33:55 [100] Error line 4
            2019-4-1 13:33:55 [100] Error line 5
            2019-4-2 13:33:56 [100] ERROR: Some other exception occured
            ----
            """)

        self.assertLog(log_input, expected)

    def test_ignore_garbage(self):
        """
        Output should not be printed if log line does not match regex.
        """
        log_input = textwrap.dedent("""\
            2019-4-1 13:32:40 No pid
            """)

        expected = ""

        self.assertLog(log_input, expected)

    def assertLog(self, input_text, expected_text):
        with tempfile.NamedTemporaryFile(mode='w+t') as f:
            f.writelines(input_text)
            f.seek(0)
            output = io.StringIO()
            sys.stdout = output
            logparser.print_errors(f.name)
            sys.stdout = sys.__stdout__
        self.assertMultiLineEqual(expected_text, output.getvalue())


if __name__ == '__main__':
    unittest.main()