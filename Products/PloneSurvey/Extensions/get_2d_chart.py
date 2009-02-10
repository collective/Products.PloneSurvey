'''
Call this method on a SurveyTwoDimensional instance. Draws a two
dimensional graph with a point for each answer.
'''
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.axes import YValueAxis
from reportlab.graphics.shapes import Drawing, Group, String, Rect
from reportlab.lib import colors
from reportlab.graphics.widgets.markers import makeMarker 
from reportlab.graphics.widgets.grids import DoubleGrid, Grid
from reportlab.graphics.charts.legends import Legend, LineLegend
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.widgetbase import Widget

class StringWidget(Widget):
    """
    This class fits into the Legend plugin architecture. 
    This class is extensible, so we can add coloured text
    in future.
    """
    def __init__(self, msg, fontName='Helvetica', fontSize=12):
        self.msg = str(msg)
        self.fontName = fontName
        self.fontSize = fontSize
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def draw(self):
        g = Group()
        # 0.718 is for Helvetica. xxx: needs work for other fonts
        g.add(String(self.x, self.y+1-0.718, self.msg, fontSize=self.fontSize, fontName=self.fontName))
        return g
     
def setupGrid(lineplot):
        """This code from ReportLab lineplots.py"""
        sel = lineplot
        xva, yva = sel.xValueAxis, sel.yValueAxis
        if xva: xva.joinAxis = yva
        if yva: yva.joinAxis = xva

        yva.setPosition(sel.x, sel.y, sel.height)
        yva.configure(sel.data)

        # if zero is in chart, put x axis there, otherwise
        # use bottom.
        xAxisCrossesAt = yva.scale(0)
        if ((xAxisCrossesAt > sel.y + sel.height) or (xAxisCrossesAt < sel.y)):
            y = sel.y
        else:
            y = xAxisCrossesAt

        xva.setPosition(sel.x, y, sel.width)
        xva.configure(sel.data)

        back = sel.background
        if isinstance(back, Grid):
            if back.orientation == 'vertical' and xva._tickValues:
                xpos = map(xva.scale, [xva._valueMin] + xva._tickValues)
                steps = []
                for i in range(len(xpos)-1):
                    steps.append(xpos[i+1] - xpos[i])
                back.deltaSteps = steps
            elif back.orientation == 'horizontal' and yva._tickValues:
                ypos = map(yva.scale, [yva._valueMin] + yva._tickValues)
                steps = []
                for i in range(len(ypos)-1):
                    steps.append(ypos[i+1] - ypos[i])
                back.deltaSteps = steps
        elif isinstance(back, DoubleGrid):
            # Ideally, these lines would not be needed...
            back.grid0.x = sel.x
            back.grid0.y = sel.y
            back.grid0.width = sel.width
            back.grid0.height = sel.height
            back.grid1.x = sel.x
            back.grid1.y = sel.y
            back.grid1.width = sel.width
            back.grid1.height = sel.height

            # some room left for optimization...
            if back.grid0.orientation == 'vertical' and xva._tickValues:
                xpos = map(xva.scale, [xva._valueMin] + xva._tickValues)
                steps = []
                for i in range(len(xpos)-1):
                    steps.append(xpos[i+1] - xpos[i])
                back.grid0.deltaSteps = steps
            elif back.grid0.orientation == 'horizontal' and yva._tickValues:
                ypos = map(yva.scale, [yva._valueMin] + yva._tickValues)
                steps = []
                for i in range(len(ypos)-1):
                    steps.append(ypos[i+1] - ypos[i])
                back.grid0.deltaSteps = steps
            if back.grid1.orientation == 'vertical' and xva._tickValues:
                xpos = map(xva.scale, [xva._valueMin] + xva._tickValues)
                steps = []
                for i in range(len(xpos)-1):
                    steps.append(xpos[i+1] - xpos[i])
                back.grid1.deltaSteps = steps
            elif back.grid1.orientation == 'horizontal' and yva._tickValues:
                ypos = map(yva.scale, [yva._valueMin] + yva._tickValues)
                steps = []
                for i in range(len(ypos)-1):
                    steps.append(ypos[i+1] - ypos[i])
                back.grid1.deltaSteps = steps

