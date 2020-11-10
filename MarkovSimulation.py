import numpy as np
import math
from RATs import RATattributes
from RATs import Services
from RATs import RATloads


def MarkovSimulator(i):
    print()
    print(" Voice Simulator Running  ...")

    # **** Create RAT Networks and the different service class ****
    RAT1 = RATattributes(1, 5, 3)  # RATattributes( rid, capacity, threshold):
    RAT2 = RATattributes(2, 7, 4)
    RAT3 = RATattributes(3, 9, 5)

    voice = Services("voice", 1, 1)  # Services( name, sid, bbu):
    data = Services("data", 2, 2)

    ratesR1 = RATloads(1, 6, 6, 6, 6, i, i, i, i )  # RATloads(rid, arvNewvoice,arvNewdata, arvHandoffvoice,arvHandoffdata,depNewvoice,depNewdata,depHandoffvoice,depHandoffdata) *In __calls/min*
    ratesR2 = RATloads(2, 6, 6, 6, 6, i, i, i, i )
    ratesR3 = RATloads(3, 6, 6, 6, 6, i, i, i, i )

    RAT1load = ratesR1.RATload()  # calculate loading for each RAT of class-i and returns [self.rid,PnewVc, PhandoffVc,PnewDt,PhandoffDt ]
    RAT2load = ratesR2.RATload()
    RAT3load = ratesR3.RATload()

    # **** The (2*J*K) dimensional vector state ****
    J = 3  # Number of RATs
    K = 2  # Number of service classes
    dimension = J * K  # dimension of a state

    # **** Create array to store the states ****
    global Gv
    Gv =Gd = Hstv = Hstv1 = Hstv2 = Hstv3 = 0
    HstblckR1v = HstblckR1d =0  # storing markov values for blocking and dropping states
    HstdropR1v = HstdropR1d =0
    HstblckR2v = HstblckR2d =0
    HstdropR2v = HstdropR2d =0
    HstblckR3v = HstblckR3d =0
    HstdropR3v = HstdropR3d = 0
    UR1 = UR2 = UR3 = 0

    state = [0] * dimension
    admstatev = []
    admstated = []

    #for voice calls
    blckstateR1v = []
    blckstateR2v = []
    blckstateR3v = []

    drpstateR1v = []
    drpstateR2v = []
    drpstateR3v = []

    #for Data calls
    blckstateR1d = []
    blckstateR2d = []
    blckstateR3d = []

    drpstateR1d = []
    drpstateR2d = []
    drpstateR3d = []

