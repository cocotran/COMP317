# CMPT 145: Abstract Data Types
# Defines the Statistics ADT
# Calculate mean and variance.

# Implementation
# Do the calculations without storing all the data!
# Uses a dictionary as a record to store three quantities:
#   'count':     the number of data values added
#   'avg':       the running average of the values added
#   'sumsqdiff': the sum of the square differences between the 
#                values added and the mean so far
# These values can be modified every time a new data value is 
# added, so that the mean and variance can be calculated quickly  
# as needed.  This approach means that we do not need to store  
# the data values themselves, which could save a lot of space.

class Statistics(object):

    def __init__(self):
        """
        Purpose:
            Create a Statistics object.
        """
        self.__count = 0      # how many data values have been seen
        self.__avg = 0        # the running average so far
        self.__sumsqdiff = 0  # the sum of the square differences
        self.__min = None
        self.__max = None

    def add(self, value):
        """
        Purpose:
            Use the given value in the calculation of statistics.
        Pre-Conditions:
            value: the value to be added
        Post-Conditions:
            none
        Return:
            none
        """
        self.__count += 1
        k = self.__count           # convenience
        diff = value - self.__avg  # convenience
        self.__avg += diff/k
        self.__sumsqdiff += ((k-1)/k)*(diff**2)
        
        if self.__max is None or self.__max < value:
            self.__max = value
    
        if self.__min is None or self.__min > value:
            self.__min = value

    def mean(self):
        """
        Purpose:
            Return the mean of all the values seen so far.
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Return:
            The mean of the data seen so far.
            Note: if no data has been seen, 0 is returned.
                  This is clearly false.
        """
        return self.__avg


    def min(self):
        """
        Purpose:
            Return the minimum of all the values seen so far.
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Return:
            The minimum of the data seen so far.
            Note: if no data has been seen, None is returned.
        """
        return self.__min

    def max(self):
        """
        Purpose:
            Return the maximum of all the values seen so far.
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Return:
            The maximum of the data seen so far.
            Note: if no data has been seen, None is returned.
        """
        return self.__max
 
    def count(self):
        """
        Purpose:
            Return the number of all the values seen so far.
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Return:
            The number of the data seen so far.
            Note: if no data has been seen, 0 is returned.
        """
        return self.__count

       
    def var(self):
        """
        Purpose:
            Return the variance of all the values seen so far.
            (variance is the average of the squared difference
            between each value and the average of all values)
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Return:
            The variance of the data seen so far.
            Note: if 0 or 1 data values have been seen, 0 is returned.
                  This is clearly false.
        """
        return self.__sumsqdiff/self.__count


    def sample_var(self):
        """
        Purpose:
            Return the sample variance of all the values seen so far.
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Return:
            The sample variance of the data seen so far.
            Note: if 0 or 1 data values have been seen, 0 is returned.
                  This is clearly false.
        """
        return self.__sumsqdiff/(self.__count - 1)



