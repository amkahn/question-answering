#!/opt/python-2.7/bin/python2.7
#
# script can be run without invoking python because of shebang
# will be run with correct version on Patas
#
# Code last updated on 5/26/2014 by Claire Jaja
#
# This script will convert documents from the AQUAINT2 format
# to the AQUAINT format.

import sys
from bs4 import BeautifulSoup
from os import listdir, path, makedirs

def main():
    # argument is folder to put converted corpus
    converted_data = sys.argv[1]
    AQUAINT2 = "/corpora/LDC/LDC08T25/data/"

    # for every folder in AQUAINT2/data
    for folder in listdir(AQUAINT2):
        sys.stderr.write("Folder: "+folder+"\n")
        # create same folder in converted_data folder
        new_folder = path.join(converted_data,folder)
        if not path.exists(new_folder):
            makedirs(new_folder)
        # for every .xml file in that folder
        for file in [ x for x in listdir(path.join(AQUAINT2,folder)) if x.endswith(".xml") ]:
            sys.stderr.write("File: "+file+"\n")
            # create file with same name in newly created folder
            new_file = open(path.join(new_folder,file),'w')
            # parse xml with beautiful soup
            xml = open(path.join(AQUAINT2,folder,file),'r')
            soup = BeautifulSoup(xml)
            # gather doc ID, headline, and text
            docs = soup.find_all("doc")
            doc_ids = []
            headlines = []
            text = []
            for doc in docs:
                doc_ids.append(doc['id'])
                if doc.headline:
                    headlines.append(doc.headline.get_text())
                else:
                    headlines.append("None")
                text.append(doc.text)
            xml.close()
            # print out doc ID, headline, and text to newly created file
            for i in range(len(doc_ids)):
                new_file.write("<DOC>\n")
                new_file.write("<DOCNO> %s </DOCNO>\n" % doc_ids[i])
                new_file.write("<BODY>\n")
                if headlines[i]:
                    new_file.write("<HEADLINE> %s </HEADLINE>\n" % headlines[i].encode('utf8'))
                new_file.write("<TEXT> %s </TEXT>\n" % text[i].encode('utf8'))
                new_file.write("</BODY>\n")
                new_file.write("</DOC>\n")
            new_file.close()


if __name__ == '__main__':
	main()
