import string
from tuitools import colorize_string as cs, Colors

class CodeType:
    COMMENT="COMMENT"
class GCode:
    def __init__(self,type:str, tokens, number:int, comment:str, group:str):
        self.type = type
        self.tokens = tuple(tokens) if tokens else None
        self.number = number
        self.comment = comment
        self.group = group
        
        
    def shouldProcess(self):
        """Put any logic that should prevent an entry from being processed here"""
        if self.type == CodeType.COMMENT:
            return False
        return True

    def format(self):
        if self.type=='COMMENT':
            return cs(self.comment,Colors.DARK_GREY)
        s=[]
        for token in self.tokens:
            s.append(cs(token[0],getcolor(token)))
            s.append(token[1:])
            s.append(' ')
        s.append(cs(self.group,Colors.DARK_GREY))
        return "".join(s)

class GCodeParser:
    
    def parse(self, code:str, number:int=None) -> GCode:
        raw = code.strip()
        number = number
        if self.isComment(code):
            return self.commentInit(code,number)
        tokens = self.tokenize(code)
        type = tokens[0][0]
        group = getGroup(tokens[0])
        return GCode(type=type,tokens=tokens, comment=None, number=number, group=group)

    def commentInit(self,code:str, number:int):
        code = code.strip()
        if not (code.startswith('(') and code.endswith(')')):
            raise ValueError(f'{code} is malformed')
        comment = code.strip(' ()')
        type = CodeType.COMMENT        
        return GCode(type=type,tokens=None, comment=comment, number=number, group=None)


    def isComment(self,code:str):
        return code.startswith('(')

    @classmethod
    def tokenize(cls,code:str):
        code = code.strip().replace(' ','').upper()
        i,l = 0,len(code)
        tokens = []
        for j in range(1,l):
            if code[j] in string.ascii_uppercase:
                tokens.append(code[i:j])
                i=j
        else:
            tokens.append(code[i:])
        
        tokens[0] = normalize(tokens[0])
        
        return tuple(tokens)



def getcolor(token):
    c = {
        'G':Colors.GREEN,
        'M':Colors.BLACK,
        'X':Colors.LIGHT_RED,
        'Y':Colors.LIGHT_GREEN,
        'Z':Colors.YELLOW,
    }.get(token[0],Colors.WHITE)
    return c

def normalize(token):
    if len(token) > 2:
        return token
    a = token[0]
    if not a in 'GM':
        return token
    b=f'{int(token[1:]):02}'
    return a+b
    
def getGroup(word: str):
    for group, description in groups:
        if word in group:
            return description




GROUP0 = "G04", "G10", "G28", "G30", "G53", "G92", "G92.1", "G92.2", "G92.3"
GROUP1 = "G00", "G01", "G02", "G03", "G33", "G38.x", "G73", "G76", "G80", "G81", "G82", "G84", "G85", "G86", "G87", "G88", "G89"
GROUP2 = "G17", "G18", "G19", "G17.1", "G17.2", "G17.3"
GROUP3 = "G90", "G91"
GROUP4 = "G90.1", "G91.1"
GROUP5 = "G93", "G94"
GROUP6 = "G20", "G21"
GROUP7 = "G40", "G41", "G42", "G41.1", "G42.1"
GROUP8 = "G43", "G43.1", "G49"
GROUP10 = "G98", "G99"
GROUP12 = "G54", "G55", "G56", "G57", "G58", "G59", "G59.1", "G59.2", "G59.3"
GROUP13 = "G61", "G61.1", "G64"
GROUP14 = "G96", "G97"
GROUP15 = "G07", "G08"

MGROUP4 = "M00", "M01", "M02", "M30", "M60"
MGROUP7 = "M03", "M04", "M05"
MGROUP8 = "M07", "M08", "M09"
MGROUP9 = "M48", "M49"
MGROUP10 = "M100 to M199"
groups = (
    (GROUP1, "Current motion mode"),
    (GROUP2, "Plane Selection"),
    (GROUP3, "distance mode"),
    (GROUP4, "arc IJK distance mode"),
    (GROUP5, "feed rate mode"),
    (GROUP6, "units"),
    (GROUP7, "cutter radius compensation"),
    (GROUP8, "tool length offset"),
    (GROUP10, "return mode in canned cycles"),
    (GROUP12, "coordinate system selection"),
    (GROUP13, "path control mode"),
    (GROUP14, "spindle speed mode"),
    (GROUP15, "lathe diameter mode"),
    (MGROUP4, "stopping"),
    (MGROUP7, "spindle turning"),
    (MGROUP8, "coolant"),
    (MGROUP9, "enable/disable feed and speed override controls"),
    (MGROUP10, "operatordefinded"),
    (GROUP0, "")
)