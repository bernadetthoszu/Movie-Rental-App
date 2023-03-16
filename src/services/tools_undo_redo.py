class Call:
    """"
    Objectifies a function call... Its fields are function_name and *function_params (a list of some parameters, depending on function_name)
    Its method 'call' puts together the function name and the parameters and executes the function call.
    """
    def __init__(self, function_name, *function_params): #function_name + other parameters
        self._function_name = function_name
        self._function_params = function_params #list (packed them)

    def call(self):
        # print(*self._function_params)
        # print(self._function_name)
        self._function_name(*self._function_params)

class Operation:
    """"
    Objectifies an operation... Its fields are undo_call (function_name(*function_parameters)) and redo_call (function_name(*function_parameters))
    Its methods undo and redo call the functions stored in undo_call and redo_call of type Call
    """
    def __init__(self, undo_call, redo_call):
        self._undo_call = undo_call
        self._redo_call = redo_call

    def undo(self):
        self._undo_call.call()

    def redo(self):
        self._redo_call.call()

class CascadedOperation:
    """"
    Sister of the class Operation...
    The difference is that Operation refers strictly to the operation which has to be undone/redone
         while CascadedOperation applies undo/redo to the operation which are bound in some ways to
         the operation of type Operation (if we remove a client, we must remove also his/her rentals.txt,
         if we undo the removal, we must add back his/her rentals.txt too)
    """
    def __init__(self):
        self._operations = []

    def add(self, operation):
        self._operations.append(operation)

    def undo(self):
        for op in self._operations:
            op.undo()

    def redo(self):
        for op in self._operations:
            op.redo()