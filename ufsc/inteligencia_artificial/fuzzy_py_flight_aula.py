# https://pythonhosted.org/scikit-fuzzy/

from numpy import array, arange, maximum, matrix, clip, asarray, zeros, append, \
    concatenate, linspace
from skfuzzy import trimf, trapmf, interp_membership, defuzz
import skfuzzy.control
from fuzzy_control import control_signal

from matplotlib.pyplot import plot, show, subplots, axis, pause, legend, xlabel, \
    ylabel
from matplotlib.axes import *

n_intervals = 200
angle_range = (-0.20943951, 0.20943951)
angular_velocity_range = (-3.5, 3.5)

angle = linspace(-100, 100, n_intervals)
angular_velocity = linspace(-100, 100, n_intervals)
force = linspace(-100, 100, n_intervals)

angle_large_pos = trapmf(angle, [50, 90, 100, 101])
angle_medium_pos = trimf(angle, [0, 50, 100])
angle_near_zero = trimf(angle, [-50, 0, 50])
angle_medium_neg = trimf(angle, [-100, -50, 0])
angle_large_neg = trapmf(angle, [-101, -100, -90, -50])

plot(angle, angle_large_pos, label='Angle Large Pos (ALP)')
plot(angle, angle_medium_pos, label='Angle Medium Pos (AMP)')
plot(angle, angle_near_zero, label='Angle Near Zero (ANZ)')
plot(angle, angle_medium_neg, label='Angle Medium Neg (AMN)')
plot(angle, angle_large_neg, label='Angle Large Neg (ALN)')

xlabel('Angle (rad)')
ylabel('Membership')
legend(loc='best')
show()

ang_vel_large_pos = trapmf(angular_velocity, [50, 90, 100, 101])
ang_vel_medium_pos = trimf(angular_velocity, [0, 50, 90])
ang_vel_zero = trimf(angular_velocity, [-50, 0, 50])
ang_vel_medium_neg = trimf(angular_velocity, [-90, -50, 0])
ang_vel_large_neg = trapmf(angular_velocity, [-101, -100, -90, -50])

plot(angular_velocity, ang_vel_large_pos, label='Vel Large Positive (VLP)')
plot(angular_velocity, ang_vel_medium_pos, label='Vel Medium Positive (VMP)')
plot(angular_velocity, ang_vel_zero, label='Vel Zero (VZ)')
plot(angular_velocity, ang_vel_medium_neg, label='Vel Medium Negative (VMN)')
plot(angular_velocity, ang_vel_large_neg, label='Vel Large Negative (VLM)')
xlabel('Velocity (rad/s)')
ylabel('Membership')
legend(loc='best')
show()


force_left = trapmf(force, [-100, -100, 0, 0])
force_right = trapmf(force, [0, 0, 100, 100])

force_matrix = array(
    [
        trapmf(force, [-100, -100, 0, 0]),
        trapmf(force, [0, 0, 100, 100])
     ]
)

plot(force, force_left, label='Force Left (FL)')
plot(force, force_right, label='Force Right (FR)')
xlabel('Force (N)')
ylabel('Membership')
legend(loc='best')
show()


fam_table = ([[0, 4, 2],  # ALP and VLP = Z
              [0, 3, 3],  # ALP and VMP = DS
              [0, 2, 4],  # ALP and VZ = DL
              [0, 1, 4],  # ALP and VMN = ?
              [0, 0, 4],  # ALP and VLM = ?

              [1, 4, 3],  # AMP and VLP = US
              [1, 3, 2],  # AMP and VMP = Z
              [1, 2, 3],  # AMP and VZ = DS
              [1, 1, 3],  # AMP and VMN = ?
              [1, 0, 3],  # AMP and VLM = ?

              [2, 4, 0],  # ANZ and VLP = ?
              [2, 3, 1],  # ANZ and VMP = ?
              [2, 2, 1],  # ANZ and VZ = ?
              [2, 1, 3],  # ANZ and VMN = ?
              [2, 0, 3],  # ANZ and VLM = DL

              [3, 4, 0],  # AMN and VLP = ?
              [3, 3, 0],  # AMN and VMP = ?
              [2, 2, 1],  # AMN and VZ = ?
              [2, 1, 1],  # AMN and VMN = DS
              [2, 0, 1],  # AMN and VLM = DS

              [3, 4, 0],  # ALN and VLP = ?
              [3, 3, 0],  # ALN and VMP = ?
              [2, 2, 1],  # ALN and VZ = ?
              [2, 1, 1],  # ALN and VMN = DS
              [2, 0, 1]  # ALN and VLM = DS
              ])

v_height = 1000
v_velocity = -20

MAX = 1000
i = 0
heights = [
    v_height]  # list of heights along the episodes - start with the initial height
velocities = [
    v_velocity]  # list of velocities along the episodes - start with the initial velocity

for i in range(0, MAX):
    control = control_signal(2,  # input_size
                             array([v_height, v_velocity]),  # inputs
                             array([x_height, x_velocity]),
                             x_force,
                             array([height_array, velocity_array]),
                             # membership
                             force_matrix,
                             fam_table
                             )

    print(i, " - altura: ", v_height, "; velocidade: ", v_velocity,
          "; altura final: ", v_height + v_velocity, "; velocidade final: ",
          v_velocity + control)

    v_height = v_height + v_velocity
    v_velocity = v_velocity + control
    heights = append(heights, v_height)
    velocities = append(velocities, abs(v_velocity))
    if v_height < 0:
        print("*********** Altura Negativa **************")
        print(v_height)
        break

print(heights)
plot(heights)
plot(velocities)
show()
########################
