from interfaces import Interface, getInterface
import config
import gcode

class Progress:
    def __init__(self,source):
        self.source = source
        self.l = len(source)
        self.k = 100./self.l
    
    def __iter__(self):
        self.i = 0
        return self
    
    def __next__(self):
        if self.i == self.l:
            raise StopIteration()
        p=int(self.i*self.k)
        r = self.source[self.i]
        self.i+=1
        return p,r
    
def main():
    cfg:config.MongooseConfig = config.loadConfig()
    interface:Interface = getInterface(cfg.interface)
    parser = gcode.GCodeParser()
    with open('boomerangv4.ncc') as f:
        data = f.readlines()
    
    for i,line in Progress(data):
        g = parser.parse(line)
        if g.shouldProcess():
            print(f'{i:02}%:{g.format()}',end="   >   ")
            r = interface.send(g)
            print(r.format())
        else:
            print(g.format())
    


if __name__ == "__main__":
    main()

