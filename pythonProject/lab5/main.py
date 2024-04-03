import copy

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
    def __init__(self, start, scopuri):
        self.start = start
        self.scopuri = scopuri

    def scop(self, informatieNod):
        return informatieNod in self.scopuri

    def valideaza(self):
        matrDesfasurata = self.start[0] + self.start[1] + self.start[2]
        nrInvers = 0
        for i, placuta in enumerate(matrDesfasurata):
            for placuta2 in matrDesfasurata[i+1:]:
                if placuta > placuta2 and placuta2:
                    nrInvers += 1
        return nrInvers % 2 == 0


    def estimeaza_h(self, infoNod, euristica):
        if self.scop(infoNod):
            return 0
        if euristica == "banala":
            return 1
        if euristica == "euristica mutari":
            min_h = float('inf')
            for scop in scopuri:
                h = 0
                for iLinie, linie in enumerate(scop):
                    for iPlacuta, placuta in enumerate(linie):
                        if infoNod[iLinie][iPlacuta] != placuta:
                            h += 1
                if h < min_h:
                    min_h = h
            return min_h

    def succesori(self, nod, euristica):

        def gasesteGol(matr):
            for l in range(3):
                for c in range(3):
                    if matr[l][c] == 0:
                        return l, c

        lSuccesori = []
        lGol, cGol = gasesteGol(nod.informatie)
        directii = [[-1, 0], [1, 0], [0, 1], [0, -1]]

        for d in directii:
            lPlacuta = lGol + d[0]
            cPlacuta = cGol + d[1]
            if not (0 <= lPlacuta <= 2 and 0 <= cPlacuta <= 2):
                continue

            infoSuccesor = copy.deepcopy(nod.informatie)
            infoSuccesor[lGol][cGol], infoSuccesor[lPlacuta][cPlacuta] = infoSuccesor[lPlacuta][cPlacuta], infoSuccesor[lGol][cGol]
            if not nod.inDrum(infoSuccesor):
                lSuccesori.append(NodArbore(infoSuccesor, nod.g+1, self.estimeaza_h(infoSuccesor, euristica), nod))
        return lSuccesori


def aStar(g, euristica):
    if not g.valideaza():
        print("nu avem solutii!!!")
        return
    OPEN = [NodArbore(gr.start)]
    CLOSED = []
    while OPEN:
        nodCurent = OPEN.pop(0)
        CLOSED.append(nodCurent)
        if gr.scop(nodCurent.informatie):
            print(repr(nodCurent))
            return

        lSuccesori = gr.succesori(nodCurent, euristica)
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
    print("nu avem solutii!!!")


f = open("input.txt", "r")
continut = f.read()
start = [list(map(int, linie.strip().split())) for linie in continut.strip().split("\n")]
scopuri = [
    [[1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]]
]

gr = Graf(start, scopuri)
aStar(gr, "euristica mutari")





