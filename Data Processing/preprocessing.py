

def featureExtraction(xlst,cond):

    """
       Description:

           The following is the feature extraction which was used.

       Input Args:

           xlist        =  The data             (np.array),
           cond         =  Conditional          (string)

    """


    featData = []

    for lst in xlst:
        # The following are all the features which were examined. Not all of them are used.
        raw_signal = lst
        average    = float(np.mean(lst))
        variance   = float(np.var(lst))
        abs_chang  = float(np.mean([abs(lst[i] - lst[i-1]) for i in range(1, len(lst))]))
        maximum    = float(np.max(lst))
        minimum    = float(np.min(lst))
        range_mm   = float(maximum - minimum)

        if  cond ==  "":
           featData.append("<Enter desired features>")

        elif  cond ==  "":
           featData.append("<Enter desired features>")

        elif cond ==  "":
           featData.append("<Enter desired features>")

        elif cond ==  "":
           featData.append("<Enter desired features>")

        else: print("Error during feature extraction"

    return featData

