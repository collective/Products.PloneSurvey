'''
Call this method on a Survey instance. 
Draws a (stacked) barchart with average scores per dimension.
'''
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, Group, String, Rect
from reportlab.lib import colors
from reportlab.graphics.widgets.markers import makeMarker 
from reportlab.graphics.charts.legends import Legend, LineLegend
from reportlab.graphics.charts.textlabels import Label

def run(self, include_sub_survey=False, dimensions=[]):

    # Build data set
    averages = []
    category_names = []
    
    for dimension in self.getDimensions():
        averages.append(self.get_average_score_for_dimension(
            include_sub_survey=include_sub_survey,
            dimension=dimension))
        category_names.append(dimension)
        
    drawing = Drawing(600, 300)
    
    bc = VerticalBarChart()         
    bc.x = 20
    bc.y = 20  
    bc.height = 260
    bc.width = 580
    bc.data = [averages]
    bc.categoryAxis.categoryNames = category_names
    bc.categoryAxis.labels.fontName = 'Helvetica'
    bc.categoryAxis.labels.fontSize = 10
    bc.categoryAxis.labels.textAnchor = 'middle'
    bc.categoryAxis.visibleTicks = 0
    bc.valueAxis.valueMax = 100.0
    bc.valueAxis.valueMin = min(averages, 0)
    bc.valueAxis.labels.fontName = 'Helvetica'
    bc.valueAxis.labels.fontSize = 10
    bc.valueAxis.labels.textAnchor = 'middle'
    bc.barLabelFormat = '%.0f'
    bc.barLabels.dy = 8
    bc.barLabels.fontName = 'Helvetica'
    bc.barLabels.fontSize = 10
    bc.barWidth = len(averages)
    bc.fillColor = None

    drawing.add(bc)
    
    # Write out
    data = drawing.asString('png')
    request = self.REQUEST
    response = request.RESPONSE
    response.setHeader('Content-Type', 'image/png')
    response.setHeader('Content-Disposition','inline; filename=%s.png' % self.getId())
    response.setHeader('Content-Length', len(data))           
    response.setHeader('Cache-Control', 's-maxage=0')
    
    return data
