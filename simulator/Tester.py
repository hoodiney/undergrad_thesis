# from simulator_class import Simulator
from Simulator import Simulator
import time

class Tester:
    def __init__(self):
        self.group_size_options = [[9, 18], [19, 38]]
        self.group_num_options = [[76, 38], [36, 18]]
        self.if_one_empty_options = [0, 1]
        self.distance_options = []
        self.staff_num_options = []
        self.staff_num_baseline = 76
        self.time_waited_baseline = 0.05
        self.x_divide = [38, 18]
        self.simulator = Simulator(0.076, 9, 76, 1, 3.02, 8.36, 0.8, 600)

    def set_distance_options(self, group_choice, if_one_empty):
        if if_one_empty == 0:
            self.distance_options = [i for i in range(self.group_num_options[group_choice])]
        else:
            self.distance_options = [i for i in range(1, self.group_num_options[group_choice])]

    def set_staff_num_options(self, group_choice):
        self.staff_num_options = [i for i in range(1, self.group_size_options[group_choice] + 1)]

    def print_simulator(self, simulator):
        print("group_size is %d" % simulator.group_size)
        print("group_num is %d" % simulator.group_num)
        print("staff_num is %d" % simulator.staff_num)
        print("distance is %d" % simulator.distance)
        print("if_one_empty is %d" % simulator.if_one_empty)

    def search_for_time_waited(self):
        simulator_list = []
        time_waited_list = []
        cnt = 0
        for if_one_empty in self.if_one_empty_options:
            self.simulator.if_one_empty = if_one_empty
            for group_choice in range(len(self.group_num_options)):
                self.set_distance_options(group_choice, if_one_empty)
                self.set_staff_num_options(group_choice)
                self.simulator.set_group(self.group_num_options[group_choice], self.group_size_options[group_choice])
                # for distance_choice in range(len(self.distance_options)):
                for distance_choice in range(3):
                    for staff_num_choice in range(len(self.staff_num_options)):
                        if (if_one_empty == 0 and self.group_num_options[group_choice] * self.staff_num_options[staff_num_choice] <= self.staff_num_baseline) \
                        or (if_one_empty == 1 and (self.group_num_options[group_choice] - 1) * self.staff_num_options[staff_num_choice] <= self.staff_num_baseline):
                            print("this is round %d" % cnt)
                            cnt += 1
                            start_time = time.time()
                            # 设置本次run的simulator参数
                            self.simulator.set_distance(self.distance_options[distance_choice])
                            self.simulator.set_staff_num(self.staff_num_options[staff_num_choice])

                            (average_staff_used, average_time_waited) = self.simulator.run(1000)
                            # 若time_waited比baseline小，则验证人数是否不大于原人数
                            if average_time_waited <= self.time_waited_baseline:
                                simulator_list.append(Simulator(self.simulator.failure_rate, self.simulator.group_size, self.simulator.group_num, self.simulator.staff_num, self.simulator.group_interval, self.simulator.machine_interval, self.simulator.speed, self.simulator.fix_time))
                                simulator_list[len(simulator_list) - 1].if_one_empty = self.simulator.if_one_empty
                                simulator_list[len(simulator_list) - 1].distance = self.simulator.distance
                                time_waited_list.append(average_time_waited)
                            end_time = time.time()
                            print(end_time - start_time)
        return simulator_list, time_waited_list

    def search_for_staff_num(self):
        simulator_list = []
        time_waited_list = []
        staff_num_list = []
        cnt = 0
        for if_one_empty in self.if_one_empty_options:
            self.simulator.if_one_empty = if_one_empty
            for group_choice in range(len(self.group_num_options)):
                self.set_distance_options(group_choice, if_one_empty)
                self.set_staff_num_options(group_choice)
                self.simulator.set_group(self.group_num_options[group_choice], self.group_size_options[group_choice])
                # for distance_choice in range(len(self.distance_options)):
                for distance_choice in range(3):
                    for staff_num_choice in range(len(self.staff_num_options)):
                        total_staff_num = self.group_num_options[group_choice] * self.staff_num_options[staff_num_choice] if if_one_empty == 0 else (self.group_num_options[group_choice] - 1) * self.staff_num_options[staff_num_choice]
                        if (if_one_empty == 0 and total_staff_num < self.staff_num_baseline) or (if_one_empty == 1 and total_staff_num < self.staff_num_baseline):
                            print("this is round %d" % cnt)
                            cnt += 1
                            start_time = time.time()
                            # 设置本次run的simulator参数
                            self.simulator.set_distance(self.distance_options[distance_choice])
                            self.simulator.set_staff_num(self.staff_num_options[staff_num_choice])

                            (average_staff_used, average_time_waited) = self.simulator.run(1000)
                            # 验证time_waited是否不大于原baseline
                            if average_time_waited <= self.time_waited_baseline:
                                simulator_list.append(Simulator(self.simulator.failure_rate, self.simulator.group_size, self.simulator.group_num, self.simulator.staff_num, self.simulator.group_interval, self.simulator.machine_interval, self.simulator.speed, self.simulator.fix_time))
                                simulator_list[len(simulator_list) - 1].if_one_empty = self.simulator.if_one_empty
                                simulator_list[len(simulator_list) - 1].distance = self.simulator.distance
                                time_waited_list.append(average_time_waited)
                                staff_num_list.append(total_staff_num)
                            end_time = time.time()
                            print(end_time - start_time)
        return simulator_list, time_waited_list, staff_num_list