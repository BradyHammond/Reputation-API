# ================================================== #
#                     PROCESSOR                      #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 12/04/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #


from app.storage.storage import Data


# ================================================== #
#                  CLASS DEFINITIONS                 #
# ================================================== #


# Define processor object
class Processor(object):

    # Define init function
    def __init__(self, reputee, mode):
        # Store the queried reputee
        self.reputee = reputee
        self.mode = mode

    # ============================================= #

    # Define function to get reach, clarity, and clout
    def get_all(self):
        # Calculate reach, clarity, and clout
        reach = self.get_reach()
        clarity = self.get_clarity()
        clout = self.get_clout(clarity, reach)

        # Return calculated values
        return [clout, reach, clarity]

    # ============================================= #

    # Define function to get reach
    def get_reach(self):
        # Open database
        data = Data(self.mode)
        data.open()
        # Initialize a list
        reach_list = []

        # Loop through the database and append to list any entries matching queried reputee
        for key in data.db:
            if data.db[key]['reputee'] == self.reputee:
                if data.db[key]['repute']['feature'] == "reach":
                    reach_list.append(data.db[key]['repute']['value'])

        # Close database
        data.close()

        # Calculate score
        if len(reach_list) == 0:
            score = 0
        else:
            score = sum(reach_list)/len(reach_list)
        # Calculate confidence
        confidence = self.s_function(2, 6, len(reach_list))

        # Return calculated values
        return (score, confidence)

    # ============================================= #

    # Define function to get clarity
    def get_clarity(self):
        # Open database
        data = Data(self.mode)
        data.open()
        # Initialize a list
        clarity_list = []

        # Loop through the database and append to list any entries matching queried reputee
        for key in data.db:
            if data.db[key]['reputee'] == self.reputee:
                if data.db[key]['repute']['feature'] == "clarity":
                    clarity_list.append(data.db[key]['repute']['value'])
        # Close database
        data.close()

        # Calculate score
        if len(clarity_list) == 0:
            score = 0
        else:
            score = sum(clarity_list) / len(clarity_list)
        # Calculate confidence
        confidence = self.s_function(4, 8, len(clarity_list))

        # Return calculated values
        return (score, confidence)

    # ============================================= #

    # Define function to get clout
    def get_clout(self, reach, clarity):
        # Calculate weights
        reach_weight = reach[1]/(clarity[1] + reach[1])
        clarity_weight = clarity[1]/(clarity[1] + reach[1])
        # Normalize weights
        normalized_weight = (clarity_weight*clarity[0]) + (reach_weight*reach[0])
        score = normalized_weight/10
        # Calculate confidence
        confidence = min([clarity[1], reach[1]])

        # Return calculated values
        return(score, confidence)

    # ============================================= #

    # Define s function
    def s_function(self, a, b, x):
        # Piecewise function used to calculate confidence
        if x <= a:
            return 0
        elif a <= x <= ((a+b)/2):
            return 2*((x-a)/(b-a))**2
        elif ((a+b)/2) <= x <= b:
            return 1-2*((x-b)/(b-a))**2
        else:
            return 1


# ================================================== #
#                        EOF                         #
# ================================================== #
