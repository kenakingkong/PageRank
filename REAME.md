# CSC 466 Lab 7
Makena Kong

## Packages Needed
* Networkx - for the graph
* BeautifulSoup - for parsing html

## How I implemented this

### Step 1: Create the Graph
1. Created the Node for each webpage
    * A NetworkX Digraph's node is represented as a tuple (html name, {cities,links,rank})
2. For each node
    * visit its page
    * add its edges
    * add its Page Rank (1/n)
### Step 2: Iterate to Get Page Ranks
1. I iterated twice because a youtube video did it twice.
### Step 3: Get query by user input
### Step 4: Parse the user input
1. Combined search words coupled by "and" starting left to right
2. Got rid of "or" words
### Step 5: Filter the Nodes/Pages by query
### Step 6: Sort the result by rank
### Step 7: Print the top ten pages
