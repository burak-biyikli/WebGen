#!/usr/bin/env python3



functions = [
    [1, (0, 255), (lambda x, y, i: i)],         #Imm
    [2, (0,  16), (lambda x, y, i: y<<i)],      #Shift
    [2, (0, 266), (lambda x, y, i: y+i)]        #Add
]

cnt = 0
i_map = {}

class tree_op:
    def __init__(self, x, y, i, func):
        self.x  = x
        self.y  = y
        self.i  = i
        self.fn = func
        global cnt
        cnt += 1

    def val(self):
        xt = self.x if isinstance(self.x, int) else self.x.val()
        yt = self.y if isinstance(self.y, int) else self.y.val()
        it = self.y if isinstance(self.i, int) else self.i.val()
        return self.fn(xt, yt, it)

    def depth(self):
        xd = 0 if isinstance(self.x, int) else self.x.depth()
        yd = 0 if isinstance(self.y, int) else self.y.depth()
        id = 0 if isinstance(self.i, int) else self.i.depth()
        return 1 + xd + yd + id

    def str(self, depth=1)


 

if __name__ == "__main__":

    idx = 0
    fnc = functions[idx][2]
    for i in range(functions[idx][1][0], functions[idx][1][1]):
        res = fnc(0,0,i)
        i_map[res] = tree_op(0, 0, i, fnc)


    for _ in range(4):
        print(cnt)
    
    print(i_map[0])
        
        
