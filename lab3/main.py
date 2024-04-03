import queue
from time import time
import cProfile


class NodArbore:
    def __init__(self, informatie, g=0, h=0, parinte=None):
        self.informatie = informatie
        self.parinte = parinte
        self.g = g
        self.h = h
        self.f = g + h

    def drumRadacina(self):
        nod=self
        lDrum=[]
        while nod:
            lDrum.append(nod)
            nod=nod.parinte
        return lDrum[::-1]

    def inDrum(self,infonod):
        nod=self
        while nod:
            if nod.informatie==infonod:
                return True
            nod = nod.parinte
        return False

    def __eq__(self, other):
        return self.f == other.f and self.g == other.g

    # are sens?
    def __le__(self, other):
        return self.f <= other.f

    def __lt__(self, other):
        return self.f < other.f or (self.f == other.f and self.g > other.g)

    def __gt__(self, other):
        return self.f > other.f

    def __str__(self):
        return f"({str(self.informatie)}, g: {self.g}, f: {self.f})"

    def __repr__(self):
        return "{}, ({})".format(str(self.informatie), "->".join([str(x) for x in self.drumRadacina()]))


class Graf:
    def __init__(self, matr, start, scopuri, h):
        self.matr = matr
        self.start = start
        self.scopuri = scopuri
        self.h = h

    def scop(self, informatieNod):
        return informatieNod in self.scopuri

    def estimeaza_h(self, infoNod):
        return self.h[infoNod]

    def succesori(self, nod):
        lSuccesori = []
        for infoSuccesor in range(len(self.matr)):
            if self.matr[nod.informatie][infoSuccesor] > 0 and not nod.inDrum(infoSuccesor):
                lSuccesori.append(NodArbore(infoSuccesor, nod.g+self.matr[nod.informatie][infoSuccesor], self.estimeaza_h(infoSuccesor), nod))
        return lSuccesori


def aStarSolMultiple(gr, nsol):
    coada=[NodArbore(gr.start)]
    while coada:
        nodCurent = coada.pop(0)
        if gr.scop(nodCurent.informatie):
            print(repr(nodCurent))
            nsol -= 1
            if nsol == 0:
                return
        coada += gr.succesori(nodCurent)
        coada.sort()


# cu priority queue
def aStarSolMultiplePQ(gr, nsol):
    pq = queue.PriorityQueue()
    pq.put(NodArbore(gr.start))
    while pq:
        nodCurent = pq.get()
        if gr.scop(nodCurent.informatie):
            print(repr(nodCurent))
            nsol -= 1
            if nsol == 0:
                return
        for succesor in gr.succesori(nodCurent):
            pq.put(succesor)


def bin_search(listaNoduri, nodNou):
    ls = 0
    ld = len(listaNoduri) - 1
    while ls <= ld:
        mij = (ls + ld) // 2
        if listaNoduri[mij] == nodNou:
            return mij
        elif nodNou < listaNoduri[mij]:
            ld = mij - 1
        else:
            ls = mij + 1
    return ls


def aStarSolMultiple2(gr, nsol):
    coada=[NodArbore(gr.start)]
    while coada:
        nodCurent = coada.pop(0)
        if gr.scop(nodCurent.informatie):
            print(repr(nodCurent))
            nsol -= 1
            if nsol == 0:
                return

        for succesor in gr.succesori(nodCurent):
            poz = bin_search(coada, succesor)
            coada.insert(poz, succesor)


m = [
    [0, 3, 5, 10, 0, 0, 100],
    [0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 4, 9, 3, 0],
    [0, 3, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 5],
    [0, 0, 3, 0, 0, 0, 0],
]
start = 0
scopuri = [4, 6]
h = [0, 1, 6, 2, 0, 3, 0]

gr = Graf(m, start, scopuri, h)


# ex 3
def compare_solutii():
    # 235 function calls in 0.005 seconds
    # 235 function calls in 0.000 seconds
    #  0.0 milisecunde
    #  0.0 milisecunde
    #  0.9770393371582031 milisecunde
    start_time = time()
    cProfile.run('aStarSolMultiple(gr, nsol=4)')
    # aStarSolMultiple(gr, nsol=4)
    end_time = time()
    # print(f"timp executare A*: {(end_time - start_time)*1000} milisecunde")
    print("----------------------------------------------")

    # 497 function calls in 0.002 seconds
    # 497 function calls in 0.001 seconds
    #  0.9732246398925781 milisecunde
    #  0.0 milisecunde
    #  0.0 milisecunde
    start_time_pq = time()
    cProfile.run('aStarSolMultiplePQ(gr, nsol=4)')
    # aStarSolMultiplePQ(gr, nsol=4)
    end_time_pq = time()
    # print(f"timp executare A* cu priority queue: {(end_time_pq - start_time_pq)*1000} milisecunde")

# compare_solutii()

# ex 4
aStarSolMultiple(gr, nsol=4)
print('----------------------------------------------------')
aStarSolMultiple2(gr, nsol=4)


def aStar(g):
    OPEN = [NodArbore(gr.start)]
    CLOSED = []
    while OPEN:
        nodCurent = OPEN.pop(0)
        CLOSED.append(nodCurent)
        if gr.scop(nodCurent.informatie):
            print(repr(nodCurent))
            return

        lSuccesori = gr.succesori(nodCurent)
        for s in lSuccesori:
            gasitOpen = False
            for nodC in OPEN:
                if s.informatie == nodC.informatie:
                    gasitOpen = True
                    if s < nodC:
                        OPEN.remove(nodC)
                    else:
                        lSuccesori.remove(s)
            if not gasitOpen:
                for nodC in CLOSED:
                    if s.informatie == nodC.informatie:
                        if s < nodC:
                            CLOSED.remove(nodC)
                        else:
                            lSuccesori.remove(s)
        OPEN += lSuccesori
        OPEN.sort()

