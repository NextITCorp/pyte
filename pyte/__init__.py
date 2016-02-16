"""
pyTE - python temporal expression module
Temporal expressions are simple predicate functions that let 
you evaluate a 'schedule' to determine which actual dates apply 
to the schedule.  The system allows one to compose a tree of 
temporal expressions into a new temopral expression to provide 
complex schedule structures (e.g., workdays during the month, 
        the first and third Tuesday of each month, or 
        weekend days excluding the summer months).

This library also includes some extensions for dates to generate 
a list of dates.  this can be used with a TE to restrict a list to 
conform to the requirements of the predicate, excluding dates from 
the list that do not conform.

All the dates used with this library must be utc or the functions 
will raise exceptions.
"""
__all__=['DateExtensions','TemporalExpressions']
