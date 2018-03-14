__author__ = 'Jordi Vilaplana'

import json
import csv

if __name__ == '__main__':

    filtered_nodes = []
    filtered_links = []

    filtered_node_list = []

    nodes = []
    with open('nodes.csv', 'r') as data_file:
        data = csv.reader(data_file.read().splitlines())

        i = 0
        for line in data:
            nodes.append(line)
            i += 1
        print "Total nodes: " + str(i)

    links = []
    with open('links.csv', 'r') as data_file:
        data = csv.reader(data_file.read().splitlines())

        i = 0
        for line in data:
            links.append(line)
            i += 1
        print "Total links: " + str(i)

    for node in nodes:
        node_occurrences = 0

        if node[0] == '1':
            filtered_nodes.append(node)
            filtered_node_list.append(node[1])

        if node[0] == '2':
            for link in links:
                if link[0] == node[1] or link[1] == node[1]:
                    node_occurrences += 1
                    if node_occurrences > 22:
                        filtered_nodes.append(node)
                        filtered_node_list.append(node[1])
                        break

    for link in links:
        if link[0] in filtered_node_list and link[1] in filtered_node_list:
            filtered_links.append(link)

    # for node in filtered_nodes:
    #     for link in links:
    #         if link[0] == node[1] or link[1] == node[1]:
    #             filtered_links.append(link)

    print "Filtered nodes: " + str(len(filtered_nodes))
    print "Filtered links: " + str(len(filtered_links))

    with open('filtered_nodes22.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(filtered_nodes)

    with open('filtered_links22.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(filtered_links)

    print "Done!"
