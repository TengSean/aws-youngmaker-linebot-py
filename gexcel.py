import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


class ExcelBase(object):
    def __init__(self, ):
        scope = ["https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("./config/creds.json", scope)
        self.__client = gspread.authorize(creds)
        
    def ongoing(self,):
        cur_sheet = self.__client.open("youngmaker-little-helper").worksheet("最新課程資訊")  # Open the spreadhseet
        week_intro, week_url = cur_sheet.batch_get(['L4:L33', 'P4:P33'])
        camp_intro, camp_url = cur_sheet.batch_get(['L36:L65', 'P36:P65'])
        stripe_intro, stripe_url = cur_sheet.batch_get(['L68:L97', 'P68:P97'])
        weekend = [{'intro':intro[0],'url': url[0] }for intro, url in zip(week_intro, week_url)]
        camp = [{'intro':intro[0],'url':url[0] } for intro, url in zip(camp_intro, camp_url)]
        stripe = [{'intro':intro[0],'url':url[0]} for intro, url in zip(stripe_intro, stripe_url)]
        return weekend, camp, stripe
    def history(self,):
        cur_sheet = self.__client.open("youngmaker-little-helper").worksheet("歷史課程資訊")  # Open the spreadhseet
        #load from boto3.
        stripe, weekend, camp = cur_sheet.batch_get(['A3:C1000', 'D3:F1000', 'G3:I1000'])
        weekend = [{'name':w[0], 'date':w[1], 'photos': w[2].split('\n')} for w in weekend]
        camp = [{'name': c[0], 'date': c[1], 'photos' : c[2].split('\n')} for c in camp]
        stripe = [{'name': s[0], 'date': s[1], 'photos' : s[2].split('\n')} for s in stripe]
        return weekend, camp, stripe
# ge = ExcelBase().ongoing()
# ge = ExcelBase().history()
