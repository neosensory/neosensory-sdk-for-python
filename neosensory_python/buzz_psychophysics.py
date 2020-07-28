import math


def get_motor_intensity(linear_intensity, min_intensity, max_intensity):
    if linear_intensity <= 0:
        return min_intensity
    elif linear_intensity >= 1:
        return max_intensity
    else:
        return int(math.expm1(linear_intensity) / (math.e - 1)
         * (max_intensity - min_intensity) + min_intensity)


def get_buzz_illusion_activations(linear_intensity, location,
        min_intensity, max_intensity, num_motors):
    motor_frame = [0, 0, 0, 0]
    if linear_intensity <= 0:
        return motor_frame
    motor_intensity = get_motor_intensity(linear_intensity,
        min_intensity, max_intensity)
    motor_location = location * (num_motors - 1)
    lower_motor_index = int(math.floor(motor_location))
    upper_motor_index = int(math.ceil(motor_location))
    lower_distance = abs(motor_location - lower_motor_index)
    upper_distance = abs(motor_location - upper_motor_index)
    lower_activation = int(motor_intensity * math.sqrt(1 - lower_distance))
    upper_activation = int(motor_intensity * math.sqrt(1 - upper_distance))
    motor_frame[lower_motor_index] = lower_activation
    motor_frame[upper_motor_index] = upper_activation
    return motor_frame
