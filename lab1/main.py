class NodArbore:
    def __init__(self, informatie, parinte=None):
        self.informatie =informatie
        self.parinte=parinte

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
            nod=nod.parinte
        return False

    def __str__(self):
        return str(self.informatie)

    #c (a->b->c)
    def __repr__(self):
        return "{}, ({})".format(str(self.informatie), "->".join([str(x)   for x in self.drumRadacina()]))


class Graf:
    def __init__(self, matr, start, scopuri):
        self.matr=matr
        self.start=start
        self.scopuri=scopuri

    def scop(self, informatieNod):
        return informatieNod in self.scopuri

    def succesori(self, nod):
        lSuccesori=[]
        for infoSuccesor in range(len(self.matr)):
            if self.matr[nod.informatie][infoSuccesor]==1 and not nod.inDrum(infoSuccesor):
                lSuccesori.append(NodArbore(infoSuccesor,nod))
        return lSuccesori


def breadthFirst(gr, nsol=2):
    coada=[NodArbore(gr.start)]
    while coada:
        nodCurent=coada.pop(0)
        if gr.scop(nodCurent.informatie):
            print(repr(nodCurent))
            nsol-=1
            if nsol==0:
                return
        coada+=gr.succesori(nodCurent)





m = [
    [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
]


start = 0
scopuri = [5, 9]


gr=Graf(m,start,scopuri)
breadthFirst(gr, nsol=3)