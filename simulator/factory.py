class Machine:
    def __init__(self, x, y):
        self.status = 0
        self.time_waited = 0
        self.x = x
        self.y = y
        self.if_chosen = 0 # 0表示机器是否在员工的queue里

class Staff:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.queue = []
        self.time_left = 0
