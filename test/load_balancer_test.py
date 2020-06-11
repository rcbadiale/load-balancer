# -*- coding: utf-8 -*-
"""
Test file for 'load_balancer.py'.

Created on Wed Jun 10 08:55:37 2020

@author: rcbadiale
"""

import pytest
from main import load_balancer as lb


@pytest.mark.parametrize("umax", range(1, 11))
def test_should_return_true_when_server_is_available(umax):
    server = lb.Server(umax)
    assert server.available() is True


def test_should_return_true_when_user_is_added():
    server = lb.Server(2)
    ttask = 1
    assert server.add(ttask) is True


def test_should_return_false_when_server_is_not_available():
    server = lb.Server(2)
    server.add(1)
    server.add(1)
    assert server.available() is False


def test_should_return_false_when_try_to_add_user_after_max_users_reached():
    server = lb.Server(2)
    server.add(1)
    server.add(1)
    assert server.add(1) is False


def test_should_return_ticks_remaining_per_task_when_calling_users():
    server = lb.Server(2)
    server.add(1)
    server.add(10)
    assert server.users == [1, 10]


def test_should_return_highest_ticks_remaining_on_server():
    server = lb.Server(2)
    server.add(1)
    server.add(10)
    assert server.max_task() == 10


def test_should_remove_users_with_finished_tasks_on_server():
    server = lb.Server(2)
    server.add(0)
    server.add(1)
    server.clear()
    assert server.users == [1]


def test_should_reduce_one_tick_per_user_on_the_server_when_a_tick_passes():
    server = lb.Server(2)
    server.add(2)
    server.add(3)
    server.tick()
    assert server.users == [1, 2]


def test_should_reduce_one_tick_per_user_on_the_server_when_a_tick_passes_then_remove_users_with_finished_tasks():
    server = lb.Server(2)
    server.add(1)
    server.add(1)
    server.tick()
    assert server.users == []


def test_should_reduce_one_tick_per_user_on_all_servers_when_a_tick_passes():
    server1 = lb.Server(1)
    server2 = lb.Server(2)
    ttask = 2
    server1.add(ttask)
    server2.add(ttask)
    server2.add(ttask)
    lb.run_tick([server1, server2])
    assert server1.users == [ttask - 1]
    assert server2.users == [ttask - 1] * 2


def test_should_return_true_when_server1_has_longer_tasks_than_server2():
    server1 = lb.Server(1)
    server2 = lb.Server(2)
    server1.add(5)
    server2.add(3)
    server2.add(2)
    assert lb.check_tasks(server1, server2) is True


def test_should_return_false_when_server2_has_longer_tasks_than_server1():
    server1 = lb.Server(1)
    server2 = lb.Server(2)
    server1.add(1)
    server2.add(3)
    server2.add(2)
    assert lb.check_tasks(server1, server2) is False


def test_should_start_one_new_server_on_servers_list():
    servers = []
    umax = 5
    lb.start_new_server(servers, umax)
    assert len(servers) == 1


def test_should_return_the_available_server_when_one_is_available_and_one_is_full():
    umax = 2
    server1 = lb.Server(umax)
    server2 = lb.Server(umax)
    server1.add(1)
    server1.add(3)
    server2.add(2)
    assert lb.get_best_server([server1, server2], umax) == server2


def test_should_return_the_server_with_longer_tasks_when_both_servers_are_available():
    umax = 2
    server1 = lb.Server(umax)
    server2 = lb.Server(umax)
    server1.add(3)
    server2.add(2)
    assert lb.get_best_server([server1, server2], umax) == server1


def test_should_return_new_server_when_both_servers_are_full():
    umax = 2
    server = lb.Server(umax)
    server.add(1)
    server.add(3)
    assert isinstance(lb.get_best_server([server], umax), lb.Server) is True


def test_should_add_new_user_to_server_with_longer_tasks_when_both_servers_are_available():
    umax = 2
    ttask = 5
    server1 = lb.Server(umax)
    server2 = lb.Server(umax)
    server1.add(3)
    server2.add(2)
    lb.users_to_server([server1, server2], 1, umax, ttask)
    assert server1.users == [3, 5]


def test_should_add_two_users_one_on_each_server_when_both_servers_are_available():
    umax = 2
    ttask = 5
    server1 = lb.Server(umax)
    server2 = lb.Server(umax)
    server1.add(3)
    server2.add(2)
    lb.users_to_server([server1, server2], 2, umax, ttask)
    assert server1.users == [3, 5] and server2.users == [2, 5]


def test_should_return_total_cost_when_one_user():
    ttask = 1
    umax = 1
    users = [1]
    base_cost = 1
    assert lb.main_loop(ttask, umax, users, base_cost) == ([[1], []], 1)


def test_should_return_total_cost_when_more_users():
    ttask = 4
    umax = 2
    users = [1, 3, 0, 1, 0, 1]
    base_cost = 1
    assert lb.main_loop(ttask, umax, users, base_cost) == ([[1], [2, 2], [2, 2], [2, 2, 1], [1, 2, 1], [2], [2], [1], [1], []], 15)


@pytest.mark.parametrize("ttask, umax, users, base_cost", [(10, 10, [5, 2, 6, 5, 10], 1)])
def test_should_return_total_cost_when_more_users_with_ttask_and_umax_at_max_limit(ttask, umax, users, base_cost):
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


def test_should_return_read_data_from_input_file():
    ttask = 4
    umax = 2
    users = [1, 3, 0, 1, 0, 1]
    path = 'test/input.txt'
    data = lb.read_file(path)
    assert data == (ttask, umax, users)
