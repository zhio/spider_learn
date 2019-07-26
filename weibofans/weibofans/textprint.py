acotr = []
with open('actor.txt','r') as f:
    while True:
        lines = f.readline()
        if not lines :
            break
            pass
        lines = eval(lines)
        #print(lines)
        acotr = acotr+lines
print(acotr)

