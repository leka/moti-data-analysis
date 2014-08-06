import sys
import json
from collections import OrderedDict
import matplotlib.pyplot as plt


PLOT_MOTORS, PLOT_LEDS, PLOT_SENSORS = 1, 2, 4


class MotorData:
    def __init__(self, motors):
        self.right_speed = motors[1] * (1 if motors[0] == 1 else -1)
        self.left_speed = motors[3] * (1 if motors[2] == 1 else -1)


class LedData:
    def __init__(self, leds):
        self.led_indicator = leds[0]
        self.red, self.green, self.blue = leds[1:]


class SensorsData:
    def __init__(self, sensors):
        self.accel_x, self.accel_y, self.accel_z = sensors[:3]
        self.gyro_y, self.gyro_p, self.gyro_r = sensors[3:]


class Data:
    def __init__(self, motors, leds, sensors):
        if motors[0] != 'M' or leds[0] != 'L' or sensors[0] != 'S':
            print('Error, malformed data (Motor, Led, Sensors).')
            sys.exit(0)

        self.motors = [int(x) for x in motors[1:]]
        self.leds = [int(x) for x in leds[1:]]
        self.sensors = [float(x) for x in sensors[1:]]

        self.motor_data = MotorData(self.motors)
        self.led_data = LedData(self.leds)
        self.sensors_data = SensorsData(self.sensors)


def read_data(filepath):
    data = OrderedDict()

    with open(filepath) as f:
        i = 0
        while True:
            infos = [f.readline().split(',') for _ in range(4)]
            time, motors, leds, sensors = infos

            if len(time) == 0 or time[0] == '':
                break

            if time[0] != 'A':
                print('Error, malformed data (%d).' % i)

            data[int(time[1])] = Data(motors, leds, sensors)
            i += 1

    return data


def find_value(time, data):
    '''
        Returns the items whose time is the closest to `time`
    '''

    items = data.items()
    a, b = 0, len(data) - 1

    while a != b:
        mid = (a + b) / 2

        if abs(items[mid][0] - time) > abs(items[mid + 1][0] - time):
            a = mid + 1
        else:
            b = mid

    return items[a]


def plot(data, config):
    items = data.items()

    t = [item[0] for item in items]

    motors, leds, sensors = config['motors'], config['leds'], config['sensors']

    # Motors
    if motors['right'] or motors['left']:
        right_speed = [item[1].motor_data.right_speed for item in items]
        left_speed = [item[1].motor_data.left_speed for item in items]

        plt.figure(1)
        plt.xlabel('time (ms)')
        plt.ylabel('speed')

        if motors['right']:
            plt.plot(t, right_speed, label='Right motor')
        
        if motors['left']:
            plt.plot(t, left_speed, label='Left motor')
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4,
                   ncol=2, mode="expand", borderaxespad=0.)
        plt.savefig('plot/motors.png', format='png')

    # Leds
    if leds:
        pass

    # Accelerometer
    acc = sensors['acc']
    if acc['X'] or acc['Y'] or acc['Z']:
        accel_x = [item[1].sensors_data.accel_x for item in items]
        accel_y = [item[1].sensors_data.accel_y for item in items]
        accel_z = [item[1].sensors_data.accel_z for item in items]

        plt.figure(2)
        plt.subplot(212)
        plt.xlabel('time (ms)')
        plt.ylabel('amplitude')

        if acc['X']:
            plt.plot(t, accel_x, label="AccX")
        
        if acc['Y']:
            plt.plot(t, accel_y, label="AccY")
        
        if acc['Z']:
            plt.plot(t, accel_z, label="AccZ")
    
        plt.legend(bbox_to_anchor=(0.0, 1.02, 1.0, 0.102), loc=4,
                   ncol=2, mode="expand", borderaxespad=0.0)
        plt.savefig('plot/accelerometer.png', format='png')

    # Gyroscope
    gyr = sensors['gyr']
    if gyr['Y'] or gyr['P'] or gyr['R']:
        gyr_y = [item[1].sensors_data.gyro_y for item in items]
        gyr_p = [item[1].sensors_data.gyro_p for item in items]
        gyr_r = [item[1].sensors_data.gyro_r for item in items]

        plt.figure(3)
        plt.subplot(211)
        plt.xlabel('time (ms)')
        plt.ylabel('amplitude')

        if gyr['Y']:
            plt.plot(t, gyr_y, label="GyrY")
        
        if gyr['P']:
            plt.plot(t, gyr_p, label="GyrP")
        
        if gyr['R']:
            plt.plot(t, gyr_r, label="GyrR")
    
        plt.legend(bbox_to_anchor=(0.0, 1.02, 1.0, 0.102), loc=4,
                   ncol=2, mode="expand", borderaxespad=0.0)
        plt.savefig('plot/gyroscope.png', format='png')

    plt.show()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python data-analysis.py input_data_filepath')
        sys.exit(0)

    input_file = sys.argv[1]

    with open('config.json') as config_file:
        config = json.loads(config_file.read())

    data = read_data(input_file)

    plot(data, config)
