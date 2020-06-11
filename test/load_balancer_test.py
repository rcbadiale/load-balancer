# -*- coding: utf-8 -*-
"""
Test file for 'load_balancer.py' file for Diebold Nixdorf practical test.

Created on Wed Jun 10 08:55:37 2020

@author: rcbadiale
"""

import pytest
from main import load_balancer as lb


@pytest.mark.parametrize("umax", range(1, 11))
def test_server_availability_for_new_users(umax):
    server = lb.Server(umax)
    assert server.available() is True


def test_server_add_new_users():
    server = lb.Server(2)
    ttask = 1
    assert server.add(ttask) is True
    assert server.users == [ttask]


def test_server_not_available_for_new_users():
    server = lb.Server(2)
    server.add(1)
    server.add(1)
    assert server.available() is False


def test_should_not_add_user_to_server_reaches_max_users():
    server = lb.Server(2)
    server.add(1)
    server.add(1)
    assert server.add(1) is False


def test_check_users_task_lenght_server():
    server = lb.Server(2)
    server.add(1)
    server.add(10)
    assert server.users == [1, 10]


def test_check_higher_lenght_task_server():
    server = lb.Server(2)
    server.add(1)
    server.add(10)
    assert server.max_task() == 10


def test_server_clear_method():
    server = lb.Server(2)
    server.add(0)
    server.add(1)
    server.clear()
    assert server.users == [1]


def test_server_tick_method_reduce_task_lenght_by_one_in_each_user():
    server = lb.Server(2)
    server.add(2)
    server.add(3)
    server.tick()
    assert server.users == [1, 2]


def test_server_tick_method_reduce_task_lenght_by_one_in_each_user_then_remove_empty_users():
    server = lb.Server(2)
    server.add(1)
    server.add(1)
    server.tick()
    assert server.users == []


def test_run_tick_multiple_servers():
    server1 = lb.Server(1)
    server2 = lb.Server(2)
    ttask = 2
    server1.add(ttask)
    server2.add(ttask)
    server2.add(ttask)
    lb.run_tick([server1, server2])
    assert server1.users == [ttask - 1]
    assert server2.users == [ttask - 1] * 2


def test_check_tasks_lenght_server1_bigger_server2_true():
    server1 = lb.Server(1)
    server2 = lb.Server(2)
    server1.add(5)
    server2.add(3)
    server2.add(2)
    assert lb.check_tasks(server1, server2) is True


def test_check_tasks_lenght_server1_bigger_server2_false():
    server1 = lb.Server(1)
    server2 = lb.Server(2)
    server1.add(1)
    server2.add(3)
    server2.add(2)
    assert lb.check_tasks(server1, server2) is False


def test_start_new_server_with_umax():
    servers = []
    umax = 5
    lb.start_new_server(servers, umax)
    assert len(servers) == 1


def test_get_best_server_for_new_user_one_available_spot():
    umax = 2
    server1 = lb.Server(umax)
    server2 = lb.Server(umax)
    server1.add(1)
    server1.add(3)
    server2.add(2)
    assert lb.get_best_server([server1, server2], umax) == server2


def test_get_best_server_for_new_user_one_available_spot_per_server_server1_should_be_chosen():
    umax = 2
    server1 = lb.Server(umax)
    server2 = lb.Server(umax)
    server1.add(3)
    server2.add(2)
    assert lb.get_best_server([server1, server2], umax) == server1


def test_get_best_server_for_new_user_full_server():
    umax = 2
    server = lb.Server(umax)
    server.add(1)
    server.add(3)
    assert isinstance(lb.get_best_server([server], umax), lb.Server) is True


def test_add_new_user_to_best_server():
    umax = 2
    ttask = 5
    server1 = lb.Server(umax)
    server2 = lb.Server(umax)
    server1.add(3)
    server2.add(2)
    lb.users_to_server([server1, server2], 1, umax, ttask)
    assert server1.users == [3, 5]


def test_add_two_new_users_to_best_servers():
    umax = 2
    ttask = 5
    server1 = lb.Server(umax)
    server2 = lb.Server(umax)
    server1.add(3)
    server2.add(2)
    lb.users_to_server([server1, server2], 2, umax, ttask)
    assert server1.users == [3, 5] and server2.users == [2, 5]


def test_main_loop_with_simplest_data():
    ttask = 2
    umax = 2
    users = [1]
    base_cost = 1
    assert lb.main_loop(ttask, umax, users, base_cost) == ([[1], [1], []], 2)


def test_main_loop_with_given_example():
    ttask = 4
    umax = 2
    users = [1, 3, 0, 1, 0, 1]
    base_cost = 1
    assert lb.main_loop(ttask, umax, users, base_cost) == ([[1], [2, 2], [2, 2], [2, 2, 1], [1, 2, 1], [2], [2], [1], [1], []], 15)


@pytest.mark.parametrize("ttask, umax, users, base_cost", [(10, 10, [5, 2, 6, 5, 10], 1)])
def test_main_loop_with_predefined_numbers(ttask, umax, users, base_cost):
    result = (
        [
            [5],
            [7],
            [10, 3],
            [10, 8],
            [10, 10, 8],
            [10, 10, 8],
            [10, 10, 8],
            [10, 10, 8],
            [10, 10, 8],
            [10, 10, 8],
            [5, 10, 8],
            [3, 10, 8],
            [7, 8],
            [2, 8],
            []
        ],
        34
    )
    assert lb.main_loop(ttask, umax, users, base_cost) == result


def test_read_input_file_given_example():
    ttask = 4
    umax = 2
    users = [1, 3, 0, 1, 0, 1]
    path = 'test/input.txt'
    data = lb.read_file(path)
    assert data == (ttask, umax, users)
