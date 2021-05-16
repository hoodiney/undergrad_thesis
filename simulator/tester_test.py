from Tester import Tester
from Simulator import Simulator

if __name__ == '__main__':
    tester = Tester()
    (simulator_list, time_waited_list, staff_num_list) = tester.search_for_staff_num()
    print(len(time_waited_list))
    print(min(time_waited_list))
    print(min(staff_num_list))
    simulator_index = staff_num_list.index(min(staff_num_list))
    print(time_waited_list[simulator_index])
    tester.print_simulator(simulator_list[simulator_index])
