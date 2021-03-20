#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

def constructVariableArray(board):
  result = []
  totalRows = len(board)
  domain = [0, 1, 2, 3, 4, 5, 6, 7, 8 ,9]
  for row in range(totalRows):
    variableRowList = []
    for column in range(10):
      if (board[row][column] != -1):
        value = board[row][column]
        variable = Variable("Row " + str(row) + " Column " + str(column), [value]) # Change to current?
        variable.assign(value)
      else:
        variable = Variable("Row " + str(row) + " Column " + str(column), domain)
      variableRowList.append(variable)

    result.append(variableRowList)
  
  return result

def getSatisfiedTuplesList(current, compareVariable):
  result = []
  for checkTuple in itertools.product(current.domain(), compareVariable.domain()):
    if (checkTuple[0] != checkTuple[1]):
      result.append(checkTuple)
  return result

def getAdjDiaRowConstraintsModel1(constraintList, totalRows, cspVariableList):
  for row in range(totalRows):
    for column in range(10):
      current = cspVariableList[row][column]
      # Check top constraint
      adjacentContraints(row, cspVariableList, column, current, constraintList)
      for index in range(column + 1, 10):
        current = cspVariableList[row][column]
        compareVariable = cspVariableList[row][index]
        constraint = Constraint("RowConstraint {},{}|{},{}".format(row, column, row, index), [current, compareVariable])
        satisfiedTuplesList = getSatisfiedTuplesList(current, compareVariable)
        constraint.add_satisfying_tuples(satisfiedTuplesList)
        constraintList.append(constraint)

def adjacentContraints(row, cspVariableList, column, current, constraintList):
  # Careful of overlaps
  # If checking bottom, no need to check top
  # If checking bottom - right, no need to check top - left
  # If checking bottom - left, no need to check top - right
  # If checking top, no need to check bottom
  # If checking top - right, no need to check bottom - left
  # If checking top - left, no need to check bottom - right
  if (row != 0):
    compareVariable = cspVariableList[row - 1][column]
    constraint = Constraint("TopAdj {},{}|{},{}".format(row, column, row-1, column), [current, compareVariable])
    satisfiedTuplesList = getSatisfiedTuplesList(current, compareVariable)
    constraint.add_satisfying_tuples(satisfiedTuplesList)
    constraintList.append(constraint)

  # Check topRight Constraint
  if (row != 0 and column != 9):
    compareVariable = cspVariableList[row - 1][column + 1]
    constraint = Constraint("TopRight {},{}|{},{}".format(row, column, row-1, column+1), [current, compareVariable])
    satisfiedTuplesList = getSatisfiedTuplesList(current, compareVariable)
    constraint.add_satisfying_tuples(satisfiedTuplesList)
    constraintList.append(constraint)

  # Check topLeft Constraint
  if (row != 0 and column != 0):
    compareVariable = cspVariableList[row - 1][column - 1]
    constraint = Constraint("topLeft {},{}|{},{}".format(row, column, row-1, column-1), [current, compareVariable])
    satisfiedTuplesList = getSatisfiedTuplesList(current, compareVariable)
    constraint.add_satisfying_tuples(satisfiedTuplesList)
    constraintList.append(constraint)
  
        
  # #Check Bottom constarint
  # if (row != totalRows - 1):
  #   compareVariable = cspVariableList[row + 1][column]
  #   constraint = Constraint("BottomAdj {},{}|{},{}".format(row, column, row+1, column), [current, compareVariable])
  #   satisfiedTuplesList = getSatisfiedTuplesList(current, compareVariable)
  #   constraint.add_satisfying_tuples(satisfiedTuplesList)
  #   constraintList.append(constraint)


  # # Check BottomLeft Constraint
  # if (row != totalRows - 1 and column != 0):
  #   compareVariable = cspVariableList[row + 1][column - 1]
  #   constraint = Constraint("BottomLeft {},{}|{},{}".format(row, column, row+1, column-1), [current, compareVariable])
  #   satisfiedTuplesList = getSatisfiedTuplesList(current, compareVariable)
  #   constraint.add_satisfying_tuples(satisfiedTuplesList)
  #   constraintList.append(constraint)

  # # Check BottomRight Constraint
  # if (row != totalRows - 1 and column != 9):
  #   compareVariable = cspVariableList[row + 1][column + 1]
  #   constraint = Constraint("BottomRight {},{}|{},{}".format(row, column, row+1, column+1), [current, compareVariable])
  #   satisfiedTuplesList = getSatisfiedTuplesList(current, compareVariable)
  #   constraint.add_satisfying_tuples(satisfiedTuplesList)
  #   constraintList.append(constraint)

def getColumnConstraints(constraintList, board, sumRow):
  for column in range(10):
    columnVariablesDomain = []
    columnVariables = []
    for row in range(len(board)):
      variable = board[row][column]
      columnVariablesDomain.append(variable.cur_domain())
      columnVariables.append(variable)
    constraint = Constraint("ColumnConstrant {}".format(column), columnVariables)
    validTupleList = []
    for product in itertools.product(*columnVariablesDomain):
      if (sum(product) == sumRow[column]):
        validTupleList.append(product)
    constraint.add_satisfying_tuples(validTupleList)
    constraintList.append(constraint)

def getAllVariables(board):

  result = []
  totalRows = len(board)
  for row in range(totalRows):
    for column in range(10):
      result.append(board[row][column])
  
  return result

def addConstraintsToCsp(constraintList, csp):
  for constraint in constraintList:
    csp.add_constraint(constraint)

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''

    varriableBoard = constructVariableArray(initial_tenner_board[0])
    constraintList = []
    ## Adding constraints to tennerModel
    getAdjDiaRowConstraintsModel1(constraintList, len(varriableBoard), varriableBoard)
    getColumnConstraints(constraintList, varriableBoard, initial_tenner_board[1])

    allVariableList = getAllVariables(varriableBoard)
    tennerModel = CSP("TennerModel1", allVariableList)

    addConstraintsToCsp(constraintList, tennerModel)


    return tennerModel, varriableBoard

def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

      However, model_2 has different constraints. In particular, instead
       of binary non-equals constaints model_2 has a combination of n-nary 
       all-different constraints: all-different constraints for the variables in
       each row, and sum constraints for each column. You may use binary 
       contstraints to encode contiguous cells (including diagonally contiguous 
       cells), however. Each -ary constraint is over more 
       than two variables (some of these variables will have
       a single value in their domain). model_2 should create these
       all-different constraints between the relevant variables.
    '''
    varriableBoard = constructVariableArray(initial_tenner_board[0])
    constraintList = []
    ## Adding constraints to tennerModel
    getAdjDiaRowConstraintsModel1(constraintList, len(varriableBoard), varriableBoard)
    getColumnConstraints(constraintList, varriableBoard, initial_tenner_board[1])

    allVariableList = getAllVariables(varriableBoard)
    tennerModel = CSP("TennerModel2", allVariableList)

    addConstraintsToCsp(constraintList, tennerModel)


    return None, None
