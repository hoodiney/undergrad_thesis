# from simulator_class import Simulator
from Simulator import Simulator
import matplotlib.pyplot as plt
import matplotlib.colors
import time

colors = list(matplotlib.colors.CSS4_COLORS.keys())
print(len(colors))

FAILURE_RATE = 0.076
GROUP_SIZE = 9 # 18
GROUP_NUM = 76 # 38
STAFF_NUM = 9
# meter
GROUP_INTERVAL = 3.02 # 3.02
MACHINE_INTERVAL = 8.36 # 8.36
# s / m
SPEED = 0.8 # 0.8
# second
FIX_TIME = 600
STAFF_NUM_BASELINE = 76
TIME_WAITED_BASELINE = 0.05
X_DIVIDE = 38 # 只有38和18两种

def draw_graph_staff_num(x_list_list, y_list_list):
    plt.figure(1)
    for i in range(len(x_list_list)):
        plt.plot(x_list_list[i], y_list_list[i], marker="o", linestyle="dashed", color=matplotlib.colors.CSS4_COLORS[colors[i + 1]], alpha=0.8, linewidth=1, label='staff_%d' % i)
    plt.legend(loc="upper right")
    plt.xlabel('staff num')
    plt.ylabel('y axis')

def draw_graph_time_waited(x_list_list, y_list_list):
    plt.figure(2)
    for i in range(len(x_list_list)):
        plt.plot(x_list_list[i], y_list_list[i], marker="o", linestyle="dashed", color=matplotlib.colors.CSS4_COLORS[colors[i + 10]], alpha=0.8, linewidth=1, label='time_waited_%d' % i)
    plt.legend(loc="upper right")
    plt.xlabel('staff num')
    plt.ylabel('y axis')

def test_single_run(simulator, round):
    (average_staff_used, average_time_waited) = simulator.run(round)
    print(average_staff_used)
    print(average_time_waited)

def test_staff_num(simulator, round):
    total_staff_used_list = []
    total_time_waited_list = []
    staff_num_list = [i for i in range(1, GROUP_SIZE + 1)]

    for staff_num in range(1, GROUP_SIZE + 1):
        print("this is time %d" % staff_num)
        simulator.set_staff_num(staff_num)
        (average_staff_used, average_time_waited) = simulator.run(round)
        total_staff_used_list.append(average_staff_used)
        total_time_waited_list.append(average_time_waited)

    return total_staff_used_list, total_time_waited_list

def test_influence_of_distance(simulator, round, range_start, range_end):
    rec_total_staff_used_list = []
    rec_total_time_waited_list = []
    rec_staff_num_list = []
    for distance in range(range_start, range_end):
        simulator.set_distance(distance)
        print("\n\n\n\n\nthis is distance %d\n\n\n\n\n" % distance)
        (total_staff_used_list, total_time_waited_list) = test_staff_num(simulator, round)
        rec_total_staff_used_list.append(total_staff_used_list)
        rec_total_time_waited_list.append(total_time_waited_list)
        rec_staff_num_list.append([i for i in range(1, GROUP_SIZE + 1)])

    draw_graph_staff_num(rec_staff_num_list, rec_total_staff_used_list)
    draw_graph_time_waited(rec_staff_num_list, rec_total_time_waited_list)
    plt.show()


if __name__ == '__main__':
    test_round = 10000
    simulator = Simulator(FAILURE_RATE, GROUP_SIZE, GROUP_NUM, STAFF_NUM, GROUP_INTERVAL, MACHINE_INTERVAL, SPEED, FIX_TIME, X_DIVIDE)
    # test_influence_of_distance(simulator, test_round, 0, 1)
    time_start = time.time()
    test_single_run(simulator, test_round)
    time_end = time.time()
    print("time for this run is:")
    print(time_end - time_start)

    # (total_staff_used_list, total_time_waited_list) = test_staff_num(simulator, test_round)
    # draw_graph_time_waited([[i for i in range(1, GROUP_SIZE + 1)]], [total_time_waited_list])
    # plt.show()


    # result_staff = []
    # result_waited_time = []
    # staff_num_list = []
    # for i in range(1, GROUP_SIZE + 1):
    #     simulator.set_staff_num(i)
    #
    #     (average_staff_used, average_time_waited) = simulator.run(1)
    #     result_staff.append(average_staff_used)
    #     result_waited_time.append(average_time_waited)
    #     staff_num_list.append(i)
    # plt.plot(staff_num_list, result_staff, '-', color='g', alpha=0.8, linewidth=1, label='staff')
    # plt.plot(staff_num_list, result_waited_time, '-', color='b', alpha=0.8, linewidth=1, label='time_waited')
    # plt.legend(loc="upper right")
    # plt.xlabel('x axis')
    # plt.ylabel('y axis')
    #
    # plt.show()