#!/bin/env python

import logging, os, sys
from pathlib import Path
import jekyll, ijsite, tsutil
import tutorials


logger = logging.getLogger('indexer')

def index_documents(collection, documents):
    client = tsutil.connect()
    if client is None:
        logger.info('No typesense credentials available.')
        return
    logger.info('Connected to typesense.')
    created = tsutil.create(client, collection, documents, force=True)
    logger.info('Created new collection.' if created else 'Updating existing collection.')
    logger.info(f'Indexing {len(documents)} documents...')
    tsutil.update_index(client, collection, documents)
    logger.info('Done!')


def main(args):
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    logging.root.setLevel(logging.INFO)


    p = Path(sys.argv[0]).parent
    root_imagej_wiki = p / '..' / '..'
    root_imagej_tutorials = p / 'sites' / 'tutorials' #TODO: shell script to clone git repo if missing
    root_imagej_website = '/var/www/mirror.imagej.net'
    sites = [
        ('imagej-wiki', root_imagej_wiki, jekyll.is_jekyll_site, jekyll.load_jekyll_site),
        ('imagej-website', root_imagej_website, ijsite.is_imagej_website, ijsite.load_site), 
        ('imagej-tutorials', root_imagej_tutorials, tutorials.is_imagej_tutorials, tutorials.load_imagej_tutorials)
    ]

    for collection, root, isvalid, loadsite in sites:
        if isvalid(root):
            documents = loadsite(root)
            index_documents(collection, documents)
        else:
            logger.warning(f"Skipping invalid site {root}")
    

    # wiki, tutorials, source code(source + javadoc to actions), 
    # imagej-website, support channels(mailing lists + forums + chat rooms + issues), and maven artifacts

if __name__ == '__main__':
    main(sys.argv)
