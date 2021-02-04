import json
import re


class MsgHandler(object):
    def __init__(self):
        pass
    def msgReplace(self, obj, values):
#         print(values)
        def extract(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        obj[k] = extract(v)
                    elif isinstance(v, str):
                        mares = re.findall(r"{[A-Z]+[0-9]*}", v)
                        if mares:
                            print(obj)
                            for mr in mares:
                                # replace.
#                                 print(values[mr])
                                obj[k] = re.sub(mr, values[mr],v)
            elif isinstance(obj, list):
                for idx, item in enumerate(obj):
                    obj[idx] = extract(item)
            return obj
        return extract(obj)