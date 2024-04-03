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

    def estimeaza_h(self, infoNod, euristica):
        if self.scop(infoNod):
            return 0
        if euristica == "banala":
            return 1
        if euristica == "euristica mutari":
            min_h = float('inf')
            for scop in scopuri:
                h = 0
                for iStiva, stiva in enumerate(scop):
                    for iBloc, bloc in enumerate(stiva):
                        try:
                            if infoNod[iStiva][iBloc] != bloc:
                                h += 1
                        except:
                            h += 1
                if h < min_h:
                    min_h = h
            return min_h
        if euristica == "euristica costuri":
            return
        if euristica == "euristica neadmisibila":
            return 1000

    def succesori(self, nod, euristica):
        lSuccesori = []
        for i, stiva in enumerate(nod.informatie):
            if not stiva:
                continue
            copieStive = copy.deepcopy(nod.informatie)
            bloc = copieStive[i].pop()
            for j in range(len(nod.informatie)):
                if i == j:
                    continue
                infoSuccesor = copy.deepcopy(copieStive)
                infoSuccesor[j].append(bloc)
                if not nod.inDrum(infoSuccesor):
                    lSuccesori.append(NodArbore(infoSuccesor, nod.g+1, self.estimeaza_h(infoSuccesor, euristica), nod))
        return lSuccesori


def aStar(g, euristica):
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


def calculeazaStive(sir):
    return [sirStiva.strip().split() if sirStiva != "#" else [] for sirStiva in sir.strip().split('\n')]


f = open("input.txt","r")
sirStart, sirScopuri=f.read().split("=========")
start = calculeazaStive(sirStart)
scopuri = [calculeazaStive(sirScop) for sirScop in sirScopuri.split("---")]

gr = Graf(start, scopuri)
# print(start)
# print(scopuri)

aStar(gr, "euristica mutari")
