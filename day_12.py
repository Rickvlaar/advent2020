import util

movement_list = util.parse_file_as_list('input_files/day_12.txt')


class Ship:
    def __init__(self, directions=movement_list):
        self.directions = [(direction[0], int(direction[1:])) for direction in directions]
        self.position = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
        self.coordinates = {'W': 0, 'N': 0}
        self.waypoint_position = {'N': 1, 'S': 0, 'E': 10, 'W': 0}
        self.waypoint_coordinates = {'E': 10, 'N': 1}
        self.wind_direction_dict = {0: 'N', 90: 'E', 180: 'S', 270: 'W'}
        self.heading = 90  # initial heading is east

    def set_sail(self):  # just follow the map without thinking
        for action, value in self.directions:
            if action in self.position.keys():
                self.position[action] += value
            elif action == 'R':
                self.heading = (self.heading + value) % 360
            elif action == 'L':
                self.heading = (self.heading - value) % 360
            elif action == 'F':
                self.position[self.wind_direction_dict.get(self.heading)] += value
        print('Our current Manhatten position is: ' + str(abs(self.position.get('N') - self.position.get('S'))) + ', ' + str(abs(self.position.get('W') - self.position.get('E'))))

    def set_waypoint_coordinates(self):
        self.waypoint_coordinates.clear()
        y_wind_direction = 'N' if self.waypoint_position['N'] > self.waypoint_position['S'] else 'S'
        x_wind_direction = 'W' if self.waypoint_position['W'] > self.waypoint_position['E'] else 'E'
        y_value = abs(self.waypoint_position.get('N') - self.waypoint_position.get('S'))
        x_value = abs(self.waypoint_position.get('W') - self.waypoint_position.get('E'))
        self.waypoint_coordinates = {x_wind_direction: x_value, y_wind_direction: y_value}

    def hunt_the_whale(self):  # the waypoint is our whale
        for action, value in self.directions:
            if action in self.waypoint_position.keys():
                self.waypoint_position[action] += value
            elif (action == 'R' and value == 90) or (action == 'L' and value == 270):
                self.waypoint_position = {'N': self.waypoint_position['W'],
                                          'E': self.waypoint_position['N'],
                                          'S': self.waypoint_position['E'],
                                          'W': self.waypoint_position['S']}
            elif (action == 'R' and value == 180) or (action == 'L' and value == 180):
                self.waypoint_position = {'N': self.waypoint_position['S'],
                                          'E': self.waypoint_position['W'],
                                          'S': self.waypoint_position['N'],
                                          'W': self.waypoint_position['E']}
            elif (action == 'R' and value == 270) or (action == 'L' and value == 90):
                self.waypoint_position = {'N': self.waypoint_position['E'],
                                          'E': self.waypoint_position['S'],
                                          'S': self.waypoint_position['W'],
                                          'W': self.waypoint_position['N']}
            elif action == 'F':
                self.set_waypoint_coordinates()
                for wind_direction, units in self.waypoint_coordinates.items():
                    self.position[wind_direction] += (value * units)
        print('Our current Manhatten position is: ' + str(abs(self.position.get('N') - self.position.get('S'))) + ', ' + str(abs(self.position.get('W') - self.position.get('E'))))
