import arcpy,math

#Вхідний клас даних
infc=r"Path to feature class"
#Довжина бергштриха
length=60

#Пряма та обернена геодезична задача
def pointCalc(x,y,kut,l):
    xn=x+l*math.sin(math.radians(kut))
    yn=y+l*math.cos(math.radians(kut))
    return arcpy.Point(xn,yn)

def NA_1(point1,point2):
    degBearing=math.degrees(math.atan2((point2.X - point1.X),(point2.Y - point1.Y)))
    if (degBearing < 0):
        degBearing += 360.0
    return degBearing

#Операції по зміні довжини бергштриха
curs=arcpy.da.UpdateCursor(infc,["SHAPE@"])
for row in curs:
    kut=NA_1(row[0].firstPoint,row[0].lastPoint)
    point1=row[0].firstPoint
    point2=pointCalc(row[0].firstPoint.X,row[0].firstPoint.Y,kut,length)
    polyline=arcpy.Polyline(arcpy.Array([point1,point2]))
    row[0]=polyline
    curs.updateRow(row)
curs.reset()
