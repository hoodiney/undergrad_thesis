from factory import Machine, Staff
import random
from itertools import permutations

class Simulator:
    def __init__(self, failure_rate, group_size, group_num, staff_num, group_interval, machine_interval, speed, fix_time, x_divide):
        self.failure_rate = failure_rate
        self.group_size = group_size
        self.group_num = group_num
        self.staff_num = staff_num
        self.group_interval = group_interval
        self.machine_interval = machine_interval
        self.speed = speed
        self.fix_time = fix_time
        # self.staff_num_baseline = staff_num_baseline
        # self.time_waited_baseline = time_waited_baseline
        self.distance = 0
        self.time_interval = 1200
        self.x_divide = x_divide

        self.machine_status = [[Machine(0, 0) for i in range(self.group_size)] for j in range(self.group_num)]
        self.staff_status = [[Staff(0, 0) for i in range(staff_num)] for j in range(group_num)]
        self.machine_status_mark = [0, 1]
        self.distribution = [1 - failure_rate, failure_rate]
        self.if_one_empty = 0

        for i in range(group_num):
            for j in range(group_size):
                self.machine_status[i][j].x = (i % self.x_divide) * self.group_interval
                self.machine_status[i][j].y = (int(i / x_divide)) * self.group_size * self.machine_interval + j * self.machine_interval
        for i in range(self.group_num if self.if_one_empty == 0 else self.group_num - 1):
            for j in range(staff_num):
                self.staff_status[i][j].x = self.machine_status[i][j].x
                self.staff_status[i][j].y = self.machine_status[i][j].y

    def set_distance(self, distance):
        self.distance = distance

    def set_staff_num(self, staff_num):
        self.staff_num = staff_num
        self.staff_status = [[Staff(0, 0) for i in range(staff_num)] for j in range(self.group_num)]
        for i in range(self.group_num if self.if_one_empty == 0 else self.group_num - 1):
            for j in range(staff_num):
                self.staff_status[i][j].x = self.machine_status[i][j].x
                self.staff_status[i][j].y = self.machine_status[i][j].y

    def set_fix_time(self, fix_time):
        self.fix_time = fix_time

    def set_failure_rate(self, failure_rate):
        self.failure_rate = failure_rate

    def set_x_divide(self, x_divide):
        self.x_divide = x_divide
        self.machine_status = [[Machine(0, 0) for i in range(self.group_size)] for j in range(self.group_num)]
        self.staff_status = [[Staff(0, 0) for i in range(self.staff_num)] for j in range(self.group_num)]
        for i in range(self.group_num):
            for j in range(self.group_size):
                self.machine_status[i][j].x = (i % self.x_divide) * self.group_interval
                self.machine_status[i][j].y = (int(i / x_divide)) * self.group_size * self.machine_interval + j * self.machine_interval
        for i in range(self.group_num if self.if_one_empty == 0 else self.group_num - 1):
            for j in range(self.staff_num):
                self.staff_status[i][j].x = self.machine_status[i][j].x
                self.staff_status[i][j].y = self.machine_status[i][j].y

    def set_group(self, group_num, group_size):
        self.group_num = group_num
        self.group_size = group_size
        self.machine_status = [[Machine(0, 0) for i in range(group_size)] for j in range(group_num)]
        for i in range(group_num):
            for j in range(group_size):
                self.machine_status[i][j].x = (i % self.x_divide) * self.group_interval
                self.machine_status[i][j].y = (int(i / self.x_divide)) * self.group_size * self.machine_interval + j * self.machine_interval

    # 为了提高仿真器的真实性，仿真器需要能够遍历各种分支情况
    def pattern_update(self):
        for col in range(self.group_num):
            machine_in_queue = []
            # 先分配machine的status，staff的状态可以通过machine的状态进行推导
            # 选定组号的时候就获取负责当前组机器的所有staff
            for row in range(self.group_size):
                self.machine_status[col][row].status = (random.choices(self.machine_status_mark, self.distribution))[0] * self.fix_time
                if self.machine_status[col][row].status == self.fix_time:
                    self.machine_status[col][row].if_chosen = random.randint(0,1)
                    if self.machine_status[col][row].if_chosen == 1:
                        machine_in_queue.append(self.machine_status[col][row])
            # for i in range(len(machine_in_queue)):
            #     print((machine_in_queue[i].x / self.group_interval, machine_in_queue[i].y / self.machine_interval))
            # print(len(machine_in_queue))

            staff_col_start = col % self.x_divide + self.x_divide * int(col / self.x_divide) if (col % self.x_divide) - self.distance <= 0 else col - self.distance
            staff_col_end = col + 1 if (self.if_one_empty == 0 or (self.if_one_empty == 1 and col != self.group_num - 1)) else col
            for i in range(staff_col_start, staff_col_end):
                for j in range(self.staff_num):
                    # print("i: %d, j: %d, start: %d, end: %d" % (i, j, staff_col_start, staff_col_end))
                    self.staff_status[i][j].x = random.uniform(self.machine_status[staff_col_start][0].x, self.machine_status[staff_col_end - 1][0].x)
                    self.staff_status[i][j].y = random.uniform(self.machine_status[staff_col_start][0].y, self.machine_status[staff_col_start][self.group_size - 1].y)
                    if len(machine_in_queue) == 0:
                        continue
                    # 如果当前staff在维修
                    if random.randint(0, 1) == 1:
                        # 分配在维修的machine
                        machine_choice = random.randrange(0, len(machine_in_queue))
                        self.staff_status[i][j].queue.append(machine_in_queue[machine_choice])
                        # 分配在维修machine的维修状态
                        self.staff_status[i][j].queue[0].status = random.uniform(0, self.fix_time)
                        self.staff_status[i][j].queue[0].time_waited = self.fix_time - self.staff_status[i][j].queue[0].status \
                                                                        + self.speed * (abs(self.staff_status[i][j].x - self.staff_status[i][j].queue[0].x) + abs(self.staff_status[i][j].y - self.staff_status[i][j].queue[0].y))
                        machine_in_queue.pop(machine_choice)
                        self.staff_status[i][j].x = self.staff_status[i][j].queue[0].x
                        self.staff_status[i][j].y = self.staff_status[i][j].queue[0].y
                        self.staff_status[i][j].time_left = self.fix_time - self.staff_status[i][j].queue[0].status
            # 将machine_in_queue的顺序打乱
            random.shuffle(machine_in_queue)
            # 分配machine
            for machine in machine_in_queue:
                time_left_min = 0
                staff_choice = (0, 0)
                flag = 0
                for i in range(col - self.distance if col - self.distance > 0 else 0, col + 1):
                    for j in range(self.staff_num):
                        time_left = self.fix_time + self.staff_status[i][j].time_left + self.speed * (abs(self.staff_status[i][j].x - machine.x) + abs(self.staff_status[i][j].y - machine.y))
                        if flag == 0:
                            time_left_min = time_left
                            staff_choice = (i, j)
                            flag = 1
                        else:
                            if time_left < time_left_min:
                                time_left_min = time_left
                                staff_choice = (i, j)
                self.staff_status[staff_choice[0]][staff_choice[1]].queue.append(machine)
                self.staff_status[staff_choice[0]][staff_choice[1]].time_left = time_left_min




    def assign_task_col_greedy(self, staff_list, machine_list):
        staff_place_list = []
        staff_rec_list = []
        time_used_rec_list = []
        for staff in staff_list:
            staff_place_list.append((self.staff_status[staff[0]][staff[1]].x, self.staff_status[staff[0]][staff[1]].y))

        machine_list_size = len(machine_list)
        for order in range(machine_list_size):
            staff_rec_list.clear()
            time_used_rec_list.clear()
            for i in range(len(machine_list)):
                staff_choice = 0
                time_used_min = 0
                for j in range(len(staff_list)):
                    time_used = self.fix_time + self.staff_status[staff_list[j][0]][staff_list[j][1]].time_left \
                                + (abs(staff_place_list[j][0] - self.machine_status[machine_list[i][0]][machine_list[i][1]].x)
                                   + abs(
                                staff_place_list[j][1] - self.machine_status[machine_list[i][0]][machine_list[i][1]].y)) * self.speed
                    if j == 0:
                        staff_choice = j
                        time_used_min = time_used
                    else:
                        if time_used < time_used_min:
                            staff_choice = j
                            time_used_min = time_used
                staff_rec_list.append(staff_list[staff_choice])
                time_used_rec_list.append(time_used_min)
            machine_index = time_used_rec_list.index(min(time_used_rec_list))
            self.machine_status[machine_list[machine_index][0]][machine_list[machine_index][1]].if_chosen = 1
            self.staff_status[staff_rec_list[machine_index][0]][staff_rec_list[machine_index][1]].queue.append(
                self.machine_status[machine_list[machine_index][0]][machine_list[machine_index][1]])
            self.staff_status[staff_rec_list[machine_index][0]][staff_rec_list[machine_index][1]].time_left = \
            time_used_rec_list[machine_index]
            staff_index = staff_list.index((staff_rec_list[machine_index][0], staff_rec_list[machine_index][1]))
            staff_place_list[staff_index] = (self.machine_status[machine_list[machine_index][0]][machine_list[machine_index][1]].x,
                                             self.machine_status[machine_list[machine_index][0]][machine_list[machine_index][1]].y)
            machine_list.pop(machine_index)

    def assign_task_col_bf(self, staff_list, machine_list):
        staff_place_list = []
        machine_waited_time_min = 0
        flag = 0
        machine_permutation_choice = tuple(machine_list)
        permutation_cnt = 0
        for machine_permutation in permutations(machine_list):
            permutation_cnt += 1
            machine_waited_time = 0
            for staff in staff_list:
                staff_place_list.append((self.staff_status[staff[0]][staff[1]].x, self.staff_status[staff[0]][staff[1]].y))

            for index in range(len(machine_list)):
                staff_time_used_list = []
                for i in range(len(staff_list)):
                    total_used_time = self.staff_status[staff_list[i][0]][staff_list[i][1]].time_left + (abs(
                        staff_place_list[i][0] - self.machine_status[machine_permutation[index][0]][
                            machine_permutation[index][1]].x) + abs(
                        staff_place_list[i][1] - self.machine_status[machine_permutation[index][0]][
                            machine_permutation[index][1]].y)) * self.speed
                    staff_time_used_list.append(total_used_time)
                staff_choice = staff_time_used_list.index(min(staff_time_used_list))
                machine_waited_time += (len(machine_list) - index) * (staff_time_used_list[staff_choice] + self.fix_time)
                # staff_list[staff_choice].queue.append(machine)
                staff_place_list[staff_choice] = (
                self.machine_status[machine_permutation[index][0]][machine_permutation[index][1]].x,
                self.machine_status[machine_permutation[index][0]][machine_permutation[index][1]].y)
            if flag == 0:
                machine_waited_time_min = machine_waited_time
                machine_permutation_choice = machine_permutation
                flag = 1
            else:
                if machine_waited_time < machine_waited_time_min:
                    machine_waited_time_min = machine_waited_time
                    machine_permutation_choice = machine_permutation
            staff_place_list.clear()
        # 此处已获得最低等待时间的machine处理顺序
        for staff in staff_list:
            staff_place_list.append((self.staff_status[staff[0]][staff[1]].x, self.staff_status[staff[0]][staff[1]].y))
        for machine in list(machine_permutation_choice):
            staff_time_used_list = []
            for i in range(len(staff_list)):
                total_used_time = self.staff_status[staff_list[i][0]][staff_list[i][1]].time_left + (
                            abs(staff_place_list[i][0] - self.machine_status[machine[0]][machine[1]].x) + abs(
                        staff_place_list[i][1] - self.machine_status[machine[0]][machine[1]].y)) * self.speed
                staff_time_used_list.append(total_used_time)
            staff_choice = staff_time_used_list.index(min(staff_time_used_list))
            self.staff_status[staff_list[staff_choice][0]][staff_list[staff_choice][1]].time_left += staff_time_used_list[
                                                                                                    staff_choice] + self.fix_time
            self.staff_status[staff_list[staff_choice][0]][staff_list[staff_choice][1]].queue.append(
                self.machine_status[machine[0]][machine[1]])
            staff_place_list[staff_choice] = (self.machine_status[machine[0]][machine[1]].x, self.machine_status[machine[0]][machine[1]].y)
            self.machine_status[machine[0]][machine[1]].if_chosen = 1

    def assign_task_origin(self):
        for i in range(self.group_num):
            staff_list = []
            machine_list = []
            for j in range(self.staff_num):
                staff_list.append((i, j))
            for j in range(self.group_size):
                if self.machine_status[i][j].status == self.fix_time and self.machine_status[i][j].if_chosen == 0:
                    machine_list.append((i, j))
            if len(staff_list) == 0 or len(machine_list) == 0:
                continue
            # assign_task_col_bf(staff_list, machine_list)
            self.assign_task_col_greedy(staff_list, machine_list)

    def assign_task_only_right(self):
        for i in range(self.group_num):
            staff_list = []
            machine_list = []
            # 每组在分配本组machine时除了要遍历本组，还要遍历helper组
            staff_col_start = i % self.x_divide + self.x_divide * int(i / self.x_divide) if (i % self.x_divide) - self.distance <= 0 else i - self.distance
            staff_col_end = i + 1 if (self.if_one_empty == 0 or (self.if_one_empty == 1 and i != self.group_num - 1)) else i
            for index in range(staff_col_start, staff_col_end):
                for j in range(self.staff_num):
                    staff_list.append((i, j))
            for j in range(self.group_size):
                if self.machine_status[i][j].status == self.fix_time and self.machine_status[i][j].if_chosen == 0:
                    machine_list.append((i, j))
            if len(staff_list) == 0 or len(machine_list) == 0:
                continue
            # assign_task_col_bf(staff_list, machine_list)
            self.assign_task_col_greedy(staff_list, machine_list)

    def update_all(self):
        total_staff_used = 0
        total_time_waited = 0
        # time_period = self.group_size * self.fix_time + (self.group_size - 1) * self.machine_interval * self.speed
        time_period = 0
        for i in range(self.group_num if self.if_one_empty == 0 else self.group_num - 1):
            for j in range(self.staff_num):
                if len(self.staff_status[i][j].queue) == 0:
                    continue
                if time_period < self.staff_status[i][j].time_left:
                    time_period = self.staff_status[i][j].time_left
                total_staff_used += 1
                queue_size = len(self.staff_status[i][j].queue)
                # 将时间限制在time_interval内
                time_left_for_use = self.time_interval
                for index in range(queue_size):
                    time_needed_this_machine = self.fix_time + (abs(self.staff_status[i][j].x - self.staff_status[i][j].queue[index].x) + abs(self.staff_status[i][j].y - self.staff_status[i][j].queue[index].y)) * self.speed
                    if time_left_for_use >= time_needed_this_machine:
                        total_time_waited += (queue_size - index) * (self.fix_time + (
                                    abs(self.staff_status[i][j].x - self.staff_status[i][j].queue[index].x) + abs(
                                self.staff_status[i][j].y - self.staff_status[i][j].queue[index].y)) * self.speed)
                        time_left_for_use -= time_needed_this_machine
                    else:
                        total_time_waited += (queue_size - index) * time_left_for_use

        return total_staff_used, total_time_waited, time_period

    def reset_all(self):
        for i in range(self.group_num):
            for j in range(self.group_size):
                self.machine_status[i][j].status = 0
                self.machine_status[i][j].time_waited = 0
                self.machine_status[i][j].if_chosen = 0
        for i in range(self.group_num if self.if_one_empty == 0 else self.group_num - 1):
            for j in range(self.staff_num):
                self.staff_status[i][j].queue.clear()
                self.staff_status[i][j].x = self.machine_status[i][j].x
                self.staff_status[i][j].y = self.machine_status[i][j].y
                self.staff_status[i][j].time_left = 0

    def run(self, round):
        total_staff_used_list = []
        total_time_waited_list = []
        file = open("debug.txt", "w")
        for time in range(round):
            # print("this is round %d" % time)
            ###### for testing ######
            rec_machine_status = [[0 for i in range(self.group_size)] for j in range(self.group_num)]
            rec_machine_time_waited = [[0 for i in range(self.group_size)] for j in range(self.group_num)]
            file.write("this is time %d\n" % time)
            ###### for testing ######

            self.pattern_update()
            ###### for testing ######
            for i in range(self.group_num):
                for j in range(self.group_size):
                    rec_machine_time_waited[i][j] = self.machine_status[i][j].time_waited
                    rec_machine_status[i][j] = self.machine_status[i][j].status
            file.write("time_waited " + str(rec_machine_time_waited) + "\n")
            file.write("machine_status " + str(rec_machine_status) + "\n")
            ###### for testing ######

            self.assign_task_only_right()
            ###### for testing ######
            for i in range(self.group_num):
                for j in range(self.staff_num):
                    rec_staff_queue = []
                    file.write("group {} num {}\n".format(i, j))
                    file.write("x: {}, y: {}\n".format(self.staff_status[i][j].x, self.staff_status[i][j].y))
                    for machine in self.staff_status[i][j].queue:
                        rec_staff_queue.append((machine.x, machine.y))
                    file.write(str(rec_staff_queue) + "\n")
                    file.write(str(self.staff_status[i][j].time_left) + "\n")
            ###### for testing ######
            (total_staff_used, total_time_waited, time_period) = self.update_all()
            total_staff_used_list.append(total_staff_used / self.group_num)
            # total_time_waited_list.append(total_time_waited / (self.group_num * self.group_size * time_period) if time_period != 0 else 0)
            total_time_waited_list.append(total_time_waited / (self.group_num * self.group_size * self.time_interval))
            self.reset_all()
        file.close()
        return sum(total_staff_used_list) / len(total_staff_used_list), sum(total_time_waited_list) / len(total_time_waited_list)

