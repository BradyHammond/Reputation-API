# ================================================== #
#                      STORAGE                       #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 12/02/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

import os
import shelve

# ================================================== #
#                  CLASS DEFINITIONS                 #
# ================================================== #


# Define Data object
class Data(object):

    # Define init function
    def __init__(self, mode):
        # Crate a variable to hold the database
        self.db = None
        self.mode = mode

    # ============================================= #

    # Define function to close open
    def open(self):
        directory = os.path.dirname(__file__)
        # Check mode and open corresponding database
        if self.mode == "Production":
            file = os.path.join(directory, 'data.db')
            self.db = shelve.open(file)
        else:
            file = os.path.join(directory, 'test_data.db')
            self.db = shelve.open(file)

    # ============================================= #

    # Define function to clear database
    def clear(self):
        self.db.clear()

    # ============================================= #

    # Define function to close database
    def close(self):
        # Close the database
        self.db.close()


# ================================================== #
#                        EOF                         #
# ================================================== #
