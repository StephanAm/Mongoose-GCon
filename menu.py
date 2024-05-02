from typing import Callable, Any

class MenuItem:
    def __init__(self,name) -> None:
        self.name = name
    
    def __str__(self) -> str:
        return self.name
    
    def execute(self):
        raise NotImplementedError()
    
    def setParent(self, parent:Any):
        self.parent = parent

class Command(MenuItem):
    def __init__(self, name, action) -> None:
        super().__init__(name)
        self.action = action
    def execute(self):
        return self.parent

class Menu(MenuItem):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._items = []
        self._selectedItemIndex = 0
    def __iter__(self):
        self._iter_n = 0
        return self
    def __next__(self):
        if self._iter_n == self._item_count:
            raise StopIteration
        res = (self._iter_n == self._selectedItemIndex, self._items[self._selectedItemIndex])
        self._iter_n += 1
        return res

    def getActiveItem(self)->MenuItem:
        return self._items[self._selectedItemIndex]

    def selectNextItem(self) -> None:
        self._selectedItemIndex += 1
        self._selectedItemIndex %= len(self._items)

    def selectPrevItem(self) -> None:
        self._selectedItemIndex -= 1
        self._selectedItemIndex %= len(self._items)

    def addMenuItem(self,item:MenuItem):
        item.setParent(self)
        self._items.append(item)
        self._item_count = len(self._items)

    def execute(self):
        return self
    
    def getOptions(self):
        return tuple(self._items)
    
    def createSubMenu(self,name):
        sub = Menu(name)
        self.addMenuItem(sub)
        return sub
    
    def createCommand(self,name,action:Callable) -> Command:
        cmd = Command(name,action)
        self.addMenuItem(cmd)
        return cmd

