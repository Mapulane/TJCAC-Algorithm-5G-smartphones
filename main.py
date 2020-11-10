from MarkovSimulation import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def main():
    print_hi('Hello 5G')
    #MarkovSimulator(1)

    fig, (ax1,ax2) =plt.subplots(1,2)

# ******************************blocking probability for RAT 1 voice ************************************#
    # x axis values
    x1 = [ 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5]
    y1 = []
    y1d = []
    y2 = []
    y2d = []
    y3 = []
    y3d = []
    y4 = []
    y4d = []
    y5 = []
    y5d = []
    y6 = []
    y6d = []

    i=1
    j=1
    while j<6.5:
        NCBP = MarkovSimulator(j) #return [NCBP1v, NCBP2v ,NCBP3v, HCDP1v, HCDP2v, HCDP3v, NCBP1d,  NCBP2d, NCBP3d,HCDP1d, HCDP2d, HCDP3d ]

        f1 = (NCBP[0] + NCBP[6]) /2
        f2 =(NCBP[1] + NCBP[7])/2
        f3 =(NCBP[2] +NCBP[8])/2
        f4 =(NCBP[3] +NCBP[9])/2
        f5 = (NCBP[4] + NCBP[10])/2
        f6 = (NCBP[5] + NCBP[11] )/2
        i=i +1
        y1.append(NCBP[0])
        y2.append(NCBP[1])
        y3.append(NCBP[2])
        y4.append(NCBP[3])
        y5.append(NCBP[4])
        y6.append(NCBP[5])
        y1d.append(NCBP[6])
        y2d.append(NCBP[7])
        y3d.append(NCBP[8])
        y4d.append(NCBP[9])
        y5d.append(NCBP[10])
        y6d.append(NCBP[11])
        j = j + 0.5

   # j = 0.5
    #i=0
    #while j<5.5:
    #    util = MarkovSimulator(j)
    #    y1.append(util[0])
     #   y1d.append(util[1])
     #   y2.append(util[2])
     #   Tutil = (util[0] + (util[1]) +util[2]) / 3
     #   y2d.append(Tutil)
     #   j = j + 0.5
     #   i = i + 1
        print(i, " ", i, " ", i, " ", i, " ",i, " ", i, " ", i, " ", i, " ", i, " ", i, " ",i, " ", i, " ", i, " ", i, " ", i, " ", i, " ",i, " ", i, " ", i, " ", i, " ", i, " ", i, " ",i, " ", i, " ", i, " ", i, " ", i, " ", i, " ",i, " ", i, " ", i)
        #print(util[0])
       # print(util[1])
       # print(util[2])


   # ax1.plot(x1, y1, color='green', label="G1 subscribers", linewidth=2, marker='o', markerfacecolor='green', markersize=6)
    #ax1.plot(x1, y1d, color='red', label="G2 subscribers  ", linewidth=2, marker='o', markerfacecolor='red', markersize=6)
    #ax1.plot(x1, y2, color='blue', label="G3 subscribers", linewidth=2, marker='o', markerfacecolor='blue', markersize=6)

    ax1.plot(x1, y1, color='green', label="new G1 subscriber ", linewidth=2, marker='o', markerfacecolor='green', markersize=7)
    ax1.plot(x1, y4, color='green', label="handoff G1 subscriber", linestyle='dashed', linewidth=2, marker='x',markerfacecolor='green', markersize=7)
    ax1.plot(x1, y2, color='red', label="new G2 subscriber", linewidth=2, marker='o', markerfacecolor='red',markersize=6)
    ax1.plot(x1, y5, color='red', label="handoff G2 subscriber", linestyle='dashed', linewidth=2, marker='x',markerfacecolor='red', markersize=6)
    ax1.plot(x1, y3, color='blue', label="new G3 subscriber", linewidth=2, marker='o', markerfacecolor='blue',markersize=7)
    ax1.plot(x1, y6, color='blue', label="handoff G3 subscriber", linestyle='dashed', linewidth=2, marker='x',markerfacecolor='blue', markersize=7)

    # setting x and y axis range
    ax1.set_xlim(1 , 5.5)
    ax1.set_ylim(0 , 1)


    # naming the x axis
    ax1.set_xlabel('Call Departure Rate')
    # naming the y axis
    ax1.set_ylabel('Blocking/Dropping Probability ')

    # giving a title to my graph
    ax1.set_title('Voce call blocking/dropping probability Vs Call Departure Rate')


    # plotting the points for second Graph
    #plt.plot(x, y, color='green', linestyle='dashed', linewidth=3, marker='o', markerfacecolor='blue', markersize=)
    #ax2.plot(x1, y2d, color='green',label="All subscribers", linewidth=2, marker='o', markerfacecolor='green', markersize=6)
    ax2.plot(x1, y1d, color='green', label="new G1 subscriber ", linewidth=2, marker='o', markerfacecolor='green',markersize=7)
    ax2.plot(x1, y4d, color='green', label="handoff G1 subscriber", linestyle='dashed', linewidth=2, marker='x',markerfacecolor='green', markersize=7)
    ax2.plot(x1, y2d, color='red', label="new G2 subscriber", linewidth=2, marker='o', markerfacecolor='red',markersize=6)
    ax2.plot(x1, y5d, color='red', label="handoff G2 subscriber", linestyle='dashed', linewidth=2, marker='x',markerfacecolor='red', markersize=6)
    ax2.plot(x1, y3d, color='blue', label="new G3 subscriber", linewidth=2, marker='o', markerfacecolor='blue',markersize=7)
    ax2.plot(x1, y6d, color='blue', label="handoff G3 subscriber", linestyle='dashed', linewidth=2, marker='x',markerfacecolor='blue', markersize=7)

    # setting x and y axis range
    ax2.set_xlim(1, 5.5 )
    ax2.set_ylim(0 , 1)

    # naming the x axis
    ax2.set_xlabel('Call Departure Rate')
    # naming the y axis
    ax2.set_ylabel('Blocking/Dropping Probability')

    # giving a title to my graph
    ax2.set_title('Data call blocking/dropping probability Vs Departure Rate' )

    # function to show the plot
    ax1.legend(loc='best')
    ax2.legend(loc='best')
    plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