#*************** class-1: VOICE SERVICES ****************************#

    # ************ Admissible states & MArkov Simulation  & Call Blocking and Dropping Probabilitues*************#
    for nR3v in range(RAT3.capacity + 1):
        for mR3v in range(RAT3.threshold + 1):
            for nR2v in range(RAT2.capacity + 1):
                for mR2v in range(RAT2.threshold +1):
                    for nR1v in range(RAT1.capacity + 1):
                        for mR1v in range(RAT1.threshold + 1):

                            # ********  Markov Process   ****************#

                            # finding all aadmmisible states
                            if (mR1v * voice.bbu <= RAT1.threshold and (mR1v + nR1v) * voice.bbu <= RAT1.capacity) and \
                                    ( mR2v*voice.bbu <= RAT2.threshold and (mR2v + nR2v)*voice.bbu <= RAT2.capacity )  and \
                                    ( mR3v * voice.bbu <= RAT3.threshold and (mR3v + nR3v) * voice.bbu <= RAT3.capacity):

                                #markov process
                                # RATload valuses [self.rid, PnewVc, PhandoffVc, PnewDt, PhandoffDt]
                                Hstv = (pow(RAT1load[1], mR1v) * pow(RAT1load[2], nR1v)) / ( math.factorial(mR1v) * math.factorial(nR1v)) *\
                                 (pow(RAT2load[1], mR2v) * pow(RAT2load[2], nR2v)) / ( math.factorial(mR2v) * math.factorial(nR2v)) *\
                               (pow(RAT3load[1], mR3v) * pow(RAT3load[2], nR3v)) / (math.factorial(mR3v) * math.factorial(nR3v))

                                # calculation of the G normilisation constant
                                Gv = Gv + Hstv  # Normalisation factor: addition of each state probability
                                #print("GV  ", Gv)
                                #print(" HSTV ", Hstv, " HSTBLCK", HstblckR1v)

                                # ******** admissible state for voice in RAT 1 ****************#
                                if mR1v*voice.bbu <= RAT1.threshold and (mR1v + nR1v)*voice.bbu <= RAT1.capacity:
                                    state[0] = mR1v
                                    state[1] = nR1

                                    # blocking states for RAT1
                                    if voice.bbu + mR1v * voice.bbu > RAT1.threshold or (voice.bbu + (mR1v + nR1v) * voice.bbu) > RAT1.capacity :
                                        if state not in blckstateR1v:
                                            HstblckR1v = HstblckR1v + Hstv  # computional Markov equations
                                            blckstateR1v.append(state[:])

                                    # Dropping states for RAT 1
                                    if (voice.bbu + (mR1v + nR1v) * voice.bbu) > RAT1.capacity:
                                        if state not in drpstateR1v:
                                            HstdropR1v = HstdropR1v + Hstv # computional Markov equations
                                            drpstateR1v.append(state[:])


                                    #network Utilisation
                                    UR1 = UR1 + ((mR1v*voice.bbu + nR1v*voice.bbu)*Hstv)


                                # ******** admissible state for voice in RAT 2 ****************#
                                if mR2v*voice.bbu <= RAT2.threshold and (mR2v + nR2v)*voice.bbu <= RAT2.capacity:
                                    state[2] = mR2v
                                    state[3] = nR2v

                                    # blocking states for RAT2 must be here
                                    if (state in blckstateR1v) and \
                                        ((voice.bbu + mR2v * voice.bbu) > RAT2.threshold or (voice.bbu + (mR2v + nR2v) * voice.bbu)  > RAT2.capacity):
                                        if state not in blckstateR2v:
                                            HstblckR2v = HstblckR2v + Hstv  # computional Markov equations
                                            blckstateR2v.append(state[:])

                                    # dropping states for RAT2
                                    if (state in drpstateR1v) and (voice.bbu + (mR2v + nR2v) * voice.bbu) > RAT2.capacity:
                                        if state not in drpstateR2v:
                                            HstdropR2v = HstdropR2v + Hstv  # computional Markov equations
                                            drpstateR2v.append(state[:])


                                    # network Utilisation
                                    UR2 = UR2 + ((mR2v * voice.bbu + nR2v * voice.bbu)*Hstv)

                                # ******** admissible state for voice in RAT 3 ****************#
                                if mR3v * voice.bbu <= RAT3.threshold and (mR3v + nR3v) * voice.bbu <= RAT3.capacity:
                                    state[4] = mR3v
                                    state[5] = nR3v

                                    # blocking states for RAT 3 must be here
                                    if (state in blckstateR2v) and (state in blckstateR1v) and \
                                        ((voice.bbu + mR3v * voice.bbu) > RAT3.threshold or (voice.bbu + (mR3v + nR3v) * voice.bbu) > RAT3.capacity):
                                        if state not in blckstateR3v:
                                            HstblckR3v = HstblckR3v + Hstv  # computional Markov equations
                                            blckstateR3v.append(state[:])

                                    # Dropping states for RAT 3
                                    if (state in drpstateR2v) and (state in drpstateR1v) and (voice.bbu + (mR3v + nR3v) * voice.bbu) > RAT3.capacity:
                                        if state not in drpstateR3v:
                                            HstdropR3v = HstdropR3v + Hstv  # computional Markov equations
                                            drpstateR3v.append(state[:])

                                    # network Utilisation
                                    UR3 = UR3 + ((mR3v * voice.bbu + nR3v * voice.bbu) * Hstv)

                                #print(state)
                                #print(RAT1load)
                                # checking if state is already found
                                if state not in admstatev:
                                    admstatev.append(state[:])


    #************** Class-1: Voice probabilities *********************#
    NCBP1v =HstblckR1v / Gv
    NCBP2v = HstblckR2v / Gv
    NCBP3v = HstblckR3v / Gv

    HCDP1v = HstdropR1v / Gv
    HCDP2v = HstdropR2v / Gv
    HCDP3v = HstdropR3v / Gv

    addmissiblestatesv = np.array(admstatev)
    # print( addmissiblestates, iii )
    print("******************************* Class-1: Voice **********************************")
    print()
    print(len(admstatev))
    print("Admissible: ", addmissiblestatesv.size, "  blocking RAT 1:  ", len(blckstateR1v), "   blocking RAT 2:  ",
          len(blckstateR2v), "  blocking RAT 3:  ", len(blckstateR3v))
    print("Admissible: ", addmissiblestatesv.size, "  Dropping RAT 1:  ", len(drpstateR1v), "   Dropping RAT 2:  ",
          len(drpstateR2v), "  Dropping RAT 3:  ", len(drpstateR3v))
    print()
    print(" RAT 1 New Call Blocking Probability: ", NCBP1v)
    print(" RAT 2 New Call Blocking Probability: ", NCBP2v)
    print(" RAT 3 New Call Blocking Probability: ", NCBP3v)
    print()
    print(" RAT 1 HandOff Call Dropping Probability: ", HCDP1v )
    print(" RAT 2 HandOff Call Dropping Probability: ", HCDP2v)
    print(" RAT 3 HandOff Call Dropping Probability: ", HCDP3v)
    print()

