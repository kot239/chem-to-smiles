import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import networkx as nx
import copy
from keras.models import load_model
from src.glue_lines import GlueLines
from src.lines_to_graph import LinesToGraph
from src.graph_to_smiles import GraphToSmiles

FOLDER_NAME = '../images'
LOG_PATH = 'log'
GROUPS = ['F', 'Br', 'B', 'O', 'Cl', 'N', 'T', 'S', 'P', 'C', '0']


def create_log_folder():
    is_exist = os.path.exists(LOG_PATH)
    if not is_exist:
        os.makedirs(LOG_PATH)


def is_to_union(rect1, rect2, threshold):
    return (rect2[0][0] <= rect1[1][0] + threshold and
            rect2[0][1] <= rect1[1][1] + threshold and
            rect1[0][1] <= rect2[1][1] + threshold)


def union_rectangles(rectangles, threshold=10):
    rectangles = sorted(rectangles, key=lambda rec: rec[0][0])
    united = [False] * len(rectangles)
    new_rectangles = []
    for i, cur_rect in enumerate(rectangles):
        if not united[i]:
            for j in range(i + 1, len(rectangles)):
                if is_to_union(cur_rect, rectangles[j], threshold):
                    cur_rect = [(cur_rect[0][0],
                                 min(cur_rect[0][1], rectangles[j][0][1])),
                                (max(cur_rect[1][0], rectangles[j][1][0]),
                                 max(cur_rect[1][1], rectangles[j][1][1]))]
                    united[j] = True
            united[i] = True
            new_rectangles.append(cur_rect)
    return new_rectangles


def get_group(rect, col_img, model):
    cur_img = col_img[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]
    width = rect[1][0] - rect[0][0]
    height = rect[1][1] - rect[0][1]
    img_size = max(width, height)
    squared_img = np.zeros(shape=(img_size, img_size, 3))
    w_indent = (img_size - width) // 2
    h_indent = (img_size - height) // 2
    squared_img[h_indent:(h_indent + height), w_indent:(w_indent + width)] = cur_img
    saving_img = cv2.resize(squared_img, (32, 32), interpolation=cv2.INTER_AREA)
    saving_img = saving_img.astype('float32')
    saving_img = cv2.cvtColor(saving_img, cv2.COLOR_BGR2GRAY)
    saving_img /= 255
    saving_img = saving_img.reshape((1, 32, 32, 1))
    ans = model.predict([saving_img])
    it = np.argmax(ans[0])
    return GROUPS[it]


def convert(img_path, threshold_area=40):
    create_log_folder()

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.bitwise_not(img)

    threshed_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    color_img = cv2.cvtColor(threshed_img, cv2.COLOR_GRAY2BGR)

    lines = cv2.HoughLinesP(image=threshed_img,
                            rho=1,
                            theta=(np.pi / 180),
                            threshold=50,
                            lines=None,
                            minLineLength=45,
                            maxLineGap=5
                            )
    lines = [line[0] for line in lines]

    empty_img = np.zeros([512, 512, 1], dtype=np.uint8)
    empty_img.fill(255)
    for i, l in enumerate(lines):
        cv2.line(empty_img, (l[0], l[1]), (l[2], l[3]), (255, 0, 0), 1, cv2.LINE_AA)
    cv2.imwrite('log/lines.png', empty_img)

    color_img2 = copy.copy(color_img)

    gl = GlueLines(lines)
    needed_lines = gl.get_glued_lines()
    for nl in needed_lines:
        cv2.line(color_img, (nl[0], nl[1]), (nl[2], nl[3]), (255, 0, 0), 3, cv2.LINE_AA)

    for nl in needed_lines:
        cv2.line(color_img2, (nl[0], nl[1]), (nl[2], nl[3]), (0, 0, 0), 3, cv2.LINE_AA)
    cv2.imwrite('log/groups.png', color_img2)

    color_img3 = copy.copy(color_img2)
    black_img3 = cv2.cvtColor(color_img3, cv2.COLOR_BGR2GRAY)
    letters, _ = cv2.findContours(black_img3, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    rectangles = []
    for letter in letters:
        (left, top, width, height) = cv2.boundingRect(letter)
        if width * height >= threshold_area:
            tl = (left, top)
            br = (left + width, top + height)
            rectangles.append([tl, br])

    new_rectangles = union_rectangles(rectangles)
    for rect in new_rectangles:
        color_img3 = cv2.rectangle(color_img3, rect[0], rect[1], (0, 0, 255), 2)
    cv2.imwrite('log/detected_groups.png', color_img3)

    model = load_model('bin/letter_to_group')

    groups = []
    for rect in new_rectangles:
        letter = get_group(rect, color_img2, model)
        if letter != 'T':
            groups.append([rect, letter])

    ltg = LinesToGraph(needed_lines, groups)
    graph = ltg.make_graph()
    nodes = ltg.get_nodes()
    for node in nodes:
        color_img = cv2.rectangle(color_img, node[0], node[1], (0, 0, 255), 2)
    cv2.imwrite('log/detected_mol.png', color_img)

    nx.draw(graph, node_color='red', node_size=1000, with_labels=True)
    plt.savefig("log/mol_graph.png")

    gts = GraphToSmiles(graph)
    return gts.get_smiles()
