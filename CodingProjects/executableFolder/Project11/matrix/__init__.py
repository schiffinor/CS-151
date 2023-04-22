'''
__init__.py
Roman Schiffino 151B Fall Semester

This is a pretty basic class I created. It basically just lets me store 
data in the form of a 2d array or in other words a matrix. Basically wrote 
this to make my life a little easier.
'''

class matData:
    '''
    Matrix data-type class. Creates a custom data type with a couple custom
    functions. These allow for some utility that really helps with the data.
    '''
    
    def __init__(self, rowCount, columnCount, data=None):
        '''
        Initiates the data set. If no data is provided an empty matrix will be created.
        '''
        rowList = []
        # Define .rows and .columns attributes.
        self.rows = rowCount
        self.columns = columnCount
        if data is None:
            for curRow in range(self.rows):
                # Creates list which contains the current row.
                colList = []
                for curCol in range(self.columns):
                    # Populates list.
                    colList.append(data)
                # Appends row to list of rows.
                rowList.append(colList)
            # Creates matrix from list.
            self.load = rowList
        if data is not None:
            # Passes data to make matrix.
            self.load = data


    def __str__(self):
        '''
        When a function calls for a string representation of the matrix this function provides a string representation of the matrix.
        '''
        rows = self.rows
        cols = self.columns
        output = ""
        for x in range(rows):
            output += str(self.load[x])+"\n"
        return output


    def get(self, x, y):
        '''
        Returns value of matrix at row x, column y.
        '''
        return self.load[x][y]


    def set(self, x, y, val):
        '''
        Sets value of matrix at row x, column y to value.
        '''
        self.load[x][y] = val
    

    def setAll(self, val):
        '''
        
        '''
        data = [[int(val)]*self.columns]*self.rows
        self.load = data

    
    def rAppend(self, other):
        '''
        Constructs a matrix where every unit of matrix other is appended to the right of the matrix self.
        '''
        newMatrix = matData(int(self.rows), int(self.columns + other.columns))
        for x in range(int(self.rows)):
            for y in range(int(self.columns + other.columns)):
                if y < self.columns:
                    newMatrix.set(x, y, self.get(x, y))
                else:
                    newMatrix.set(x, y, other.get(x-self.columns, y-self.columns))
        return newMatrix
                

    def lAppend(self, other):
        '''
        Constructs a matrix where every unit of matrix other is appended to the left of the matrix self.
        '''
        newMatrix = matData(int(self.rows), int(self.columns + other.columns))
        for x in range(newMatrix.rows):
            for y in range(newMatrix.columns):
                if y < self.columns:
                    newMatrix.set(x, y, other.get(x, y))
                else:
                    newMatrix.set(x, y, self.get(x-self.columns, y-self.columns))
        return newMatrix


    def uAppend(self, other):
        '''
        Constructs a matrix where every unit of matrix other is appended above the matrix self.
        '''
        newMatrix = matData(int(self.rows + other.rows), int(self.columns))
        for x in range(newMatrix.rows):
            for y in range(newMatrix.columns):
                if x < self.rows:
                    newMatrix.set(x, y, other.get(x, y))
                else:
                    newMatrix.set(x, y, self.get(x-self.rows, y-self.rows))
        return newMatrix


    def dAppend(self, other):
        '''
        Constructs a matrix where every unit of matrix other is appended below the matrix self.
        '''
        newMatrix = matData(int(self.rows + other.rows), int(self.columns))
        for x in range(newMatrix.rows):
            for y in range(newMatrix.columns):
                if x < self.rows:
                    newMatrix.set(x, y, self.get(x, y))
                else:
                    newMatrix.set(x, y, other.get(x-self.rows, y-self.rows))
        return newMatrix
    

    def __mul__(self,other):
        '''
        New function, matrix multiplication.
        '''
        newMatrix = matData(int(self.rows),int(other.columns))
        for x in range(newMatrix.rows):
            for y in range(newMatrix.columns):
                listRow = self.load[x]
                listColumn = [other.get(i,y) for i in range(other.rows)]
                listMult = [listRow[i]*listColumn[i] for i in range(len(listColumn))]
                value = sum(listMult)
                newMatrix.set(x,y,value)
        return newMatrix
    

    def __add__(self,other):
        '''
        New function, matrix addition.
        '''
        newMatrix = matData(int(self.rows),int(self.columns))
        for x in range(newMatrix.rows):
            for y in range(newMatrix.columns):
                value = self.get(x,y)+other.get(x,y)
                newMatrix.set(x,y,value)
        return newMatrix