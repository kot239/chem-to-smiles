# chem-converter

## Description

One of a huge problem in science comunity is extracting information from science articles. This project is going to extract structures of molecules and convert them to SMILES formed molecules. This is very useful to scientists who are going to use molecules in SMILES format

## Required libraries

* __tesseract__: install it with pip ```pip install pytesseract```

* __NetworkX__: install it with pip ```pip install networkx```

## How to use

Write this command:

`python3 chem_converter.py imagepath`

where `imagepath` is path where is located

## How it works

Pictures of each step you can find after program has worked.
Also you can find examples of these images in `examples`.

There are some steps that do program:

1. Detect lines on the image
2. Detect letters from the image using CNN
3. Find vertexes of molecular graph
4. Make molecular graph
5. Transform graph into SMILES