# ******************** class-1: END ***********************************#






# *************** class-2: DATA SERVICES ****************************#
    print()
    print(" Data Simulator Running  ...")

    # ************ Admissible states & MArkov Simulation  & Call Blocking and Dropping Probabilities*************#
    for nR3d in range(RAT3.capacity + 1):
        for mR3d in range(RAT3.threshold + 1):
            for nR2d in range(RAT2.capacity + 1):
                for mR2d in range(RAT2.threshold + 1):
                    for nR1d in range(RAT1.capacity + 1):
                        for mR1d in range(RAT1.threshold + 1):

                            #finding all the admissible states
                            if (mR1d * data.bbu <= RAT1.threshold and (mR1d + nR1d) * data.bbu <= RAT1.capacity) and \
                            (mR2d * data.bbu <= RAT2.threshold and (mR2d + nR2d) * data.bbu <= RAT2.capacity) and \
                            (mR3d * data.bbu <= RAT3.threshold and (mR3d + nR3d) * voice.bbu <= RAT3.capacity):

                                # ***************  Markov Process ***************** #
                                # RATload valuses [self.rid, PnewVc, PhandoffVc, PnewDt, PhandoffDt]
                                Hstd = (pow(RAT1load[3], mR1d) * pow(RAT1load[4], nR1d)) / (math.factorial(mR1d) * math.factorial(nR1d)) * \
                                       (pow(RAT2load[3], mR2d) * pow(RAT2load[4], nR2d)) / (math.factorial(mR2d) * math.factorial(nR2d)) * \
                                       (pow(RAT3load[3], mR3d) * pow(RAT3load[4], nR3d)) / (math.factorial(mR3d) * math.factorial(nR3d))

                                Gd = Gd + Hstd # Normalisation factor: addition of each state probability


                                # ******** admissible state for data calls in RAT 1 **************** #
                                if mR1d * data.bbu <= RAT1.threshold and (mR1d + nR1d) * data.bbu <= RAT1.capacity:
                                    state[0] = mR1d
                                    state[1] = nR1d

                                    # network Utilisation
                                    UR1 = UR1 + ((mR1d * data.bbu + nR1d* data.bbu) * Hstd)

                                    # blocking states for RAT1 must be here
                                    if data.bbu + mR1d * data.bbu > RAT1.threshold or (data.bbu + (mR1d + nR1d) * data.bbu) > RAT1.capacity:
                                        if state not in blckstateR1d:
                                            HstblckR1d = HstblckR1d + Hstd  # computional Markov equations
                                            blckstateR1d.append(state[:])
                                            #print(" RAT 1: Blk-D", state)

                                    # Dropping state for RAT1
                                    if (data.bbu + (mR1d + nR1d) * data.bbu) > RAT1.capacity:
                                        if state not in drpstateR1d:
                                            HstdropR1d = HstdropR1d + Hstd  # computional Markov equations
                                            drpstateR1d.append(state[:])
                                            #print(" RAT 1: Drp-D", state)

                                # ******** admissible state for data in RAT 2 **************** #
                                if mR2d * data.bbu <= RAT2.threshold and (mR2d + nR2d) * data.bbu <= RAT2.capacity:
                                    state[2] = mR2d
                                    state[3] = nR2d

                                    # network Utilisation
                                    UR2 = UR2 + ((mR2d* data.bbu + nR2d * data.bbu)*Hstd)

                                    # blocking states for RAT2 must be here
                                    if (state in blckstateR1d) and ((data.bbu + mR2d * data.bbu ) > RAT2.threshold or (data.bbu + (mR2d + nR2d) * data.bbu) > RAT2.capacity):
                                        if state not in blckstateR2d:
                                            HstblckR2d = HstblckR2d + Hstd  # computional Markov equations
                                            blckstateR2d.append(state[:])
                                            #print(" RAT 2 Blocking-D: ", state)

                                    # dropping states for RAT2
                                    if (state in drpstateR1d) and (data.bbu +(mR2d + nR2d) * data.bbu) > RAT2.capacity:
                                        if state not in drpstateR2d:
                                            HstdropR2d = HstdropR2d + Hstd  # computional Markov equations
                                            drpstateR2d.append(state[:])
                                           # print(" RAT 2 Dropping: ", state)

                                # ******** admissible state for data in RAT 3 **************** #
                                if mR3d * data.bbu <= RAT3.threshold and (mR3d + nR3d) * voice.bbu <= RAT3.capacity:
                                    state[4] = mR3d
                                    state[5] = nR3d

                                    # network Utilisation
                                    UR3 = UR3 + ((mR3d* data.bbu + nR3d* data.bbu)*Hstd)

                                    # blocking states for RAT 3 must be here
                                    if (state in blckstateR2d) and (state in blckstateR1d) and ((data.bbu + mR3d * data.bbu ) > RAT3.threshold or (data.bbu + (mR3d + nR3d) * data.bbu) > RAT3.capacity):
                                        if state not in blckstateR3d:
                                            HstblckR3d = HstblckR3d + Hstd  # computional Markov equations
                                            blckstateR3d.append(state[:])
                                            #print(" RAT 3 Blocking State-D: ", state)

                                    # Dropping states for RAT 3
                                    if (state in drpstateR2d) and (state in drpstateR1d) and (data.bbu + (mR3d + nR3d) * data.bbu) > RAT3.capacity:
                                        if state not in drpstateR3d:
                                            HstdropR3d = HstdropR3d + Hstd  # computional Markov equations
                                            drpstateR3d.append(state[:])
                                            #print(" RAT 3 Dropping State-D: ", state)

                                # checking if state is already found
                                if state not in admstated:
                                    admstated.append(state[:])

    # ************** Class-1: Voice probabilities *********************#
    NCBP1d = HstblckR1d / Gd
    NCBP2d = HstblckR2d / Gd
    NCBP3d = HstblckR3d / Gd

    HCDP1d = HstdropR1d / Gd
    HCDP2d = HstdropR2d / Gd
    HCDP3d = HstdropR3d / Gd

    addmissiblestatesd = np.array(admstated)
    # print( addmissiblestates, iii )
    print("******************************* Class-2: Data **********************************")
    print()
    print(len(admstated))
    print("Admissible:-D ", addmissiblestatesd.size, "  blocking RAT 1-D:  ", len(blckstateR1d), "   blocking RAT 2-D:  ", len(blckstateR2d), "  blocking RAT 3-D:  ", len(blckstateR3d))
    print("Admissible: ", addmissiblestatesd.size, "  Dropping RAT 1:  ", len(drpstateR1d), "   Dropping RAT 2:  ", len(drpstateR2d), "  Dropping RAT 3:  ", len(drpstateR3d))
    print()
    print(" RAT 1 New Call Blocking Probability: ", NCBP1d)
    print(" RAT 2 New Call Blocking Probability: ", NCBP2d)
    print(" RAT 3 New Call Blocking Probability: ", NCBP3d)
    print()
    print(" RAT 1 HandOff Call Dropping Probability: ", HCDP1d)
    print(" RAT 2 HandOff Call Dropping Probability: ", HCDP2d)
    print(" RAT 3 HandOff Call Dropping Probability: ", HCDP3d)

    UHWN = UR1 + UR2 + UR3
    normalisedUR1 = UR1/(UHWN + Gd + Gv)
    normalisedUR2 = UR2 /(UHWN + Gd + Gv)
    normalisedUR3 = UR3 / (UHWN + Gd + Gv)

    #return [normalisedUR1, normalisedUR2, normalisedUR3, UHWN]
    return [NCBP1v, NCBP2v ,NCBP3v, HCDP1v, HCDP2v, HCDP3v, NCBP1d,  NCBP2d, NCBP3d,HCDP1d, HCDP2d, HCDP3d ]
# ******************** class-1: END *********************************** #


