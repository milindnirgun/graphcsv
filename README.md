# GraphCSV
Python utility to generate directed dependency graphs from a CSV file using Graphviz.

This is a simple python program that takes a CSV file as input and generates a directed dependency graph in a pdf output file.
Some advantages for using this program are:
* Cross-platform, as long as the prerequisite software is installed
* User does not need to learn a DSL (Domain Specific Language) like dot to use Graphviz
* Simplicity of use thru the ubiquitous spreadsheet

## Setup Guide
Pre-requisites for using GraphCSV program are:
1. Install Python3 on your PC - [Download from Python.org](https://www.python.org/downloads/)
2. Install Graphviz - [Download and follow instructions from here](https://www.graphviz.org/download/)
Clone this repository to download the program and examples.

## Running GraphCSV
In the directory where graphcsv.py is downloaded alongwith the examples directory, run:
```
python graphcsv.py -i examples/round_table.csv
```
This should pop up the PDF viewer installed on your system and display a pdf file with the graph in it. This generated pdf
is saved in the same directory where the input csv file is in the above example. Optionally a "-o <filename.pdf>" argument
can be passed to the above command to save the output file with a different name or location. 
A second file is also generated with the name of the input csv with the .csv extension and it contains the _dot_ language
source that is used by Graphviz to render the graph. This is just for the user's reference and can be deleted.

## Input File Format
A quick note about the input csv file format. The graphcsv.py program expects this csv file to follow some syntax to be able
to draw a correct graph. If the output graph is not as expected or the program errors out, check this csv file format. The
format is very simple, with the first row as header defining columns "parent" and "child". The header row is ignored for now
and is intended for future extensions. Both columns define the nodes with their labels and the edges are drawn from the parent
node in the first column to the child node in the second column. If a node has _n_ edges, either from it or to it, it must
appear in _n_ rows in the respective column. 
Let's walk thru one of the examples in the round_table.csv file. The CSV looks like this in a spreadsheet:

| Parent | Child |
| --------|:-------:|
|King Arthur | Sir Lancelot the Brave |
|King Arthur | Sir Bedevere the Wise |

This will generate the dependency graph shown below. Look at the other examples provided and run them to see the results.
![Dependency Graph](


