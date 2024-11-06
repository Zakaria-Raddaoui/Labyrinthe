from pyamaze import maze, agent, textLabel
from queue import Queue, LifoQueue
class Graphe:
    def __init__(self):
        self.noeuds = {}

    def ajouterNoeud(self, noeud):
        if noeud not in self.noeuds:
            self.noeuds[noeud] = []

    def ajouterArc(self, orig, dest):
        if orig in self.noeuds:
            self.noeuds[orig].append(dest)

    def listerNoeuds(self):
        return list(self.noeuds.keys())

    def listerArcs(self):
        arcs = []
        for noeud, voisins in self.noeuds.items():
            for voisin in voisins:
                arcs.append((noeud, voisin))
        return arcs

    def adjacenceNoeud(self, noeud):
        return self.noeuds.get(noeud, [])


class SearchLabyrinthe:
    def __init__(self, graphe, start=None, goal=None):
        self.graphe = graphe
        self.explores = {}
        self.accessibles = {}
        self.start = start
        self.goal = goal
    def successeurs(self, etat):
        return self.graphe.adjacenceNoeud(etat)

    def verifEtat(self, etat, explores, accessibles):
        return etat in explores or etat in accessibles

    def succValides(self, etat, explores, accessibles):
        return [s for s in self.successeurs(etat) if s not in explores and s not in accessibles]

    def BFS(self, m):
        start = (m.rows, m.cols)
        frontier = Queue()
        frontier.put(start)
        exploree = set()
        bfs_path = {}
        while not frontier.empty():
            cell_courant = frontier.get()
            if cell_courant == (1, 1):
                break
            for d in 'ESNW':
                if m.maze_map[cell_courant][d]:
                    if d == 'E':
                        cell_suiv = (cell_courant[0], cell_courant[1] + 1)
                    elif d == 'W':
                        cell_suiv = (cell_courant[0], cell_courant[1] - 1)
                    elif d == 'S':
                        cell_suiv = (cell_courant[0] + 1, cell_courant[1])
                    elif d == 'N':
                        cell_suiv = (cell_courant[0] - 1, cell_courant[1])

                    if cell_suiv not in exploree:
                        exploree.add(cell_suiv)
                        frontier.put(cell_suiv)
                        bfs_path[cell_suiv] = cell_courant
        return bfs_path

    def DFS(self, m):
        start = (m.rows, m.cols)
        frontier = LifoQueue()
        frontier.put(start)
        exploree = set()
        dfs_path = {}
        while not frontier.empty():
            cell_courant = frontier.get()
            if cell_courant == (1, 1):
                break
            for d in 'ESNW':
                if m.maze_map[cell_courant][d]:
                    if d == 'E':
                        cell_suiv = (cell_courant[0], cell_courant[1] + 1)
                    elif d == 'W':
                        cell_suiv = (cell_courant[0], cell_courant[1] - 1)
                    elif d == 'S':
                        cell_suiv = (cell_courant[0] + 1, cell_courant[1])
                    elif d == 'N':
                        cell_suiv = (cell_courant[0] - 1, cell_courant[1])

                    if cell_suiv not in exploree:
                        exploree.add(cell_suiv)
                        frontier.put(cell_suiv)
                        dfs_path[cell_suiv] = cell_courant
        return dfs_path

    def retourChemin(self, path, start, goal):
        current = goal
        full_path = [current]
        while current != start:
            current = path[current]
            full_path.append(current)
        full_path.reverse()
        return full_path


g = Graphe()
search = SearchLabyrinthe(g)
m = maze(10, 10)
m.CreateMaze()

chemin_bfs = search.BFS(m)
chemin_dfs = search.DFS(m)

solu_bfs = search.retourChemin(chemin_bfs, start=(m.rows, m.cols), goal=(1, 1))
solu_dfs = search.retourChemin(chemin_dfs, start=(m.rows, m.cols), goal=(1, 1))

a = agent(m, footprints=True)
b = agent(m, footprints=True, color='yellow')

m.tracePath({a:solu_bfs, b:solu_dfs}, delay=100)
lbl1 = textLabel(m, 'Nombre des états découverts de BFS: ', len(solu_bfs))
lbl2 = textLabel(m, 'Nombre des états découverts de DFS: ', len(solu_dfs))

m.run()




