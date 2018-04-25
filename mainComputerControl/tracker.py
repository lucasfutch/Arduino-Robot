import tuio

class Tracker(object):

    def __init__(self):
        self.tracking = tuio.Tracking()
        self.tracker = None

    def update(self):
        self.tracking.update()

    def get_heading(self, fiducial):
        for obj in self.tracking.objects():
            if (obj.id == fiducial):
                return obj.angle

    def get_pos(self, fiducial):
        for obj in self.tracking.objects():
            if (obj.id == fiducial):
                return [obj.xpos, obj.ypos]
