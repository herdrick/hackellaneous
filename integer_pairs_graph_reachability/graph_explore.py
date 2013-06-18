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
def bittorrent_challenge(max_sum_of_digits):
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
    print 'DONE.'
    return len(explored)
    
# recur. note that this style of graph traversal, popping a node off the frontier to recur on, means that the call stack doesn't look like a path decending through the graph with max depth being the max depth of the graph. instead we go one level deeper into the call stack for each node in the graph. this is true whether we do BFS or DFS.
# this function is not tail recursive. put Is_solution into the signature of coins_graph_search() and then return that plus to make it so.
