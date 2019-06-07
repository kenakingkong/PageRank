'''
    CSC 466 Lab 7 Eight Legged Freaks
    Makena Kong 

    Program to find the top 10 results of a search
    query using a Page Rank Algorithm
'''

import os, sys, random, requests
import networkx as nx
from bs4 import BeautifulSoup

# parse user input
def parseInput(user_input):
    query = user_input.lower().title().split()
    length = len(query)

    if (length==1 and query[0] == "Quit"):
        return "quit"

    while "And" in query:
        ind = query.index("And")
        query[ind-1:ind+2] = [[query[ind-1],query[ind+1]]]

    while "Or" in query:
        query.remove("Or")

    return query

# return a complete graph of web pages 
def createGraph():
    # initialize graph
    G = nx.DiGraph()
    
    #getting the web pages
    url = "http://frank.cadrc.calpoly.edu/city_web/"
    myRequest = requests.get(url)
    soup = BeautifulSoup(myRequest.text,"html.parser")

    # create all the nodes
    table = soup.find("table")
    for row in table.find_all("td"):
        row_link = row.find("a")
        if (row_link != None):
            link = row_link.get("href")
            if (link != "/"):
                name = link.replace(".html", "")
                G.add_node(name, link=link, cities=[], links=[], rank=0)

    #page_url = "http://frank.cadrc/calpoly.edu/city_web/" + node["link"]
    #req = requests.get(page_url)
    #page_soup = BeautifulSoup(req.text,'html.parser')

    # initial rank
    total_nodes = G.number_of_nodes()
    first_rank = 1/total_nodes

    path = "/var/www/html/city_web/"

    # create edges and add initial page rank
    node_list = list(G.nodes())
    for node_name in node_list:
        node = G.node[node_name]
        node["rank"] = first_rank

        f = open(path+node["link"], "r")
        soup = BeautifulSoup(f.read(), "html.parser")

        for item in soup.find_all("a"):
            link = item.get("href")
            name = link.replace(".html", "")
            city = item.get_text()

            node["links"].append(link)
            node["cities"].append(city)
            G.add_edge(node_name,name)

    return G

'''
    page rank of a page is the sum of ....
    page rank of linker / outgoing links of linker
'''

# given a graph of pages
# iterates twice to rank all of them
def rankPages(G):
    
    node_list = list(G.nodes())
    for node_name in node_list:

        sum_rank = 0
        predecessors = list(G.predecessors(node_name))
        for prev in predecessors:
            prev_node = G.node[prev]
            p_rank = prev_node["rank"]
            outlinks = len(prev_node["links"])
            sum_rank += p_rank/outlinks

        G.node[node_name]["rank"] = sum_rank
    
    return G


def oldTopTenPages(G):
    node_list = list(G.nodes())
    sorted_pages = sorted(node_list, key = lambda i: G.node[i]['rank'],reverse=True)[:10]
    return sorted_pages

def containsPages(cities,query):
    check = False
    for item in query:
        if type(item) == list:
            if all(elem in cities for elem in item):
                check = True
        if type(item) == str:
            if item in cities:
                check = True
    return check

def topTenPages(G, query):
    filtered_nodes = filter(lambda x: containsPages(cities=x[1]["cities"],query=query), G.nodes(data=True))
    sorted_pages = sorted(filtered_nodes, key = lambda i: i[1].get('rank'),reverse=True)[:10]
    return sorted_pages

def main():

    print("Lab 7 search engine by Makena Kong")
    user_input = input("Please input your search term or “quit” to exit the program: ")
    query = parseInput(user_input)
    while (query != "quit"):
        graph = createGraph()

        # rank pages
        graph_iter_1 = rankPages(graph)
        graph_iter_2 = rankPages(graph_iter_1)
        graph_iter_3 = rankPages(graph_iter_2)

        # query
        # each page has at least one incoming link where the query is linked to the page by some other page.
        topTen = topTenPages(graph_iter_3, query)
        for page in topTen:
            print(page[0] + ".html")

        user_input = input("Please input your search term or “quit” to exit the program: ")
        query = parseInput(user_input)
        
    return

if __name__=="__main__":
    main()