import unittest
import numpy as np
from src.glue_lines import GlueLines


class SimpleCases(unittest.TestCase):
    def test_two_close_parallel_lines(self):
        input_lines = np.array([[122, 124, 278, 395],
                                [123, 123, 278, 395]])
        ans_lines = np.array([[122, 124, 278, 395]])
        gl = GlueLines(input_lines)
        self.assertTrue((gl.get_glued_lines() == ans_lines).all())

    def test_two_far_lines(self):
        input_lines = np.array([[122, 124, 278, 395],
                                [245, 255, 401, 526]])
        ans_lines = input_lines.copy()
        gl = GlueLines(input_lines)
        self.assertTrue((gl.get_glued_lines() == ans_lines).all())

    def test_two_close_continuing_lines(self):
        input_lines = np.array([[22, 22, 103, 104],
                                [104, 103, 145, 145]])
        ans_lines = np.array([[22, 22, 145, 145]])
        gl = GlueLines(input_lines)
        self.assertTrue((gl.get_glued_lines() == ans_lines).all())

    def test_two_continuing_crossing_lines(self):
        input_lines = np.array([[22, 22, 111, 111],
                                [100, 100, 145, 145]])
        ans_lines = np.array([[22, 22, 145, 145]])
        gl = GlueLines(input_lines)
        self.assertTrue((gl.get_glued_lines() == ans_lines).all())


if __name__ == '__main__':
    unittest.main()
