################################################################################
# MIT LICENSE
#
# Copyright (c) 2018, Milind Nirgun
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################

__author__ = "Milind Nirgun"
__email__ = "milinds@nirgun.com"
__date__ = "Dec. 2018"
__version__ = "0.1"

import sys, getopt
import csv
import logging
from graphviz import Digraph


# set logging level to DEBUG
logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s: %(levelname)6s: %(lineno)4s: %(funcName)10s: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


# Function to process commandline arguments passed to the program and return the inputfile
# and output file names
# argv **argv   arguments passed to the program
def handlefileargs(argv):

    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('digraph.py -i <inputfile> -o [<outputfile>]')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('usage: python digraph.py -i <inputfile> -o [<outputfile>]')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if not inputfile:
        print('Input file name is required')
        print('usage: python digraph.py -i <inputfile> -o [<outputfile>]')
        sys.exit(1)

    if not outputfile:
        dotindex = inputfile.find(".")
        outputfile = inputfile[:dotindex]
    return inputfile, outputfile


# Reads in the passed filename and returns a list with all the non-empty rows.
# A CSV file without header is expected.
# f - string    name of file to read
def readfile(f):
    with open(f, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        inputlist = []
        headers = next(reader)
        for row in reader:
            if any(row):
                inputlist.append(row)

    return inputlist


# Creates a Digraph with initial configuration and returns it
# comment - string  comment to initialize with
def creategraph(comment):
    dot = Digraph(comment=comment)
    dot.format = 'pdf'
    return dot


# Function to find an existing node in the list of nodes passed. This function is used to prevent adding
# duplicate nodes to the list if it already exists. Returns true or false depending on outcome.
# node - string     node to be looked up in the list
# alist - list      list to search for node
def dupnodes(node, alist):
    found = False

    logger.debug("Node - %s", node)
    # if node value passed in is empty, exit with false. This enables adding new nodes in main()
    if not node:
        return found

    for i in alist:
        logger.debug("list item - %s, node - %s", i, node)
        if node == i:
            found = True
            logger.debug("duplicate - %s", node)
            break

    return found


# Function to return the index no. of the given node in the list. This index value is used to specify the
# edges.
# n - string    value of the node to find
# alist - list  list to be looked up
def getindex(n, alist):

    for index, i in enumerate(alist):
        if n == i:
            return str(index)


# Main function containing all the program logic and flow.
def main(argv):

    infile = ""
    outfile = ""

    try:
        infile, outfile = handlefileargs(argv)
    except ValueError:
        logger.error("Invalid arguments")
        sys.exit(2)

    csvinfo = readfile(infile)

    dot = creategraph("The Round Table")
    nodeList = []
    edgeList = []

    # Process each line in the input file
    # logger.debug("%s", csvinfo[2:])
    for index, item in enumerate(csvinfo):
        item[0] = item[0].strip()
        item[1] = item[1].strip()

        logger.info("%d - %s", index, item)
        if item[0] and item[1]:
            edgeList.append(item)   # Always add to edgeList

        # Take each item individually and check of duplicity before creating a new node for it
        if not dupnodes(item[0], nodeList) and item[0]:
            logger.debug("Appending %s to nodeList", item[0])
            nodeList.append(item[0])
        if not dupnodes(item[1], nodeList) and item[1]:
            logger.debug("Appending %s to edgeList", item[1])
            nodeList.append(item[1])

    logger.debug("Length of nodelist = %d", len(nodeList))
    logger.debug("Length of edgelist = %d", len(edgeList))
    # Create nodes with the nodeList as input
    for index, x in enumerate(nodeList):
        logger.info("Node - %s at %d", x, index)
        dot.node(str(index), label=x)

    # Create edges with edgeList as input
    for x in edgeList:
        logger.info("Edge from - %s to - %s", x[0], x[1])
        dot.edge(getindex(x[0], nodeList), getindex(x[1], nodeList))

    print(dot.source)
    dot.render(outfile, view=True)


# Start of main program
if __name__ == "__main__":
    main(sys.argv[1:])


