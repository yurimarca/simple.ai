# speed range: 1.5 - 4
import math


class Reward:
    def __init__(self):
        self.first_racingpoint_index = 0

    def reward_function(self, params):

        ################## HELPER FUNCTIONS ###################

        def dist_2_points(x1, x2, y1, y2):
            return abs(abs(x1-x2)**2 + abs(y1-y2)**2)**0.5

        def closest_2_racing_points_index(racing_coords, car_coords):

            # Calculate all distances to racing points
            distances = []
            for i in range(len(racing_coords)):
                distance = dist_2_points(x1=racing_coords[i][0], x2=car_coords[0],
                                         y1=racing_coords[i][1], y2=car_coords[1])
                distances.append(distance)

            # Get index of the closest racing point
            closest_index = distances.index(min(distances))

            # Get index of the second closest racing point
            distances_no_closest = distances.copy()
            distances_no_closest[closest_index] = 999
            second_closest_index = distances_no_closest.index(
                min(distances_no_closest))

            return [closest_index, second_closest_index]

        def dist_to_racing_line(closest_coords, second_closest_coords, car_coords):

            # Calculate the distances between 2 closest racing points
            a = abs(dist_2_points(x1=closest_coords[0],
                                  x2=second_closest_coords[0],
                                  y1=closest_coords[1],
                                  y2=second_closest_coords[1]))

            # Distances between car and closest and second closest racing point
            b = abs(dist_2_points(x1=car_coords[0],
                                  x2=closest_coords[0],
                                  y1=car_coords[1],
                                  y2=closest_coords[1]))
            c = abs(dist_2_points(x1=car_coords[0],
                                  x2=second_closest_coords[0],
                                  y1=car_coords[1],
                                  y2=second_closest_coords[1]))

            # Calculate distance between car and racing line (goes through 2 closest racing points)
            # try-except in case a=0 (rare bug in DeepRacer)
            try:
                distance = abs(-(a**4) + 2*(a**2)*(b**2) + 2*(a**2)*(c**2) -
                               (b**4) + 2*(b**2)*(c**2) - (c**4))**0.5 / (2*a)
            except:
                distance = b

            return distance

        # Calculate which one of the closest racing points is the next one and which one the previous one
        def next_prev_racing_point(closest_coords, second_closest_coords, car_coords, heading):

            # Virtually set the car more into the heading direction
            heading_vector = [math.cos(math.radians(
                heading)), math.sin(math.radians(heading))]
            new_car_coords = [car_coords[0]+heading_vector[0],
                              car_coords[1]+heading_vector[1]]

            # Calculate distance from new car coords to 2 closest racing points
            distance_closest_coords_new = dist_2_points(x1=new_car_coords[0],
                                                        x2=closest_coords[0],
                                                        y1=new_car_coords[1],
                                                        y2=closest_coords[1])
            distance_second_closest_coords_new = dist_2_points(x1=new_car_coords[0],
                                                               x2=second_closest_coords[0],
                                                               y1=new_car_coords[1],
                                                               y2=second_closest_coords[1])

            if distance_closest_coords_new <= distance_second_closest_coords_new:
                next_point_coords = closest_coords
                prev_point_coords = second_closest_coords
            else:
                next_point_coords = second_closest_coords
                prev_point_coords = closest_coords

            return [next_point_coords, prev_point_coords]

        def racing_direction_diff(closest_coords, second_closest_coords, car_coords, heading):

            # Calculate the direction of the center line based on the closest waypoints
            next_point, prev_point = next_prev_racing_point(closest_coords,
                                                            second_closest_coords,
                                                            car_coords,
                                                            heading)

            # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
            track_direction = math.atan2(
                next_point[1] - prev_point[1], next_point[0] - prev_point[0])

            # Convert to degree
            track_direction = math.degrees(track_direction)

            # Calculate the difference between the track direction and the heading direction of the car
            direction_diff = abs(track_direction - heading)
            if direction_diff > 180:
                direction_diff = 360 - direction_diff

            return direction_diff

        #################### RACING LINE ######################

        # Optimal racing line for the Spain track
        # Each row: [x,y,speed,timeFromPreviousPoint]
        racing_track = [
                [3.08361, 0.73225, 4.0, 0.03579],
                [3.22751, 0.72144, 4.0, 0.03608],
                [3.37248, 0.71326, 4.0, 0.0363],
                [3.51823, 0.70748, 4.0, 0.03646],
                [3.66443, 0.70391, 4.0, 0.03656],
                [3.81081, 0.7024, 4.0, 0.0366],
                [3.95711, 0.70286, 4.0, 0.03658],
                [4.10311, 0.70522, 4.0, 0.03651],
                [4.24864, 0.70943, 4.0, 0.0364],
                [4.39353, 0.71545, 4.0, 0.03625],
                [4.53767, 0.72324, 4.0, 0.03609],
                [4.68099, 0.73276, 4.0, 0.03591],
                [4.8234, 0.74402, 4.0, 0.03571],
                [4.96486, 0.75698, 4.0, 0.03551],
                [5.10529, 0.77166, 4.0, 0.0353],
                [5.24463, 0.78811, 4.0, 0.03508],
                [5.38276, 0.80643, 3.5, 0.03981],
                [5.51955, 0.82678, 3.1, 0.04461],
                [5.65473, 0.84943, 2.7, 0.05077],
                [5.788, 0.87478, 2.4, 0.05652],
                [5.91893, 0.90327, 2.1, 0.06381],
                [6.04702, 0.93546, 1.9, 0.06951],
                [6.17154, 0.97208, 1.6, 0.08112],
                [6.29155, 1.01401, 1.6, 0.07945],
                [6.40587, 1.06223, 1.6, 0.07755],
                [6.51297, 1.1178, 1.6, 0.07541],
                [6.61088, 1.18175, 1.4, 0.08353],
                [6.69749, 1.25464, 1.4, 0.08086],
                [6.76876, 1.33731, 1.4, 0.07796],
                [6.82424, 1.4274, 1.4, 0.07558],
                [6.8666, 1.52206, 1.4, 0.07407],
                [6.89352, 1.62052, 1.4, 0.07291],
                [6.90068, 1.72121, 1.5, 0.06729],
                [6.89052, 1.82139, 1.6, 0.06294],
                [6.86612, 1.91969, 1.6, 0.0633],
                [6.82852, 2.01513, 1.6, 0.06411],
                [6.77499, 2.10549, 1.7, 0.06179],
                [6.70728, 2.18971, 1.9, 0.05687],
                [6.62776, 2.26765, 2.1, 0.05302],
                [6.53827, 2.3395, 2.3, 0.0499],
                [6.44047, 2.40574, 2.6, 0.04543],
                [6.3358, 2.46697, 3.0, 0.04042],
                [6.22563, 2.52397, 3.6, 0.03446],
                [6.11142, 2.57775, 4.0, 0.03156],
                [5.99446, 2.62928, 4.0, 0.03195],
                [5.87612, 2.67968, 4.0, 0.03216],
                [5.75042, 2.73411, 4.0, 0.03424],
                [5.62477, 2.78939, 4.0, 0.03432],
                [5.49919, 2.84542, 4.0, 0.03438],
                [5.37371, 2.90216, 4.0, 0.03443],
                [5.24835, 2.95957, 4.0, 0.03447],
                [5.12313, 3.01765, 4.0, 0.03451],
                [4.99808, 3.07641, 4.0, 0.03454],
                [4.87322, 3.13584, 4.0, 0.03457],
                [4.74858, 3.19598, 4.0, 0.0346],
                [4.62418, 3.2568, 4.0, 0.03462],
                [4.50006, 3.31831, 4.0, 0.03463],
                [4.37624, 3.38047, 4.0, 0.03464],
                [4.25275, 3.44322, 4.0, 0.03463],
                [4.12962, 3.50651, 4.0, 0.03461],
                [4.00685, 3.57026, 4.0, 0.03458],
                [3.88443, 3.63438, 4.0, 0.03455],
                [3.76232, 3.6988, 3.6, 0.03835],
                [3.64044, 3.76341, 3.1, 0.0445],
                [3.52115, 3.82646, 2.7, 0.04997],
                [3.40164, 3.88822, 2.7, 0.04982],
                [3.28169, 3.94754, 2.7, 0.04956],
                [3.16109, 4.00323, 2.7, 0.0492],
                [3.03958, 4.05379, 2.7, 0.04874],
                [2.9171, 4.09771, 2.7, 0.04819],
                [2.79379, 4.13303, 3.1, 0.04138],
                [2.67016, 4.16177, 3.0, 0.04231],
                [2.54643, 4.18442, 2.9, 0.04337],
                [2.42279, 4.20132, 2.6, 0.048],
                [2.29937, 4.21264, 2.4, 0.05164],
                [2.17638, 4.21829, 2.1, 0.05863],
                [2.05402, 4.21805, 1.9, 0.0644],
                [1.9326, 4.21151, 1.7, 0.07153],
                [1.8125, 4.19823, 1.5, 0.08056],
                [1.69436, 4.17713, 1.5, 0.08001],
                [1.57913, 4.14691, 1.5, 0.07941],
                [1.4683, 4.10593, 1.5, 0.07878],
                [1.36401, 4.05238, 1.5, 0.07815],
                [1.27, 3.98374, 1.5, 0.0776],
                [1.19023, 3.89932, 1.7, 0.06832],
                [1.12455, 3.80255, 1.8, 0.06497],
                [1.07141, 3.69647, 2.0, 0.05932],
                [1.02948, 3.58309, 2.2, 0.05495],
                [0.99779, 3.4638, 2.4, 0.05143],
                [0.97527, 3.33988, 2.6, 0.04844],
                [0.9613, 3.2123, 2.8, 0.04584],
                [0.95535, 3.08196, 2.9, 0.04499],
                [0.9569, 2.94973, 3.1, 0.04266],
                [0.96548, 2.81642, 3.2, 0.04174],
                [0.98068, 2.68278, 3.3, 0.04076],
                [1.00217, 2.5495, 3.4, 0.03971],
                [1.02963, 2.41715, 3.4, 0.03975],
                [1.06273, 2.28625, 3.2, 0.0422],
                [1.10113, 2.15718, 3.0, 0.04489],
                [1.1445, 2.03026, 2.7, 0.04968],
                [1.19253, 1.90571, 2.4, 0.05562],
                [1.24523, 1.78391, 2.1, 0.0632],
                [1.30258, 1.66517, 1.9, 0.0694],
                [1.36506, 1.5502, 1.9, 0.06887],
                [1.43323, 1.43984, 1.9, 0.06827],
                [1.50803, 1.33542, 1.9, 0.06761],
                [1.59055, 1.23859, 1.9, 0.06696],
                [1.68237, 1.15178, 1.9, 0.0665],
                [1.7852, 1.07817, 2.2, 0.05748],
                [1.89578, 1.0147, 2.4, 0.05313],
                [2.0127, 0.96002, 2.6, 0.04965],
                [2.13489, 0.91298, 2.9, 0.04515],
                [2.26145, 0.87251, 3.2, 0.04152],
                [2.39176, 0.8379, 3.5, 0.03852],
                [2.5253, 0.8085, 3.8, 0.03599],
                [2.66163, 0.7837, 4.0, 0.03464],
                [2.80034, 0.76301, 4.0, 0.03506],
                [2.94112, 0.746, 4.0, 0.03545]]
            
            
        # planned speed based on waypoints
        # manually adjust the list for better performance, e.g. lower the speed before turning
        above_three_five = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 
                        41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 
                            93, 94, 95, 96, 
                            113, 114, 115, 116, 117, 118]
        above_three = [12, 40, 70, 
                       91, 92, 97, 98, 
                       111, 112]
        above_two_five = [13, 14, 39,
                          64, 65, 66, 67, 68, 69, 71, 72, 73, 74, 
                          88, 89, 90,
                          99, 110]
        above_two = [37, 38, 
                     75, 76, 86, 87, 
                     100, 101, 108, 109]
        below_two = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 
                     77, 78, 79, 80, 81, 82, 83, 84, 85, 
                     102, 103, 104, 105, 106, 107]
        # TO-DO: Here we could use a function instead of several if statements,
        #However, we can't imediatly assume it will represent a linear function.
        
        
        # planned speed based on waypoints
        # observe which side the car is expected to run at
        right_track = [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
        center_track = [118, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        left_track = [i for i in range(0, 119) if i not in right_track + center_track]

        # obvious sides
        strong_left = [
                    16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                    41, 42, 43, 44,
                    65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
                    90, 91,
                    101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114
                ]
        strong_right = [49, 50, 51, 52, 53, 54, 55, 56, 57, 58]
        
        ################## INPUT PARAMETERS ###################

        # Read all input parameters
        x = params['x']
        y = params['y']
        distance_from_center = params['distance_from_center']
        is_left_of_center = params['is_left_of_center']
        heading = params['heading']
        progress = params['progress']
        steps = params['steps']
        speed = params['speed']
        steering_angle = abs(params['steering_angle'])
        track_width = params['track_width']
        is_offtrack = params['is_offtrack']

        ############### OPTIMAL X,Y,SPEED,TIME ################

        # Get closest indexes for racing line (and distances to all points on racing line)
        closest_index, second_closest_index = closest_2_racing_points_index(
            racing_track, [x, y])

        # Get optimal [x, y, speed, time] for closest and second closest index
        optimals = racing_track[closest_index]
        optimals_second = racing_track[second_closest_index]

        if steps == 1:
            self.first_racingpoint_index = closest_index

        ################ REWARD AND PUNISHMENT ################
        reward = 1e-3

        # Zero reward if off track ##
        if is_offtrack is True:
            return reward

        # Zero reward if obviously wrong direction (e.g. spin)
        direction_diff = racing_direction_diff(
            optimals[0:2], optimals_second[0:2], [x, y], heading)
        if direction_diff > 30:
            return reward

        # Reward if car goes close to optimal racing line
        def get_distance_reward(threshold, distance, multiplier):
            distance_reward = max(0, 1 - (distance / threshold))

            return distance_reward * multiplier

        DIST_THRESH = track_width * 0.5
        dist = dist_to_racing_line(optimals[0:2], optimals_second[0:2], [x, y])

        if (distance_from_center < 0.01 * track_width):
            if closest_index in center_track:
                reward += get_distance_reward(DIST_THRESH, dist, 1)
        elif is_left_of_center:
            if closest_index in left_track:
                reward += get_distance_reward(DIST_THRESH, dist, 1)
            if closest_index in strong_left:
                reward += get_distance_reward(DIST_THRESH, dist, 5)
        else:
            if closest_index in right_track:
                reward += get_distance_reward(DIST_THRESH, dist, 1)
            if closest_index in strong_right:
                reward += get_distance_reward(DIST_THRESH, dist, 5)

        def get_speed_reward(ceiling, threshold, diff):
            return ceiling - diff/threshold

        # Reward if speed falls within optimal range
        PENALTY_RATIO = 0.9
        SPEED_DIFF_NO_REWARD = 1
        speed_diff = abs(optimals[2]-speed)
        if speed_diff > SPEED_DIFF_NO_REWARD:
            return 1e-3

        if closest_index in above_three_five:
            if speed >= 3.5:
                reward += get_speed_reward(0.5, SPEED_DIFF_NO_REWARD, speed_diff)
            if steering_angle > 3:
                reward *= PENALTY_RATIO
        elif closest_index in above_three:
            if speed >= 3:
                reward += get_speed_reward(0.5, SPEED_DIFF_NO_REWARD, speed_diff)
            if steering_angle > 8:
                reward *= PENALTY_RATIO
        elif closest_index in above_two_five:
            if speed >= 2.5:
                reward += get_speed_reward(0.8, SPEED_DIFF_NO_REWARD, speed_diff)
            if steering_angle > 15:
                reward *= PENALTY_RATIO
        elif closest_index in above_two:
            if speed >= 2:
                reward += get_speed_reward(1, SPEED_DIFF_NO_REWARD, speed_diff)
        else:
            if speed < 2:
                reward += get_speed_reward(3, SPEED_DIFF_NO_REWARD, speed_diff)

        # Incentive for finishing the lap in less steps ##
        REWARD_FOR_FASTEST_TIME = 2000 # should be adapted to track length and other rewards
        TARGET_STEPS = 110
        if progress == 100:
            reward += REWARD_FOR_FASTEST_TIME / (steps - TARGET_STEPS)

        #################### RETURN REWARD ####################

        # Always return a float value
        return float(reward)


reward_object = Reward()


def reward_function(params):
    return reward_object.reward_function(params)