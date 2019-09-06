
# import heapq
# import queue
# a = ['anc', 'njnjf', 'cnje']

# print(list(zip(*a)))
# h = {'a': 2, 'b': 4, 'c': 1}
# print(sorted(h, key=h.get))
# q = queue.PriorityQueue()
# q.put((2, 4))
# q.put((2, 2))
# q.put((4, 4))
# print(q.get())
# hq = [[1, 54], [5, 77], [2, 43], [4, 53], [6, 32], [7, 88]]
# heapq.heapify(hq)
# print(hq)
# print(heapq.nsmallest(3, hq, key=lambda x: x[1]))
# print(heapq.nlargest(3, hq, key=lambda x: x[1]))
# a = [1, 2, 3]
# d = {}
# print(d.get('a', 0))
# print('.'.join(['com']))
# s = 'manhattan'
# print((s[2:], 'hello'))
# print(*(s[2:], 'hello'))
# print(s[:1])
# print(s[-1:])
# print(s[:-1])


# def iterative_levenshtein(s, t):
#     """
#         iterative_levenshtein(s, t) -> ldist
#         ldist is the Levenshtein distance between the strings
#         s and t.
#         For all i and j, dist[i,j] will contain the Levenshtein
#         distance between the first i characters of s and the
#         first j characters of t
#     """
#     rows = len(s)+1
#     cols = len(t)+1
#     dist = [[0 for x in range(cols)] for x in range(rows)]
#     # source prefixes can be transformed into empty strings
#     # by deletions:
#     for i in range(1, rows):
#         dist[i][0] = i
#     # target prefixes can be created from an empty source string
#     # by inserting the characters
#     for i in range(1, cols):
#         dist[0][i] = i

#     for col in range(1, cols):
#         for row in range(1, rows):
#             if s[row-1] == t[col-1]:
#                 cost = 0
#             else:
#                 cost = 1
#             dist[row][col] = min(dist[row-1][col] + 1,      # deletion
#                                  dist[row][col-1] + 1,      # insertion
#                                  dist[row-1][col-1] + cost)  # substitution
#     for r in range(rows):
#         print(dist[r])

#     return dist[row][col]


# print(iterative_levenshtein("abcd", "dabcd b"))
import os
f = open('sample_product_data.tsv')
print(f.fileno(), f.tell(), f.readline(), sep='\n')
