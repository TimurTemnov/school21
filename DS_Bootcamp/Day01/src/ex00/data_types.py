def data_types():
    var1 = 1
    var2 = "some string"
    var3 = 3.2
    var4 = True
    var5 = [1,2,3]
    var6 = {'first' : '25'}
    var7 = (1,2,3) 
    var8 = {1,2,3}

    print(f"[{type(var1).__name__}, {type(var2).__name__}, {type(var3).__name__}, {type(var4).__name__}, {type(var5).__name__}, {type(var6).__name__}, {type(var7).__name__}, {type(var8).__name__}]")

if __name__ == '__main__':
    data_types()