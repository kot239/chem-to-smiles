import numpy as np


def get_length(line):
    return np.sqrt((line[0] - line[2]) ** 2 + (line[1] - line[3]) ** 2)


def close_dotes(fst, snd, threshold=25):
    return (fst[0] - snd[0]) ** 2 + (fst[1] - snd[1]) ** 2 <= threshold


def calculate_theta(line):
    if line[2] == line[0]:
        return np.pi / 2
    return np.arctan((line[3] - line[1]) / (line[2] - line[0]))


def glue_lines(start1, end1, start2, end2):
    lines = [[start1[0], start1[1], end1[0], end1[1]],
             [start2[0], start2[1], end2[0], end2[1]],
             [start1[0], start1[1], start2[0], start2[1]],
             [start1[0], start1[1], end2[0], end2[1]],
             [end1[0], end1[1], start2[0], start2[1]],
             [end1[0], end1[1], end2[0], end2[1]]]
    lengths = list(map(get_length, lines))
    lengths = np.array(lengths)
    j = np.argmax(lengths)
    return lines[j]


class GlueLines:
    def __init__(self, lines, threshold=25, angle_threshold=0.1):
        self._lines = lines
        self._glued_lines = None
        self._threshold = threshold
        self._angle_threshold = angle_threshold

    def filter_lines(self):
        to_del = set()
        for i in range(len(self._lines)):
            for j in range(i + 1, len(self._lines)):
                start_i = (self._lines[i][0], self._lines[i][1])
                end_i = (self._lines[i][2], self._lines[i][3])
                start_j = (self._lines[j][0], self._lines[j][1])
                end_j = (self._lines[j][2], self._lines[j][3])
                if close_dotes(start_i, start_j, self._threshold) and close_dotes(end_i, end_j, self._threshold):
                    to_del.add(j)
        self._lines = np.array([self._lines[i] for i in range(len(self._lines)) if i not in to_del])

    def join_lines(self, pair_lines):
        thetas = list(map(calculate_theta, pair_lines))
        if abs(thetas[0] - thetas[1]) > self._angle_threshold:
            return pair_lines
        starts = [[line[0], line[1]] for line in pair_lines]
        ends = [[line[2], line[3]] for line in pair_lines]
        for i in range(0, 21):
            med = [(starts[0][0] * i + ends[0][0] * (20 - i)) / 20, (starts[0][1] * i + ends[0][1] * (20 - i)) / 20]
            if close_dotes(med, starts[1], self._threshold) or close_dotes(med, ends[1], self._threshold):
                return [np.array(glue_lines(starts[0], ends[0], starts[1], ends[1])), None]
        return pair_lines

    def check_if_ready(self):
        for line in self._glued_lines:
            if not line[1]:
                return False
        return True

    def continue_lines(self):
        self._glued_lines = [[line, False] for line in self._lines]
        while not self.check_if_ready():
            while self._glued_lines[0][1]:
                tmp = self._glued_lines.pop(0)
                self._glued_lines.append(tmp)
            fst = self._glued_lines.pop(0)
            for _ in range(len(self._glued_lines)):
                snd = self._glued_lines.pop(0)
                if snd[1]:
                    self._glued_lines.append(snd)
                    continue
                fst[0], new_snd = self.join_lines([fst[0], snd[0]])
                if new_snd is not None:
                    self._glued_lines.append([new_snd, snd[1]])
            fst[1] = True
            self._glued_lines.append(fst)
        return np.array([line[0] for line in self._glued_lines])

    def get_glued_lines(self):
        self.filter_lines()
        return self.continue_lines()
