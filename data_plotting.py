# import matplotlib.pyplot as mpl
import matplotlib as mpl
mpl.__version__

def plot(y):
    x= []
    for i in range(len(y)):
        x.append(i)
        mpl.plot(x,y)
        mpl.title('title name')
        mpl.xlabel('time')
        mpl.ylabel('stock price')
        mpl.figure(fi)
        mpl.show()