# -*- coding: utf-8 -*-
"""
Main load balancer file for Diebold Nixdorf practical test.

Created on Wed Jun 10 08:17:56 2020

@author: rcbadiale
"""


class Server(object):
    def __init__(self, umax):
        self.umax = umax  # Max users simultaneously on server
        self.users = []  # Current users on server

    def available(self):
        """Check server availability. """
        if self.umax - len(self.users) > 0:
            return True
        else:
            return False

    def add(self, ttask):
        """Add user to server with ticks to go. """
        if self.available():
            self.users.append(ttask)
            return True
        else:
            return False

    def clear(self):
        """Clear users with finished tasks. """
        self.users = [u for u in self.users if u != 0]

    def tick(self):
        """Run ticks on tasks and clean finished tasks. """
        self.users = [u - 1 for u in self.users]
        self.clear()

    def max_task(self):
        """Check the biggest number of ticks on a task on this server. """
        if len(self.users) > 0:
            return max(self.users)
        else:
            return 0


def read_file(path):
    """Read input file from path. """
    try:
        with open(path, 'r') as file:
            ttask = int(file.readline().strip('\r\n'))
            umax = int(file.readline().strip('\r\n'))
            new_users = [int(f.strip('\r\n')) for f in file]
        return ttask, umax, new_users
    except IOError:
        print('An error occurred while reading the file.')


def run_tick(servers):
    """Run one tick on all servers tasks. """
    [s.tick() for s in servers]
    return


def check_tasks(server, old_server):
    """Check if the current server will live longer than the older selected one. """
    return server.max_task() > old_server.max_task() or server.max_task() == 0


def start_new_server(servers, max_users):
    """Start a new server with defined max users. """
    servers.append(Server(max_users))
    return


def get_best_server(servers, umax):
    """Return the server which should receive the new user. """
    to_add = ''
    for s in servers:
        if s.available():
            if to_add != '':
                if check_tasks(s, to_add):
                    to_add = s
            else:
                to_add = s
        elif s is servers[-1]:  # If it is the last server and none was available, start a new one
            start_new_server(servers, umax)
    return to_add


def user_to_server(servers, umax, ttask):
    """Add one new user to the best server. """
    get_best_server(servers, umax).add(ttask)


def write_file(path, data, total_cost):
    """Write the output file to path. """
    output = []
    for d in data:
        line = ''
        for i in d:
            line += str(i) + ','
        output.append(line[:-1])
    with open(path, 'w') as file:
        for line in output:
            if line == '':
                file.write('0\n')
            else:
                file.write(line + '\n')
        file.write(str(total_cost))
    return


def main_loop(ttask, umax, queue, base_cost):
    tick = 0
    total_cost = 0
    servers = []
    output = []
    while len(queue) > 0 or len(servers) > 0:
        tick += 1
        run_tick(servers)
        if len(queue) > 0:
            add = queue.pop(0)
            if add > 0 and len(servers) == 0:  # First run
                start_new_server(servers, umax)
                servers[-1].add(ttask)
            elif add > 0:
                for user in range(add):
                    user_to_server(servers, umax, ttask)
        to_remove = [s for s in servers if s.users == []]
        [servers.remove(s) for s in to_remove]
        total_cost += len(servers) * base_cost
        # print('tick', tick, 'servers', [len(s.users) for s in servers], 'total_cost', total_cost)
        output.append([len(s.users) for s in servers])
    return output, total_cost


def main():
    base_cost = 1  # Cost per tick
    input_path = 'main/input.txt'  # Input file
    output_path = 'main/output.txt'  # Output file
    ttask, umax, new_users = read_file(input_path)
    output, cost = main_loop(ttask, umax, new_users, base_cost)
    # write_file(output_path, output, cost)


if __name__ == '__main__':
    main()
