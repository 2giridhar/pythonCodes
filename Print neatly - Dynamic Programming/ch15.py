import sys
from numpy import *
INFINITY = sys.maxint


def find_costs(words, M):
    # calculating individual costs of the dynamic programming table.
    n = len(words)
    spaces = zeros((n, n), dtype=int)
    costs = zeros((n, n), dtype=int)
    for i in range(0, n):
        spaces[i][i] = M - len(words[i])
        for j in range(i + 1, n):
            spaces[i][j] = spaces[i][j - 1] - (len(words[j]) + 1)
            if spaces[i][j] < 0:
                costs[i][j] = INFINITY
            elif j == n - 1 and spaces[i][j] >= 0:
                costs[i][j] = 0
            else:
                costs[i][j] = spaces[i][j] ** 3
    return costs


def print_neatly(words, M):
    """ Print text neatly.

    Parameters
    ----------
    words: list of str
        Each string in the list is a word from the file.
    M: int
        The max number of characters per line including spaces

    Returns
    -------
    cost: number
        The optimal value as described in the textbook.
    text: str
        The entire text as one string with newline characters.
        It should not end with a blank line.

    Details
    -------
        Look at print_neatly_test for some code to test the solution.
    """
    n = len(words)
    costs = find_costs(words, M)

    least_costs = zeros((n,), dtype=int)
    word_links = zeros((n,), dtype=int)
    # Finding the least cost till each word and then using it to find the least value of next word.
    for i in range(0, n):
        least_costs[i] = INFINITY
        for j in range(0, i):
            new_cost = least_costs[j - 1] + costs[j][i]
            if new_cost < least_costs[i]:
                least_costs[i] = new_cost
                word_links[i] = j

    # Backtracking from the last word to form lines with appropriate words.
    i = n
    text = ""
    while i > 0:
        j = word_links[i - 1]
        line = words[j]
        for j in range(j + 1, i):
            line += ' ' + words[j]
        if i != n:
            text = line + '\n' + text
        else:
            text = line
        i = j

    return least_costs[n - 1], text
