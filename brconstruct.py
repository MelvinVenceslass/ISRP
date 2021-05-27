


class serialReader():

        
    
    def barcode(self,barcode):
        barcode = [str(barcode[3:])+str(d) if str(barcode[:3]) in str(e) else None for d in self.parts for e in self.parts[d]]
        barcode = [each for each in barcode if each][0]
        return barcode
    
    def __init__(self):
        self.parts=eval(open("templates\part.json",'r').read())
        
    
