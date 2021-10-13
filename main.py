import puzzle
import a_star
from datetime import datetime

f1 = open("./boards/board1.txt", "r")
f2 = open("./boards/spiralBoard.txt", "r")
f3 = open("./boards/backwardBoard.txt", "r")


def run(file):
    f = file
    p = puzzle.Puzzle(f)
    sol = p.init_solution()
    search = a_star.AStarSearch(p, sol)
    start = datetime.now()
    search.search()
    stop = datetime.now()
    print("runtime: ", stop - start)
    print('===================================')


run(f1)
run(f2)
run(f3)
