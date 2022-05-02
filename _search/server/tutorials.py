#!/bin/env python

# Parse ImageJ tutorials into documents for
# use with their own searchable collection.

import logging, traceback, re, sys
import json
import markdown2
from parseutil import first_sentence
from pathlib import Path
from pprint import pprint


logger = logging.getLogger(__name__)


def is_imagej_tutorials(root):
    # java = Path(root) / 'java'
    notebooks = Path(root) / 'notebooks'
    return notebooks.is_dir()
    # return java.is_dir() and notebooks.is_dir()


def parse_java_source(path):
    logger.debug(f'Parsing Java source file {path}...')

    with open(path) as f:
        lines = f.read()

    # This is dumb -- do we want to do better?
    doc = {}
    doc['content'] = ''.join(lines)
    title = str(path)
    doc['title'] = title[title.find("tutorials/")+len("tutorials/"):]
    doc['icon'] = 'Java_logo.png'
    doc['score'] = 90
    doc['description'] = ''

    return doc


def parse_notebook(path):
    logger.debug(f'Parsing notebook {path}...')

    with open(path) as f:
        data = json.load(f)

    doc = {}
    doc['content'] = ''
    title = str(path)
    doc['title'] = title[title.find("tutorials/")+len("tutorials/"):]
    doc['icon'] = 'Jupyter_logo.png'
    doc['score'] = 90
    doc['description'] = ''
    for cell in data['cells']:
        doc['content'] += process_cell(cell)

    return doc

# type of cell is dict
def process_cell(cell):
    result = ''

    if 'source' in cell:
        s = "".join(cell['source'])
        # markdown to html converter
        if 'cell_type' in cell and cell['cell_type'] == 'markdown':
            s = markdown2.markdown(s)
        result += s
    
    # case 1: code cell
    if 'outputs' in cell:
        for o in cell['outputs']:
            if 'text' in o:
                result += "".join(o['text'])
            if 'data' in o:
                if 'text/html' in o['data']:
                    result += "".join(o['data']['text/html'])
                if 'text/plain' in o['data']:
                    result += f"<pre>{''.join(o['data']['text/plain'])}</pre>"
                
    return result

def load_imagej_tutorials(root):
    """
    Loads the content from the given imagej/tutorials folder.
    See: https://github.com/imagej/tutorials
    """
    java = Path(root) / 'java'
    notebooks = Path(root) / 'notebooks'
    if not java.is_dir() or not notebooks.is_dir():
        raise ValueError(f'The path {root} does not appear to be a Jekyll site.')

    logger.info('Loading content...')
    documents = []

    for javafile in java.rglob("**/*.java"):
        try:
            doc = parse_java_source(javafile)
            if doc:
                nbpath = str(javafile)[len(str(root)):]
                doc['id'] = f'https://github.com/imagej/tutorials/blob/master/{nbpath}' 
                documents.append(doc)
        except:
            logger.error(f'Failed to parse {Path}:')
            traceback.print_exc()
    logger.info(f'Loaded {len(documents)} documents from Java source files')

    for nbfile in notebooks.rglob("**/*.ipynb"):
        try:
            doc = parse_notebook(nbfile)
            if doc:
                nbpath = str(nbfile)[len(str(root)):]
                doc['id'] = f'https://github.com/imagej/tutorials/blob/master/{nbpath}' 
                documents.append(doc)
        except:
            logger.error(f'Failed to parse {Path}:')
            traceback.print_exc()
    logger.info(f'Loaded {len(documents)} documents from Jupyter notebooks')

    return documents

""" def main(args):
    docs = load_imagej_tutorials(args[0])
    for doc in docs: 
        # pprint(doc)
        print(doc['id'])

if __name__ == '__main__':
    main(['/Users/jackrueth/code/imagej/tutorials']) """
