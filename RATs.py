class RATattributes:
    def __init__(self, rid, capacity, threshold):
        # initiate class attributes
        self.rid = rid
        self.capacity = capacity
        self.threshold = threshold


class Services:
    def __init__(self, name, sid, bbu):
        # initiate class attributes
        self.name = name
        self.sid = sid
        self.bbu = bbu


class RATloads:
    def __init__(self, rid, arvNewvoice,arvNewdata, arvHandoffvoice,arvHandoffdata,depNewvoice,depNewdata,depHandoffvoice,depHandoffdata):
        # initiate class attributes
        self.rid = rid
        self.arvNewvoice= arvNewvoice
        self.arvNewdata = arvNewdata
        self.arvHandoffvoice = arvHandoffvoice
        self.arvHandoffdata = arvHandoffdata
        self.depNewvoice = depNewvoice
        self.depNewdata = depNewdata
        self.depHandoffvoice = depHandoffvoice
        self.depHandoffdata = depHandoffdata

    def RATload(self):
        PnewVc = (self.arvNewvoice/self.depNewvoice)
        PhandoffVc = (self.arvHandoffvoice/self.depHandoffvoice)
        PnewDt = (self.arvNewdata / self.depNewdata)
        PhandoffDt =  (self.arvHandoffdata/self.depHandoffdata)
        return [self.rid,PnewVc, PhandoffVc,PnewDt,PhandoffDt ]