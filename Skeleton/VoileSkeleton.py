#TODO change name
from shapely.geometry import Polygon

from Geometry.Geom2D import Poly, Pnt
from Skeleton.BoxSkeleton import BoxSkeleton
# from Skeleton.WallSkeleton import WallSkeleton


class VoileSkeleton(BoxSkeleton):

    def __init__(self,parent,start,end):
        self.parentWall = parent
        self.start = start
        self.end = end
        poly = self.getPolyFromStartEnd(start,end)
        super(VoileSkeleton, self).__init__(poly)
        self.pointsList = None
        self.isPointValid = None

    def setParentWall(self,wallSkeleton):
        self.parentWall = wallSkeleton

    def getPolyFromStartEnd(self,start,end):
        parent = self.parentWall
        length = end - start
        newLengthVec = parent.vecLength.copy().resize(length)
        move = start
        moveVec = parent.vecLength.copy()
        moveVec.resize(move)
        topLeftPnt = parent.topLeftPnt + moveVec
        newWidthVec = parent.vecWidth.copy()
        pnt1 = topLeftPnt + newWidthVec
        pnt2 = pnt1 + newLengthVec
        pnt3 = topLeftPnt + newLengthVec
        poly = Poly([topLeftPnt, pnt1, pnt2, pnt3])
        return poly

    def getLength(self):
        return self.end - self.start

    def getLengthX(self):
        return abs(self.vecLength.x())

    def getLengthY(self):
        return abs(self.vecLength.y())

    def copy(self):
        voile = VoileSkeleton(self.parentWall,self.start,self.end)
        voile.evalData = self.evalData
        return voile

    def getStartPoint(self):
        return self.topLeftPnt

    def getEndPoint(self):
        return self.topLeftPnt + self.vecLength

    # def startIsValid(self):
    #     self.isStartValid = True
    #
    # def endIsValid(self):
    #     self.isEndValid = True

    def getPointsList(self):
        if not self.pointsList:
            self.pointsList = [self.getStartPoint(),self.getEndPoint()]
            self.isPointValid = [False for p in self.pointsList]
        return self.pointsList

    def setPointValid(self,index):
        self.isPointValid[index] = True

    def getSurrondingBox(self):
        distance = 4
        wid = Pnt(self.vecLength.y(),-self.vecLength.x())
        wid = wid.copy().resize(distance)*2 + wid.copy().resize(self.vecWidth.magn())
        leng = self.vecLength.copy().resize(distance)*2 + self.vecLength
        center = self.topLeftPnt + self.vecLength/2 + self.vecWidth/2
        pnts = []
        pnts.append(center - leng/2 - wid/2)
        pnts.append(pnts[0] + leng)
        pnts.append(pnts[1] + wid)
        pnts.append(pnts[0] + wid)
        polyPnts = [[pnt.x(),pnt.y()] for pnt in pnts]
        return Polygon(polyPnts)