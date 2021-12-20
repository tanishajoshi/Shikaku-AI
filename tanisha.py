from ShikakuSolver import *
class PartiallySolvedPuzzle:
    def __init__(self, board, options):
        self.board = board
        self.options = options

class tanisha(ShikakuSolver):
    def __init__(self, problem, maxTime, visualizer):
        ShikakuSolver.__init__(self, problem, maxTime, visualizer)

    def solve(self):

        # Setup the possible options
        options = {}
        for i in range(self._problem.numRegions()):

            # Build all possible rectangles of the correct size and add them to
            # the options for that region.  Note there are much better ways
            # to do this.
            size = self._problem.getRegionSize(i)
            rectangles = []

            initRow = self._problem.getRegionOrigin(i)[0]
            initCol = self._problem.getRegionOrigin(i)[1]

            for height in range(1, size+1):
                if size % height == 0:
                    width = size // height
                    for row in range(0, self._problem.size() - height+1):
                        for col in range(0, self._problem.size() - width+1):
                            rows = {r : r for r in range(row, row+height)}
                            columns = {c : c for c in range(col, col+width)}
                            if initRow in rows and initCol in columns:
                                rectangles.append((row, col, height, width))

            options[i] = rectangles

        # Place options in descendding order
        options = { a[0] : a[1] for a in sorted(options.items(), key = lambda i : self._problem.getRegionSize(i[0]), reverse=True) }

        root = PartiallySolvedPuzzle(copy.copy(self._problem._known), options)

        if self._visualizer:
            self._visualizer.draw(root.board)

        if self._problem.isGoal(root.board):  # We found the solution
            return root.board

        solution = self.backtrack(root)
        if solution is not None:
            return solution.board
        return None  # Time is out, return nothing

    def backtrack(self, state):
        if not self.timeRemaining():
            return None

        if self._problem.isGoal(state.board):  # We found the solution
            return state

        if self._visualizer:
            self._visualizer.draw(state.board, state.options)

        if (len(state.options) == 0):
            return None

        # Choose an region to fix
        regionId = self.reOrder(state)
        regionOptions = state.options.pop(regionId)
        self._numExpansions += 1

        for rectangle in regionOptions:
            # Check if this choice is consistent with selections
            # that have already been made.  It is consistent if every
            # square has either the region id or -1 in it.
            consistent = numpy.all(numpy.logical_or(state.board == -1, state.board == regionId)[rectangle[0]:rectangle[0]+rectangle[2], rectangle[1]:rectangle[1]+rectangle[3]])

            if consistent:
                newState = copy.deepcopy(state)
                for row in range(rectangle[0], rectangle[0]+rectangle[2]):
                    for col in range(rectangle[1], rectangle[1]+rectangle[3]):
                        newState.board[row, col] = regionId

                # Adding inference after filling in squares
                self.inferMove(newState)

                if self._visualizer:
                    self._visualizer.draw(newState.board)
                solution = self.backtrack(newState)
                if solution is not None:
                    return solution
                self._backTracks += 1

        return None

    def inferMove(self, state):
        inference = False
        regionNos = list(state.options.keys())
        for rNo in regionNos:
            choices = []
            rectangles = state.options[rNo]
            for r in rectangles:
                consistent = numpy.all(numpy.logical_or(state.board == -1, state.board == rNo)[r[0]:r[0]+r[2], r[1]:r[1]+r[3]])
                if (consistent):
                    choices.append(r)

            state.options[rNo] = choices
            choicelen = len(choices)

            if (choicelen == 0):
                return

            if (choicelen == 1):
                inference = True
                r = choices[0]
                state.options.pop(rNo)

                for row in range(r[0], r[0]+r[2]):
                    for col in range(r[1], r[1]+r[3]):
                        state.board[row, col] = rNo

        if inference:
            return self.inferMove(state)

    def sortRegions(self, items):
        length = len(items[1])
        pos = 0
        initRow = self._problem.getRegionOrigin(items[0])[0]
        initCol = self._problem.getRegionOrigin(items[0])[1]
        if (initCol == 0 or initRow == 1):
            pos = 1

        if (length == 0):
            return (0, pos, self._problem.getRegionSize(items[0]))
        else:
            return (length* -1, pos, self._problem.getRegionSize(items[0]))

    def reOrder(self, state):
        total = self._problem.numRegions()
        remainingOption = len(state.options)
        if total == remainingOption:
            keys = list(state.options.keys())
            return keys[0]
        sortedRegions = sorted(state.options.items(), key = lambda x : self.sortRegions(x), reverse=True)

        return sortedRegions[0][0]
