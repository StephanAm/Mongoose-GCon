from typing import cast,Sequence,Iterable
import whiptail
from subprocess import Popen, run

class Whiptail(whiptail.Whiptail):

    def yesno(self, msg: str, default: str = "yes") -> bool:
        width = len(msg)+10
        if width<40:
            width=40
        msg=msg.center(width-5)
        cmd = ["whiptail",
            "--title",
            self.title,
            "--backtitle",
            self.backtitle,
            "--yesno",
            str(msg),
            str(7),
            str(width)]

        result = run(cmd)
        return result.returncode==0
    
    def menu(self, 
             msg: str = '', 
             items: Sequence[str] | Sequence[Iterable[str]] = ..., 
             prefix: str = " - ",
             noCancel:bool=False) -> whiptail.Tuple[str | int]:
        
        if isinstance(items[0], str):
            items = cast(Sequence[str], items)
            parsed_items = [(i, '') for i in items]
        else:
            items = cast(Sequence[Iterable[str]], items)
            parsed_items = [(k, prefix + v) for k, v in items]

        extra = self.calc_height(msg) + whiptail._flatten(parsed_items)
        extraArgs=('--nocancel',) if noCancel else ()
        returncode, val = self.run("menu", msg, extra_values=extra, extra_args=extraArgs)
        return val, returncode