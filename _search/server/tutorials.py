#!/bin/env python

# Parse ImageJ tutorials into documents for
# use with their own searchable collection.

import logging, traceback, re, sys
import json
from parseutil import first_sentence
from pathlib import Path
from pprint import pprint

logger = logging.getLogger(__name__)


def is_imagej_tutorials(root):
    java = Path(root) / 'java'
    notebooks = Path(root) / 'notebooks'
    return java.isdir() and notebooks.isdir()


def parse_java_source(path):
    logger.debug(f'Parsing Java source file {path}...')

    with open(path) as f:
        lines = json.load(f)

    # This is dumb -- do we want to do better?
    doc = {}
    doc['content'] = ''.join(lines)

    return doc


def parse_notebook(path):
    logger.debug(f'Parsing notebook {path}...')

    with open(path) as f:
        data = json.load(f)

    doc = {}
    doc['content'] = ''
    for cell in data['cells']:
        # TODO: implement process_cell: extract source and output(s) if present
        doc['content'] += process_cell(cell)

    return doc

# type of cell is dict
def process_cell(cell):
    result = ''

    if 'source' in cell:
        result += filter_data("".join(cell['source']))
    
    # case 1: code cell
    if 'outputs' in cell:
        for o in cell['outputs']:
            if 'text' in o:
                result += filter_data("".join(o['text']))
            if 'data' in o:
                for k,v in o['data'].items():
                    if k in ('text/html', 'text/plain'):
                        result += filter_data("".join(v))

    return result

# takes input of string; filters html and other data 
def filter_data(data):
    # if len(data) > 5000:
    filtered = re.sub('<[^>]*>', '', data)
    return filtered # this string will have markup with it 
    # TODO: remove markup from data

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
                documents.append(doc)
        except:
            logger.error(f'Failed to parse {Path}:')
            traceback.print_exc()
    logger.info(f'Loaded {len(documents)} documents from Java source files')

    for nbfile in notebooks.rglob("**/*.ipynb"):
        try:
            doc = parse_notebook(nbfile)
            if doc:
                nbpath = str(nbfile)[len(str(root)) + 1:]
                doc['url'] = f'https://github.com/imagej/tutorials/blob/master/{nbpath}' 
                documents.append(doc)
        except:
            logger.error(f'Failed to parse {Path}:')
            traceback.print_exc()
    logger.info(f'Loaded {len(documents)} documents from Jupyter notebooks')

    return documents

def main(args):
    docs = load_imagej_tutorials(args[0])
    for doc in docs: 
        # pprint(doc)
        print(doc['url'])

if __name__ == '__main__':
    main(['/Users/jackrueth/code/imagej/tutorials'])
