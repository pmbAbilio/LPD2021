from sys import flags

from geoip2.records import Location
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import HorizontalBarChart, VerticalBarChart
import geoip2.database
import subprocess
import re
from databasefiles.main import DataBaseFiles

styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']
flowables = []
#TA_LEFT, TA_CENTER or TA_CENTRE, TA_RIGHT and TA_JUSTIFY
styles.add(ParagraphStyle(name='Normal_CENTER',
                          parent=styles['Normal'],
                          fontName='Helvetica',
                          wordWrap='LTR',
                          alignment=TA_CENTER,
                          fontSize=20,
                          leading=13,
                          textColor=colors.black,
                          borderPadding=0,
                          leftIndent=0,
                          rightIndent=0,
                          spaceAfter=0,
                          spaceBefore=0,
                          splitLongWords=True,
                          spaceShrinkage=0.05,
                          ))
logtypes = ['SSH','UFW','APACHE']
class reportgenerator:

    PDF_NAME = 'Report.pdf'
    REPORT_HEADER = 'Log File(s) Analisys'
    conn = None
    DATA_TYPE = ''
    LOGDATA = []
    IP_RE = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    flowables=[]
    NORMALIZED_DATA = {}

    def __init__(self, conn, logtype):
        self.conn = conn
        self.DATA_TYPE = logtype
        
        doc = SimpleDocTemplate(
            self.PDF_NAME,
            pagesize=A4,
            bottomMargin=.4 * inch,
            topMargin=.6 * inch,
            rightMargin=.8 * inch,
            leftMargin=.8 * inch)
        """ with open("your_text_file.txt", "r") as txt_file:
            text_content = txt_file.read() """
        logo = "report/logo.png"
        im = Image(logo, 1 * inch, 1 * inch)
        im.hAlign = 'LEFT'
        self.flowables.append(im)
        self.flowables.append(Spacer(1, 18))
        P = Paragraph(self.REPORT_HEADER,  styles['Normal_CENTER'])
        self.flowables.append(P)
        self.flowables.append(Spacer(1, 1*inch))

        if logtype == 1:
            for i in logtypes:
                self.DATA_TYPE = i
                self.drawTable()
                self.drawPlots()
        else:
            self.drawTable()
            self.drawPlots()
        

        doc.build(
            self.flowables,
        )

    def getCountry(self, ip):
        reader = geoip2.database.Reader("GeoLiteFiles/GeoLite2-Country.mmdb")
        try:
            return str(reader.country(ip).country.name)
        except:
            output = ''
            try:
                output = subprocess.Popen(['host', ip], stdout=subprocess.PIPE).communicate()[0]
                ips = re.findall(self.IP_RE, output.decode('iso-8859-1'))
                
                if len(ips) > 0:
                    return str(reader.country(ips[0]).country.name)
                else: return []    
            except Exception as e:
                print(e)
                return []

    def drawTable(self):
        table = ''
        tableheader = []
        if self.DATA_TYPE == 'SSH':
            table = 'sshdata'
            tableheader = ['Ip','Date','User','Location','Attempts']
        elif self.DATA_TYPE == 'UFW':
            table = 'ufwdata'
            tableheader = ['Ip','Date','Location','Attempts']
        elif self.DATA_TYPE == 'APACHE':
            table = 'apachedata'
            tableheader = ['Ip','Date','Location','Attempts']
        filter = {"table" : table, "atribute" : 1}
        
        self.LOGDATA = DataBaseFiles.selectdata(self.conn,filter)
        print(self.LOGDATA)
        ips = {}
        for line in self.LOGDATA:
            if line[1] != '':
                if line[1] not in ips:
                    loc = self.getCountry(line[1])
                    if loc != None and len(loc) > 0:
                        if self.DATA_TYPE == 'SSH':
                            ips[line[1]] = {"attempts" : 1, "location" : loc, "first_seen": line[2], "user": line[3]}
                        elif self.DATA_TYPE == 'UFW':
                            ips[line[1]] = {"attempts" : 1, "location" : loc, "first_seen": line[2]}
                        elif self.DATA_TYPE == 'APACHE':
                            ips[line[1]] = {"attempts" : 1, "location" : loc, "first_seen": line[2]}
                    elif len(loc) == 0:
                        if self.DATA_TYPE == 'SSH':
                            ips[line[1]] = {"attempts" : 1, "location" : 'Not Found', "first_seen": line[2], "user": line[3]}   
                        elif self.DATA_TYPE == 'UFW':
                            ips[line[1]] = {"attempts" : 1, "location" : 'Not Found', "first_seen": line[2]} 
                        elif self.DATA_TYPE == 'APACHE':
                            ips[line[1]] = {"attempts" : 1, "location" : loc, "first_seen": line[2]}
                else:
                    for ip in ips:
                        if line[1] == ip:
                            ips[ip]["attempts"] += 1
        
        self.NORMALIZED_DATA = ips
            
        tabledata= [tableheader]
        for i in ips:
            if self.DATA_TYPE == 'SSH':
                tabledata.append([i, ips[i]["first_seen"], ips[i]["user"], ips[i]["location"], ips[i]["attempts"]])
            elif self.DATA_TYPE == 'UFW':
                tabledata.append([i, ips[i]["first_seen"], ips[i]["location"], ips[i]["attempts"]])
            elif self.DATA_TYPE == 'APACHE':
                tabledata.append([i, ips[i]["first_seen"], ips[i]["location"], ips[i]["attempts"]])
        #print(tabledata)
        t=Table(tabledata,len(tableheader)*[1.5*inch], (len(ips)+1)*[0.4*inch])
        t.setStyle(TableStyle([
        ('ALIGN',(0,(len(ips)+1)),(0,(len(ips)+1)),'CENTER'),
        ('VALIGN',(0,(len(ips)+1)),(0,(len(ips)+1)),'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))
        P = Paragraph('The following ips were found on the {} log file'.format(self.DATA_TYPE),  styles['Normal_CENTER'])
        self.flowables.append(P)
        self.flowables.append(Spacer(20, 0.5*inch))
        self.flowables.append(t)
        self.flowables.append(Spacer(20, 0.5*inch))
        

    def drawPlots(self):
        
        P = Paragraph('The following ips were found on the {} log file'.format(self.DATA_TYPE),  styles['Normal_CENTER'])
        self.flowables.append(P)
        self.flowables.append(Spacer(20, 1*inch))
        
        
        data = []
        values = ()
        names = []
        new_data = []

        renormalized = {}

        for l in self.NORMALIZED_DATA:
            new_data.append(self.NORMALIZED_DATA[l]['location'])
        new_data = list(set(new_data))

        for loc in new_data:
            for t in self.NORMALIZED_DATA:
                if self.NORMALIZED_DATA[t]['location'] == loc:
                    if loc in renormalized:
                        renormalized[loc] += int(self.NORMALIZED_DATA[t]['attempts'])
                    else: 
                        renormalized[loc] = int(self.NORMALIZED_DATA[t]['attempts'])

        for line in renormalized:
            values += (renormalized[line],)
            names.append(line)
        data.append(values)

        print(max(values))

        
        spacing = 0
        height = 0
        width = 0
        step = 0
        maxvalue = 0
        if max(values) > 1000:
            spacing = 0
            height = 500
            step = 150
            maxvalue = max(values)
        elif max(values) < 1000 and max(values) > 500:
            spacing = 0
            height = 400
            step = 100
            maxvalue = 1000
        elif max(values) < 500 and max(values) > 250:
            spacing = 0
            height = 300
            step = 50
            maxvalue = 500
        elif max(values) < 250 and max(values) > 100:
            spacing = 0
            height = 200
            step = 25
            maxvalue = 250
        elif max(values) < 100 and max(values) > 50:
            spacing = 0
            height = 100
            step = 10
            maxvalue = 100
        elif max(values) < 50 and max(values) > 10:
            spacing = 0
            height = 50
            step = 5
            maxvalue = 50
        elif max(values) < 10:
            spacing = 0
            height = 25
            step = 1
            maxvalue = 10

        drawing = Drawing(400, height)

        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 0
        bc.height = height
        bc.width = 400
        bc.data = data
        bc.strokeColor = colors.white
        bc.valueAxis.valueMin = spacing
        bc.valueAxis.valueMax = maxvalue
        bc.valueAxis.valueStep = step
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = -5
        bc.categoryAxis.labels.angle = 90
        bc.categoryAxis.labels.fontName = 'Helvetica'
        bc.categoryAxis.categoryNames = names

        drawing.add(bc)
        self.flowables.append(drawing)
        self.flowables.append(Spacer(20, 1*inch))
        
                