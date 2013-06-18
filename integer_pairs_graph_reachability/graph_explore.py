from collections import deque, defaultdict

explored=set()
frontier=deque()

# these functions are for general graph exploration, or at least could have features added to do so.

def init():
    global explored
    explored=set()
    global frontier
    frontier=deque()

def next_unexplored_node():
    try:
        node=frontier.popleft()
        while node in explored:
            node=frontier.popleft()
    except IndexError:
        node=None
    return node

def explore_node(u,out_edges_f):
    destinations=out_edges_f(u)
    for v in out_edges_f(u):
        frontier.append(v)
    explored.add(u)

# contains functions specific to this graph exploration problem
def challenge(max_sum_of_digits):
    # ex. 
    #digits(49)
    # (4, 9)
    #digits(4929329)
    # (4, 9, 2, 9, 3, 2, 9)   
    def digits(n):
        n=abs(n)
        if n==0:
            return ()
        digit=n % 10
        return digits((n-digit)/10) + (digit,)

    def x_coord(point):
        return point[0]

    def y_coord(point):
        return point[1]

    def out_edge_destinations(node):
        def acceptable(node):
            return sum(map(abs, digits(x_coord(node))+digits(y_coord(node)))) <= max_sum_of_digits
        mods=((1,0),(0,1),(-1,0),(0,-1))
        return filter (acceptable, map (lambda mod: tuple(map(sum,zip(node,mod))), mods))
    node=(0,0)
    while node:
        explore_node(node,out_edges_f=out_edge_destinations)
        node=next_unexplored_node()
    return len(explored)

if __name__=="__main__": # if this is run as a script
    import sys
    try:
        max_sum_of_digits=int(sys.argv[1])
    except IndexError:
        max_sum_of_digits=19
    print challenge(max_sum_of_digits),'nodes reachable with',max_sum_of_digits,'as max sum of digits'
