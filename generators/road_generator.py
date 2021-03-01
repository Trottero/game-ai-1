from generators.generator import Generator
import numpy as np
import itertools
from blocks import Blocks
import heapq
import sys
from multiprocessing import Pool, cpu_count


class RoadGenerator(Generator):

    # Uses kruskal to generate a minimum spanning tree and dijkstra to calculate paths

    def __init__(self, diagonal_paths=False):
        self.costs = {
            # Grass
            1: 1,
            2: 5,

            # Water
            3: 20,
            4: 35,

            # Sand
            5: 2,

            # village
            6: 0,
            # path
            7: 0
        }
        self.diagonal_paths = diagonal_paths
        pass

    def apply(self, world, height_map):
        vertices = []
        for x in range(len(world)):
            for y in range(len(world)):
                if world[x, y] == Blocks.VILLAGE and not (world[x - 1, y] == Blocks.VILLAGE or world[x, y - 1] == Blocks.VILLAGE):
                    vertices.append((x, y))

        edges = []
        perms = list(itertools.combinations(vertices, 2))
        with Pool(cpu_count()) as p:
            results = [p.apply_async(self.find_path, (world, s, t))
                       for s, t in perms]
            results = [result.get() for result in results]
            edges = [(s, t, length, path)
                     for (s, t), (length, path) in zip(perms, results)]

        edges_sorted = sorted(edges, key=lambda x: x[2])

        MST = self.kruskal(vertices, edges_sorted)

        for path in MST:
            self.draw_path(world, path)
        return world, height_map

    def kruskal(self, vertices, edges):
        MST = []
        uf = UF(len(vertices))
        for e in edges:
            u, v, w, p = e
            # if u, v already connected, abort this edge
            if uf.connected(vertices.index(u), vertices.index(v)):
                continue
            # if not, connect them and add this edge to the MST
            uf.union(vertices.index(u), vertices.index(v))
            MST.append(p)
        return MST

    def find_path(self, world, source, target):
        # D I J K S T A
        dist = {}
        dist[target] = sys.maxsize
        dist[source] = 0

        prev = {}
        active_list = []
        active_list.append(source)

        visited = []
        found = False

        while len(active_list) > 0:
            # Select node with lowest current cost
            current = self.get_min_node(
                {pos: dist[pos] for pos in active_list})
            if current == target:
                found = True
            if found and dist[current] > dist[target]:
                # early cut off
                break
            # Remove element from active list
            active_list.remove(current)
            # add to visited
            visited.append(current)

            # Add all of its non-visisted neightbours to the active list
            n = self.get_neighbours(world, current)
            uniques = [neigh for neigh in n if neigh not in active_list]
            uniques = [neigh for neigh in uniques if neigh not in visited]
            if len(uniques) > 0:
                active_list.extend(uniques)
            for next in n:
                length = self.costs[world[current]]

                alt = dist[current] + length + self.manhattan(current, target)
                if next not in dist.keys() or alt < dist[next]:
                    dist[next] = alt
                    prev[next] = current
        return dist[target], self.track_back(target, prev)

    def get_min_node(self, nodes):
        return min(nodes, key=nodes.get)

    def manhattan(self, source, target):
        x0, y0, = source
        x1, y1, = target
        return abs(x0 - x1) + abs(y0 - y1)

    def get_neighbours(self, world, pos):
        wn = len(world) - 1
        x, y = pos
        n = set([(x, y), (min(x + 1, wn), y), (max(x - 1, 0), y),
                 (x, min(y + 1, wn)), (x, max(y - 1, 0))])
        # Check if diagonal_paths need to beadded
        if self.diagonal_paths:
            n.add((min(x + 1, wn), min(y + 1, wn)))
            n.add((min(x + 1, wn), max(y - 1, 0)))
            n.add((max(x - 1, 0), min(y + 1, wn)))
            n.add((max(x - 1, 0), max(y - 1, 0)))
            pass
        n.remove((x, y))
        return list(n)

    def track_back(self, node, prev, path=[]):
        if node in prev.keys():
            return self.track_back(prev[node], prev, [prev[node], *path])
        return path

    def draw_path(self, world, path):
        for seg in path:
            world[seg] = Blocks.PATH if world[seg] != Blocks.VILLAGE else world[seg]

# Union find data structure for quick kruskal algorithm


class UF:
    def __init__(self, N):
        self._id = [i for i in range(N)]

    # judge two node connected or not
    def connected(self, p, q):
        return self._find(p) == self._find(q)

    # quick union two component
    def union(self, p, q):
        p_root = self._find(p)
        q_root = self._find(q)
        if p_root == q_root:
            return
        self._id[p_root] = q_root

    # find the root of p
    def _find(self, p):
        while p != self._id[p]:
            p = self._id[p]
        return p
