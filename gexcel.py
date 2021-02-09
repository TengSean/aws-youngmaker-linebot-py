import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import uuid, itertools
from datetime import datetime, timedelta
import numpy as np
class ExcelBase(object):
    def __init__(self, ):
        scope = ["https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("./config/creds.json", scope)
        self.__client = gspread.authorize(creds)
        self.__ALBUMMAX = 1000
        self.__newClassSheet = '「最新課程資訊」的副本'
        self.__albumSheet = '課程相簿'
        
        
    def ongoingTotal(self,shrange = None, *args, **kwargs):
        '''
            return type:
                - weel: dict
                    - Id: str(uuid4)
                    - {CLASSTAG}: str
                    - {CLASSNAME}: str
                    - {CLASDATE}: str
                    - {CLASSTIME}: str
                    - {CLASSINTRO}': str
                    - {COVERURL}: str(URL)
        '''
        if 'sheet' not in kwargs:
            sheet = self.__client.open("youngmaker-little-helper").worksheet(self.__newClassSheet)  # Open the spreadhseet
        else:
            sheet = kwargs['sheet']
        if 'row_shrange' not in kwargs:
            row_shrange = {"week": ["4","33"], "camp": ["36", "65"], "stripe":["68", "97"]}
        week = self.ongoingWeek(sheet = sheet)
        camp = self.ongoingCamp(sheet = sheet)
        stripe = self.ongoingStripe(sheet = sheet)
        return {'week':week, 'camp':camp, 'stripe':stripe}
    
    def ongoingWeek(self, shrange=None, *args, **kwargs):
        '''
            回傳一個串列
            
            retrun type:
                - list
                    - Id: str(uuid4)
                    - {CLASSTAG}: str
                    - {CLASSNAME}: str
                    - {CLASDATE}: str
                    - {CLASSTIME}: str
                    - {CLASSINTRO}': str
                    - {COVERURL}: str(URL)
        '''
        if 'sheet' not in kwargs:
            sheet = self.__client.open("youngmaker-little-helper").worksheet(self.__newClassSheet)  # Open the spreadhseet
        else:
            sheet = kwargs['sheet']
        if 'row_shrange' not in kwargs:
            row_shrange = ["4","33"]
        else:
            row_shrange = kwargs['row_shrange']
        try:
            weeks = np.array(sheet.batch_get([
                                        f'B{row_shrange[0]}:B{row_shrange[1]}',
                                        f'C{row_shrange[0]}:C{row_shrange[1]}',
                                        f'F{row_shrange[0]}:F{row_shrange[1]}',
                                        f'G{row_shrange[0]}:G{row_shrange[1]}',
                                        f'L{row_shrange[0]}:L{row_shrange[1]}',
                                        f'P{row_shrange[0]}:P{row_shrange[1]}']))
            return [{'CLASSTAG}':w[0],'{CLASSNAME}':w[1],'{CLASSDATE}':w[2], '{CLASSTIME}':w[3], '{CLASSINTRO}':w[4], '{COVERURL}':w[5]}for week in np.transpose(weeks) for w in week]
        except:
            return []
            
    def ongoingCamp(self, shrange=None, *args, **kwargs):
        '''
            回傳一個串列
            
            retrun type:
                - list
                    - {CLASSTAG}: str
                    - {CLASSNAME}: str
                    - {CLASSDATE}: str
                    - {CLASSTIME}: str
                    - {CLASSINTRO}: str
                    - {CLASSURL}: str(URL)
        '''
        if 'sheet' not in kwargs:
            sheet = self.__client.open("youngmaker-little-helper").worksheet(self.__newClassSheet)  # Open the spreadhseet
        else:
            sheet = kwargs['sheet']
        if 'row_shrange' not in kwargs:
            row_shrange = ["36", "65"]
        else:
            row_shrange = kwargs['row_shrange']
        try:
            camps = np.array(sheet.batch_get([
                                        f'B{row_shrange[0]}:B{row_shrange[1]}',
                                        f'C{row_shrange[0]}:C{row_shrange[1]}',
                                        f'F{row_shrange[0]}:F{row_shrange[1]}',
                                        f'G{row_shrange[0]}:G{row_shrange[1]}',
                                        f'L{row_shrange[0]}:L{row_shrange[1]}',
                                        f'P{row_shrange[0]}:P{row_shrange[1]}']))
            return [{'CLASSTAG}':c[0],'{CLASSNAME}':c[1],'{CLASSDATE}':c[2], '{CLASSTIME}':c[3], '{CLASSINTRO}':c[4], '{COVERURL}':c[5]}for camp in np.transpose(camps) for c in camp]
        except:
            return []
        
    def ongoingStripe(self, shrange=None, *args, **kwargs):
        '''
            回傳一個串列
            
            retrun type:
                - list
                    - Id: str(uuid4)
                    - {CLASSTAG}: str
                    - {CLASSNAME}: str
                    - {CLASDATE}: str
                    - {CLASSTIME}: str
                    - {CLASSINTRO}': str
                    - {COVERURL}: str(URL)
        '''
        if 'sheet' not in kwargs:
            sheet = self.__client.open("youngmaker-little-helper").worksheet(self.__newClassSheet)  # Open the spreadhseet
        else:
            sheet = kwargs['sheet']
        if 'row_shrange' not in kwargs:
            row_shrange = ["68", "97"]
        else:
            row_shrange = kwargs['row_shrange']
        try:
            stripes = np.array(sheet.batch_get([
                                        f'B{row_shrange[0]}:B{row_shrange[1]}',
                                        f'C{row_shrange[0]}:C{row_shrange[1]}',
                                        f'F{row_shrange[0]}:F{row_shrange[1]}',
                                        f'G{row_shrange[0]}:G{row_shrange[1]}',
                                        f'L{row_shrange[0]}:L{row_shrange[1]}',
                                        f'P{row_shrange[0]}:P{row_shrange[1]}']))
            return [{'CLASSTAG}':s[0],'{CLASSNAME}':s[1],'{CLASSDATE}':s[2], '{CLASSTIME}':s[3], '{CLASSINTRO}':s[4], '{COVERURL}':s[5]}for stripe in np.transpose(stripes) for s in stripe]
        except:
            return []
        
    def albumTotal(self,):
        sheet = self.__client.open("youngmaker-little-helper").worksheet(self.__albumSheet)  # Open the spreadhseet
        #load from boto3.
        try:
            week, camp, stripe = self.albumWeek(sheet = sheet), self.albumCamp(sheet = sheet), self.albumStripe(sheet = sheet)
            print(week)
            week = [{'Id':w[0], '{CLASSTAG}':w[1], '{CLASSNAME}':w[2], '{CLASSDATE}':w[3], '{ALBUMHASH}': w[4]} for w in week if len(w) == 4] if week else []
            camp = [{'Id':c[0], '{CLASSTAG}':c[1], '{CLASSNAME}':c[2], '{CLASSDATE}':c[3], '{ALBUMHASH}': c[4]} for c in camp if len(c) == 4] if camp else []
            stripe = [{'Id':s[0], '{CLASSTAG}':s[1], '{CLASSNAME}':s[2], '{CLASSDATE}':s[3], '{ALBUMHASH}': s[4]} for s in stripe if len(s) == 4] if stripe else []
        except:
            week = []
            camp = []
            stripe = []
        return {'weekend':week, 'camp':camp, 'stripe':stripe}
    
    def albumWeek(self,*args, **kwargs):
        '''
            回傳一個串列
            
            retrun type:
                - list
                    - {Id}: str
                    - {CLASSTAG}: str
                    - {CLASSNAME}: str
                    - {CLASSDATE}: str(NOT isoformat)
                    - {ALBUMHASH}: str
        '''
        if 'sheet' not in kwargs:
            sheet = self.__client.open("youngmaker-little-helper").worksheet(self.__albumSheet)  # Open the spreadhseet
        else:
            sheet = kwargs['sheet']
        try:
            weekend = sheet.get(f"A4:E{self.__ALBUMMAX}")
            weekend = [{'Id':w[0], '{CLASSTAG}':w[1], '{CLASSNAME}':w[2], '{CLASSDATE}':w[3], '{ALBUMHASH}': w[4]} for w in weekend if len(w) == 5]
        except:
            weekend = []
        return weekend
    
    def albumCamp(self,*args, **kwargs):
        '''
            回傳一個串列
            
            retrun type:
                - list
                    - {Id}: str
                    - {CLASSTAG}: str
                    - {CLASSNAME}: str
                    - {CLASSDATE}: str(NOT isoformat)
                    - {ALBUMHASH}: str
        '''
        if 'sheet' not in kwargs:
            sheet = self.__client.open("youngmaker-little-helper").worksheet(self.__albumSheet)  # Open the spreadhseet
        else:
            sheet = kwargs['sheet']
        try:
            camp = sheet.get(f"F4:J{self.__ALBUMMAX}")
            camp = [{'Id':c[0], '{CLASSTAG}':c[1], '{CLASSNAME}':c[2], '{CLASSDATE}':c[3], '{ALBUMHASH}': c[4]} for c in camp if len(c) == 5 ]
        except:
            camp = []
        return camp
    
    def albumStripe(self,*args, **kwargs):
        '''
            回傳一個串列
            
            retrun type:
                - list
                    - {Id}: str
                    - {CLASSTAG}: str
                    - {CLASSNAME}: str
                    - {CLASSDATE}: str(NOT isoformat)
                    - {ALBUMHASH}: str
        '''
        if 'sheet' not in kwargs:
            sheet = self.__client.open("youngmaker-little-helper").worksheet(self.__albumSheet)  # Open the spreadhseet
        else:
            sheet = kwargs['sheet']
        try:
            stripe = sheet.get(f"K4:O{self.__ALBUMMAX}")
            stripe = [{'Id':s[0], '{CLASSTAG}':s[1], '{CLASSNAME}':s[2], '{CLASSDATE}':s[3], '{ALBUMHASH}': s[4]} for s in stripe if len(s) == 5 ]
        except:
            stripe = []
        return stripe
            
            
    def newClass(self,):
        '''
            回傳一串欲更新於dynamodb 的 list
            
            return type: 
                - list
                    - Id: str(uuid4)
                    - {CLASSTAG}: str
                    - {CLASSNAME}: str
                    - {CLASDATE}: str
                    - {CLASSTIME}: str
                    - {CLASSINTRO}': str
                    - {COVERURL}: str(URL)
        '''
        sheet = self.__client.open("youngmaker-little-helper").worksheet(self.__newClassSheet)
        week_addr = self.__newClassCheck(sheet, "week")
        camp_addr = self.__newClassCheck(sheet, "camp")
        stripe_addr = self.__newClassCheck(sheet, "stripe")
        # Do update.
        week = self.__newClassFill(sheet, "week", week_addr) if week_addr else []
        camp = self.__newClassFill(sheet, "camp", camp_addr) if camp_addr else []
        stripe = self.__newClassFill(sheet, "stripe", stripe_addr) if stripe_addr else []
        return week + camp + stripe
#         return {"week":week,"camp":camp, "stripe":stripe}
    
    def __newClassCheck(self, sheet, classLabel):
        '''
            回傳一個串列
            
            retrun type:
                - list
                    - cell address: str
        '''
        if classLabel == 'week':
            base_shrange = "A4:B33"
        elif classLabel == 'camp':
            base_shrange = "A36:B65"
        elif classLabel == 'stripe':
            base_shrange  = "A68:B97"
        new_list= []
        lock = True
        base = sheet.range(base_shrange)
        for idx, r in enumerate(base):
            if idx %2 == 1 and r.value == "":
                lock = False
            elif idx%2 == 0 and r.value == '':
                new_list.append(r.address)
            if not lock:
                new_list.pop(-1)
                break
        return new_list
    
    def __newClassFill(self, sheet, classLabel, addr):
        '''
            回傳一個list
            
            return type: 
                - list
                    - Id: str(uuid4)
                    - {CLASSTAG}: str
                    - {CLASSNAME}: str
                    - {CLASDATE}: str
                    - {CLASSTIME}: str
                    - {CLASSINTRO}': str
                    - {COVERURL}: str(URL)
        '''
        newId = [[str(uuid.uuid4())] for _ in addr]
        row_shrange = [addr[0][1:], addr[-1][1:]]
        print(row_shrange)
        sheet.update(":".join( [addr[0], addr[-1]] ), newId)
#         pprint( self.ongoingWeek(row_shrange = row_shrange, sheet = sheet) )
#         return []
        if classLabel == 'week':
            return [ dict(d,**{'{Id}': nid[0]}) for d, nid in zip(self.ongoingWeek(row_shrange = row_shrange, sheet = sheet), newId) ]
        elif classLabel == 'camp':
            return [ dict(d, **{'{Id}': nid[0]}) for d, nid in zip(self.ongoingCamp(row_shrange = row_shrange, sheet = sheet), newId) ]
        elif classLabel == 'stripe':
            return [ dict(d, **{'{Id}': nid[0]}) for d, nid in zip(self.ongoingStripe(row_shrange = row_shrange, sheet = sheet), newId) ]
    
    def expiredClass(self,):
        '''
            回傳一串欲更新於dynamodb 的 list
            
            return type: 
                - list
                    - Id: str(uuid4)
                    - Datetime: str(isoformat)
                    - AlbumHash: str
        '''
        sheet = self.__client.open("youngmaker-little-helper").worksheet(self.__newClassSheet)
        # 檢查過期課程01
        week_addr = self.__expiredClassCheck(sheet, "week")
        camp_addr = self.__expiredClassCheck(sheet, "camp")
        stripe_addr = self.__expiredClassCheck(sheet, "stripe")
#         刪除過期課程.
        week_fill = self.__expiredClassDelete(sheet, "week", week_addr) if week_addr else []
        camp_fill = self.__expiredClassDelete(sheet, "camp", camp_addr) if camp_addr else []
        stripe_fill = self.__expiredClassDelete(sheet, "stripe", stripe_addr) if stripe_addr else []
        # 更新課程相簿
        week = self.__expiredClassFill(sheet, "week", week_fill) if week_fill else []
        camp = self.__expiredClassFill(sheet, "camp", camp_fill) if camp_fill else []
        stripe = self.__expiredClassFill(sheet, "stripe", stripe_fill) if stripe_fill else []
        # 回傳有相片的課程
        return week + camp + stripe
#         return {"week":week, 'camp':camp, "stripe":stripe}

    def __expiredClassCheck(self, sheet, classLabel):
        '''
            回傳欲更新的列號
            
            return type:
                - dict
            element of dict:
                - expired: dict
                    - list
                        - cell address: str
                - preserve: dict
                    - list
                        - cell address: str
        '''
        if classLabel == 'week':
            base_shrange = "F4:F33"
        elif classLabel == 'camp':
            base_shrange = "F36:F65"
        elif classLabel == 'stripe':
            base_shrange  = "F68:F97"
        expi = []
        pres = []
        today = datetime.now()
        try:
            # 欄位為空
            base = sheet.range(base_shrange)
            for cell in base:
                if cell.value:
                    date = datetime.strptime( (cell.value).split('-')[-1], "%Y/%m/%d" )
                    if today - timedelta(days=1) >= date:
                        expi.append(cell.address)
                    else:
                        pres.append(cell.address)
        except:
            pass
        return {'expired':expi, 'preserve':pres}

    def __expiredClassDelete(self, sheet, classLabel, addr):
        if classLabel == 'week':
            start_row = 4
        elif classLabel == 'camp':
            start_row = 36
        elif classLabel == 'stripe':
            start_row = 68
        # expi/pres_shrange是欲讀取的表單座標
        expi_shrange = [ f'A{a[1:]}:Q{a[1:]}' for a in addr['expired']] if addr['expired'] else []

#         pres_tmp = addr['preserve']
#         pres_idx = [ pres_tmp.pop(idx) for idx in range(len(pres_tmp)) if (4+idx) != int(pres_tmp[idx][1:])]
#         pres_st = int(pres_tmp[-1][1:]) + 1
#         pres_shrange = [ f'A{a[1:]}:Q{a[1:]}' for a in pres_idx]

        pres_shrange = [ f'A{a[1:]}:Q{a[1:]}' for a in addr['preserve']] if addr['preserve'] else []
        expired = sheet.batch_get(expi_shrange) if expi_shrange else []
        preserve = sheet.batch_get(pres_shrange)  if pres_shrange else []

    
        del_rows = len(pres_shrange) + len(expi_shrange)
        update_range = f'A{start_row}:Q{ (start_row - 1) + del_rows }'
        ept = ['' for _ in range(ord('Q') - ord('A') + 1)]
        
        update_values = []
        for i in range(del_rows):
            if i < len(preserve):
                update_values.append(preserve[i][0])
            else:
                update_values.append(ept)
#         sheet.update(update_range, update_values)
        expired_fill = []
        for ex in expired:
            date = ex[0][5].split('-')[0]
            time = ex[0][6].split('-')[0]
            expired_fill.append({"Id":ex[0][0],
                                "{CLASSTAG}":ex[0][1],
                                "{CLASSNAME}":ex[0][2],
                                "{CLASSDATE}":datetime.strptime(f"{date} {time}", "%Y/%m/%d %H:%M").isoformat() })
        return expired_fill
    
    def __expiredClassFill(self, sheet, classLabel, new_hist):
        if classLabel == 'week':
            shrange ='A{}:E{}'
        elif classLabel == 'camp':
            shrange = 'F{}:J{}'
        elif classLabel == 'stripe':
            shrange = 'K{}:O{}'
        sheet = self.__client.open("youngmaker-little-helper").worksheet(self.__albumSheet)
        # 若表個為空 則st = 4
        hist = []
        try:
            hist = sheet.get(shrange.format(4, 1000))
            shrange_st = 4 + len(hist)
        except:
            shrange_st = 4
        shrange_end = shrange_st+len(new_hist)-1
        sheet.update(shrange.format(shrange_st, shrange_end), [list(v.values())for v in new_hist])
        return self.__expiredHistoryUpdate(hist)
        
#         return new_hist
    
    def __expiredHistoryUpdate(self, hist):
        return [ {'Id':h[0], '{CLASSDATE}':h[3],'{ALBUMHASH}':h[-1] }for h in hist if len(h)==5] if hist else []

# pprint(ExcelBase().ongoingTotal())
# pprint(ExcelBase().ongoingStripe())
# pprint(ExcelBase().ongoingWeek())
# pprint(ExcelBase().newClass())
pprint(ExcelBase().expiredClass())

