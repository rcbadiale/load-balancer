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


def test_get_best_server_for_new_user_full_server():
    umax = 2
    server = lb.Server(umax)
    server.add(1)
    server.add(3)
    assert isinstance(lb.get_best_server([server], umax), lb.Server) is True
