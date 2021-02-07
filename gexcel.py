import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import uuid

class ExcelBase(object):
    def __init__(self, ):
        scope = ["https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("./config/creds.json", scope)
        self.__client = gspread.authorize(creds)
        
    def ongoingTotal(self,shrange = None, *args, **kwargs):
        if 'sheet' not in kwargs:
            sheet = self.__client.open("youngmaker-little-helper").worksheet("最新課程資訊")  # Open the spreadhseet
        else:
            sheet = kwargs['sheet']
        if not shrange:
            shrange = {"week": ["4","33"], "camp": ["36", "65"], "stripe":["68", "97"]}
    
        week_name, week_intro, week_url = sheet.batch_get(['C4:C33','L4:L33', 'P4:P33'])
        camp_name, camp_intro, camp_url = sheet.batch_get(['C36:C65','L36:L65', 'P36:P65'])
        stripe_name, stripe_intro, stripe_url = sheet.batch_get(['C68:C97','L68:L97', 'P68:P97'])
        weekend = [{'{CLASSNAME}':name[0], '{CLASSINTRO}':intro[0],'{COVERURL}': url[0] }for name, intro, url in zip(week_name, week_intro, week_url)]
        camp = [{'{CLASSNAME}':name[0], '{CLASSINTRO}':intro[0],'{COVERURL}':url[0] } for name, intro, url in zip(camp_name, camp_intro, camp_url)]
        stripe = [{'{CLASSNAME}':name[0], '{CLASSINTRO}':intro[0],'{COVERURL}':url[0]} for name, intro, url in zip(stripe_name, stripe_intro, stripe_url)]
        return {'weekend':weekend, 'camp':camp, 'stripe':stripe}
    
    def ongoingWeek(self, shrange=None, *args, **kwargs):
        if 'sheet' not in kwargs:
            sheet = self.__client.open("youngmaker-little-helper").worksheet("最新課程資訊")  # Open the spreadhseet
        else:
            sheet = kwargs['sheet']
        if not shrange:
            shrange = ["4","33"]
        week_name, week_intro, week_url = sheet.batch_get([f'C{shrange[0]}:C{shrange[1]}',
                                                           f'L{shrange[0]}:L{shrange[1]}', 
                                                           f'P{shrange[0]}:P{shrange[1]}'])
        return [{'{CLASSNAME}':name[0], '{CLASSINTRO}':intro[0],'{COVERURL}': url[0] }for name, intro, url in zip(week_name, week_intro, week_url)]

    def ongoingCamp(self, shrange=None, *args, **kwargs):
        if 'sheet' not in kwargs:
            sheet = self.__client.open("youngmaker-little-helper").worksheet("最新課程資訊")  # Open the spreadhseet
        else:
            sheet = kwargs['sheet']
        if not shrange:
            shrange = ["36", "65"]
        camp_name, camp_intro, camp_url = sheet.batch_get([f'C{shrange[0]}:C{shrange[1]}',
                                                           f'L{shrange[0]}:L{shrange[1]}', 
                                                           f'P{shrange[0]}:P{shrange[1]}'])
        return [{'{CLASSNAME}':name[0], '{CLASSINTRO}':intro[0],'{COVERURL}': url[0] }for name, intro, url in zip(camp_name, camp_intro, camp_url)]
    
    def ongoingStripe(self, shrange=None, *args, **kwargs):
        if 'sheet' not in kwargs:
            sheet = self.__client.open("youngmaker-little-helper").worksheet("最新課程資訊")  # Open the spreadhseet
        else:
            sheet = kwargs['sheet']
        if not shrange:
            shrange = ["68", "97"]
        stripe_name, stripe_intro, stripe_url = sheet.batch_get([f'C{shrange[0]}:C{shrange[1]}',
                                                                 f'L{shrange[0]}:L{shrange[1]}',
                                                                 f'P{shrange[0]}:P{shrange[1]}'])
        return [{'{CLASSNAME}':name[0], '{CLASSINTRO}':intro[0],'{COVERURL}': url[0] }for name, intro, url in zip(stripe_name, stripe_intro, stripe_url)]
    
    def historyTotal(self,):
        sheet = self.__client.open("youngmaker-little-helper").worksheet("歷史課程資訊")  # Open the spreadhseet
        #load from boto3.
        stripe, weekend, camp = sheet.batch_get(['A3:C1000', 'D3:F1000', 'G3:I1000'])
        weekend = [{'name':w[0], 'date':w[1], 'photos': w[2].split('\n')} for w in weekend]
        camp = [{'name': c[0], 'date': c[1], 'photos' : c[2].split('\n')} for c in camp]
        stripe = [{'name': s[0], 'date': s[1], 'photos' : s[2].split('\n')} for s in stripe]
        return {'weekend':weekend, 'camp':camp, 'stripe':stripe}
    
    def newClass(self,):
        sheet = self.__client.open("youngmaker-little-helper").worksheet("最新課程資訊")
        week_addr = self.__newClassCheck(sheet, "week")
        camp_addr = self.__newClassCheck(sheet, "camp")
        stripe_addr = self.__newClassCheck(sheet, "stripe")
        # Do update.
        week = self.__newClassFill(sheet, "week", week_addr) if week_addr else None
        camp = self.__newClassFill(sheet, "camp", camp_addr) if camp_addr else None
        stripe = self.__newClassFill(sheet, "stripe", stripe_addr) if stripe_addr else None
        return {"week":week,"camp":camp, "stripe":stripe}
    
    def __newClassCheck(self, sheet, classLabel):
        if classLabel == 'week':
            base_shrange = "A4:B33"
        elif classLabel == 'camp':
            base_shrange = "A36:B65"
        elif classLabel == 'stripe':
            base_shrange  = "A68:B97"
        new_list= []
        lock = True
        for idx, r in enumerate(sheet.range(base_shrange)):
            if idx %2 == 1 and r.value == "":
                lock = False
            elif not lock:
                new_list.pop(-1)
                break
            elif idx%2 == 0 and r.value == '':
                new_list.append(r.address)

        return new_list
    
    def __newClassFill(self, sheet, classLabel, addr):
        newId = [[str(uuid.uuid4())] for _ in addr]
        shrange = [addr[0][1:], addr[-1][1:]]
        sheet.update(":".join( [addr[0], addr[-1]] ), newId)
        if classLabel == 'week':
            return [ dict(d,**{'{ID}': nid[0]}) for d, nid in zip(self.ongoingWeek(shrange, sheet = sheet), newId) ]
        elif classLabel == 'camp':
            return [ dict(d, **{'{ID}': nid[0]}) for d, nid in zip(self.ongoingCamp(shrange, sheet = sheet), newId) ]
        elif classLabel == 'stripe':
            return [ dict(d, **{'{ID}': nid[0]}) for d, nid in zip(self.ongoingStripe(shrange, sheet = sheet), newId) ]
    
    def historyUpdate(self,):
        pass
    
    
# pprint(ExcelBase().ongoing_camp())
# pprint(ExcelBase().ongoing_total())
# pprint(ExcelBase().newClass())