def run(self):
    def weight_sort(a, b):
        return cmp(a.getWeight(), b.getWeight())
        
    drawing = Drawing(600, 300)
    lc = LinePlot()
     
    # Determine axis dimensions and create data set
    maxval = 0
    minval = 0    
    dimension_one_values = []
    dimension_two_values = []
    dimension_one_answeroptions_as_objects = []
    dimension_two_answeroptions_as_objects = []
    counter = 0
    for question in self.getQuestions():        
        weights = [int(weight) for weight in question.getAnswerOptionsWeights()]
        answeroptions = list(question.getAnswerOptions())

        # This is used by the legend. Sort on weight.
        if counter == 0:
            dimension_one_answeroptions_as_objects = question.getAnswerOptionsAsObjects()
            dimension_one_answeroptions_as_objects.sort(weight_sort)
        else:
            dimension_two_answeroptions_as_objects = question.getAnswerOptionsAsObjects()
            dimension_two_answeroptions_as_objects.sort(weight_sort)

        # Minmax
        lmin = min(weights)
        lmax = max(weights)
        if lmin < minval:
            minval = lmin
        if lmax > maxval:
            maxval = lmax
        
        # Data
        for user, answer in question.answers.items():
            value = answer.get('value', None)            
            weight = None
            if value is not None:                
                # Lookup the integer weight of this answer
                if value in answeroptions:
                    index = answeroptions.index(value)
                    weight = weights[index]
            # Always add to the list. ReportLab deals with None.    
            if counter == 0:
                dimension_one_values.append(weight)
            else:
                dimension_two_values.append(weight)
                
        counter += 1

    # Set minmax
    absmax = max(abs(minval), abs(maxval)) * 1.1    
    lc.xValueAxis.valueMin = -absmax
    lc.xValueAxis.valueMax = absmax    
    lc.yValueAxis.valueMin = -absmax
    lc.yValueAxis.valueMax = absmax
       
    # Zip to create data
    data = [zip(dimension_one_values, dimension_two_values)]
    if not len(data[0]):
        return
    
    lc.x = 0
    lc.y = 0
    # Misc setup
    lc.height = 300
    lc.width = 300
    lc.data = data
    lc.joinedLines = 0
    lc.fillColor = None
    lc.lines[0].strokeColor = colors.red
    lc.lines[0].symbol = makeMarker('FilledCircle')

    # Add a grid
    grid = DoubleGrid()
    lc.background = grid
    setupGrid(lc)    
    lc.background = None
    # Finetune the grid
    grid.grid0.strokeWidth = 0.2
    grid.grid1.strokeWidth = 0.2
    # Add to drawing else it overwrites the center Y axis
    drawing.add(grid)
   
    # Add a Y axis to pass through the origin
    yaxis = YValueAxis()
    yaxis.setPosition(lc.width/2, 0, lc.height)
    yaxis.configure([(0,-absmax),(0,absmax)])
    yaxis.strokeColor = colors.blue
    drawing.add(yaxis)

    # Color X-Axis
    lc.xValueAxis.strokeColor = colors.green

    drawing.add(lc)

    # Legend for Dimension One
    drawing.add(String(lc.width+20, lc.height-12, 'Dimension One (X-Axis):', 
        fontName='Helvetica', fontSize=12, fillColor=colors.green))
    legend = Legend()
    legend.alignment = 'right'
    legend.x = lc.width + 20
    legend.y = lc.height - 20
    legend.fontName = 'Helvetica'
    legend.fontSize = 12
    legend.columnMaximum = 7
    items = []
    for ob in dimension_one_answeroptions_as_objects:
        items.append( ( StringWidget(ob.getWeight()), ob() ) )
    legend.colorNamePairs = items
    drawing.add(legend, 'legend1')

    # Legend for Dimension Two
    drawing.add(String(lc.width+20, lc.height/2-12, 'Dimension Two (Y-Axis):', 
        fontName='Helvetica', fontSize=12, fillColor=colors.blue))
    legend = Legend()
    legend.alignment = 'right'
    legend.x = lc.width + 20
    legend.y = lc.height/2 - 20
    legend.fontName = 'Helvetica'
    legend.fontSize = 12
    legend.columnMaximum = 7
    items = []
    for ob in dimension_two_answeroptions_as_objects:
        items.append( ( StringWidget(ob.getWeight()), ob() ) )
    legend.colorNamePairs = items
    drawing.add(legend, 'legend2')

    # Write out
    data = drawing.asString('png')
    request = self.REQUEST
    response = request.RESPONSE
    response.setHeader('Content-Type', 'image/png')
    response.setHeader('Content-Disposition','inline; filename=%s.png' % self.getId())
    response.setHeader('Content-Length', len(data))           
    response.setHeader('Cache-Control', 's-maxage=0')
    
    return data
