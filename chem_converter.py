import sys
from src.main import convert

if __name__ == '__main__':
    args = sys.argv
    img_path = args[1]
    print(convert(img_path))
