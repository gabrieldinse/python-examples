# https://pythonhosted.org/scikit-fuzzy/

import requests
from numpy import array, arange, maximum, matrix, clip, asarray, zeros, append, \
    concatenate, linspace
from skfuzzy import trimf, trapmf, interp_membership, defuzz
import skfuzzy.control
from fuzzy_control import control_signal

from matplotlib.pyplot import plot, show, subplots, axis, pause, legend, xlabel, \
    ylabel
from matplotlib.axes import *


def init_state():
    response = requests.get(url="http://localhost:8081/?state=0").json()
    state = response['state']
    done = False
    return done, state


def act(action):
    response = requests.get(url="http://localhost:8081/?control=" + str(action)).json()
    state = response['state']
    done = response['done']
    return done, state


def normalize_state(factor, state):
    curr_position = state[0]
    curr_angle = state[2]
    curr_angular_vel = state[3]
    curr_position = curr_position / max(position_range) * factor
    curr_angle = curr_angle / max(angle_range) * factor
    curr_angular_vel = curr_angular_vel / max(angular_velocity_range) * factor
    return curr_position, curr_angle, curr_angular_vel


n_intervals = 200
angle_range = (-0.20943951, 0.20943951)
angular_velocity_range = (-3.5, 3.5)
position_range = (-2.4, 2,4)

position = linspace(-100, 100, n_intervals)
angle = linspace(-100, 100, n_intervals)
angular_velocity = linspace(-100, 100, n_intervals)
force = linspace(-100, 100, n_intervals)


# Posicao --------------------------------------
position_left = trapmf(force, [-100, -100, 0, 0])
position_right = trapmf(force, [0, 0, 100, 100])

position_array = array(
    [
        trapmf(position, [-100, -100, 0, 0]),
        trapmf(position, [0, 0, 100, 100])
     ]
)

plot(force, position_left, label='Positon Left (PL)')
plot(force, position_right, label='Position Right (PR)')
xlabel('Position')
ylabel('Membership')
legend(loc='best')
show()

# Angulo --------------------------------------
angle_large_pos = trapmf(angle, [50, 90, 100, 101])
angle_medium_pos = trimf(angle, [20, 50, 100])
angle_small_pos = trimf(angle, [-20, 20, 50])
angle_small_neg = trimf(angle, [-50, -20, 20])
angle_medium_neg = trimf(angle, [-100, -50, -20])
angle_large_neg = trapmf(angle, [-101, -100, -90, -50])

angle_array = array(
    [
        trapmf(angle, [50, 80, 100, 101]),
        trimf(angle, [25, 50, 100]),
        trimf(angle, [-25, 25, 50]),
        trimf(angle, [-50, -25, 25]),
        trimf(angle, [-100, -50, -25]),
        trapmf(angle, [-101, -100, -80, -50])
    ]
)

plot(angle, angle_large_pos, label='Angle Large Positive (ALP)')
plot(angle, angle_medium_pos, label='Angle Medium Positive (AMP)')
plot(angle, angle_small_pos, label='Angle Small Positive (ASP)')
plot(angle, angle_small_neg, label='Angle Small Negative (ASN)')
plot(angle, angle_medium_neg, label='Angle Medium Negative (AMN)')
plot(angle, angle_large_neg, label='Angle Large Negative (ALN)')
xlabel('Angle')
ylabel('Membership')
legend(loc='best')
show()

# Velociade angular --------------------------------------
ang_vel_large_pos = trapmf(angular_velocity, [50, 90, 100, 101])
ang_vel_medium_pos = trimf(angular_velocity, [20, 50, 90])
ang_vel_small_pos = trimf(angular_velocity, [-20, 20, 50])
ang_vel_small_neg = trimf(angular_velocity, [-50, -20, 20])
ang_vel_medium_neg = trimf(angular_velocity, [-90, -50, -20])
ang_vel_large_neg = trapmf(angular_velocity, [-101, -100, -90, -50])

ang_vel_array = array(
    [
        trapmf(angular_velocity, [50, 90, 100, 101]),
        trimf(angular_velocity, [20, 50, 90]),
        trimf(angular_velocity, [-20, 20, 50]),
        trimf(angular_velocity, [-50, -20, 20]),
        trimf(angular_velocity, [-90, -50, -20]),
        trapmf(angular_velocity, [-101, -100, -90, -50])
    ]
)

plot(angular_velocity, ang_vel_large_pos, label='Vel Large Positive (VLP)')
plot(angular_velocity, ang_vel_medium_pos, label='Vel Medium Positive (VMP)')
plot(angular_velocity, ang_vel_small_pos, label='Vel Small Positive (VSP)')
plot(angular_velocity, ang_vel_small_neg, label='Vel Small Negative (VSN)')
plot(angular_velocity, ang_vel_medium_neg, label='Vel Medium Negative (VMN)')
plot(angular_velocity, ang_vel_large_neg, label='Vel Large Negative (VLN)')
xlabel('Velocity')
ylabel('Membership')
legend(loc='best')
show()

# Forca de saida --------------------------------------
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

fam_table = ([[0, 0, 0, 1],  # PL and ALP and VLP
              [0, 0, 1, 1],  # PL and ALP and VMP
              [0, 0, 2, 1],  # PL and ALP and VSP
              [0, 0, 3, 1],  # PL and ALP and VSN
              [0, 0, 4, 1],  # PL and ALP and VMN
              [0, 0, 5, 1],  # PL and ALP and VLN

              [0, 1, 0, 1],  # PL and AMP and VLP
              [0, 1, 1, 1],  # PL and AMP and VMP
              [0, 1, 2, 1],  # PL and AMP and VSP
              [0, 1, 3, 1],  # PL and AMP and VSN
              [0, 1, 4, 1],  # PL and AMP and VMN
              [0, 1, 5, 0],  # PL and AMP and VLN

              [0, 2, 0, 1],  # PL and ASP and VLP
              [0, 2, 1, 1],  # PL and ASP and VMP
              [0, 2, 2, 1],  # PL and ASP and VSP
              [0, 2, 3, 1],  # PL and ASP and VSN
              [0, 2, 4, 0],  # PL and ASP and VMN
              [0, 2, 5, 0],  # PL and ASP and VLN

              [0, 3, 0, 1],  # PL and ASN and VLP
              [0, 3, 1, 1],  # PL and ASN and VMP
              [0, 3, 2, 0],  # PL and ASN and VSP
              [0, 3, 3, 0],  # PL and ASN and VSN
              [0, 3, 4, 0],  # PL and ASN and VMN
              [0, 3, 5, 0],  # PL and ASN and VLN

              [0, 4, 0, 1],  # PL and AMN and VLP
              [0, 4, 1, 0],  # PL and AMN and VMP
              [0, 4, 2, 0],  # PL and AMN and VSP
              [0, 4, 3, 0],  # PL and AMN and VSN
              [0, 4, 4, 0],  # PL and AMN and VMN
              [0, 4, 5, 0],  # PL and AMN and VLN

              [0, 5, 0, 1],  # PL and ALN and VLP
              [0, 5, 1, 0],  # PL and ALN and VMP
              [0, 5, 2, 0],  # PL and ALN and VSP
              [0, 5, 3, 0],  # PL and ALN and VSN
              [0, 5, 4, 0],  # PL and ALN and VMN
              [0, 5, 5, 0],  # PL and ALN and VLN

              [1, 0, 0, 1],  # PR and ALP and VLP
              [1, 0, 1, 1],  # PR and ALP and VMP
              [1, 0, 2, 1],  # PR and ALP and VSP
              [1, 0, 3, 1],  # PR and ALP and VSN
              [1, 0, 4, 1],  # PR and ALP and VMN
              [1, 0, 5, 0],  # PR and ALP and VLN

              [1, 1, 0, 1],  # PR and AMP and VLP
              [1, 1, 1, 1],  # PR and AMP and VMP
              [1, 1, 2, 1],  # PR and AMP and VSP
              [1, 1, 3, 1],  # PR and AMP and VSN
              [1, 1, 4, 1],  # PR and AMP and VMN
              [1, 1, 5, 0],  # PR and AMP and VLN

              [1, 2, 0, 1],  # PR and ASP and VLP
              [1, 2, 1, 1],  # PR and ASP and VMP
              [1, 2, 2, 1],  # PR and ASP and VSP
              [1, 2, 3, 1],  # PR and ASP and VSN
              [1, 2, 4, 0],  # PR and ASP and VMN
              [1, 2, 5, 0],  # PR and ASP and VLN

              [1, 3, 0, 1],  # PR and ASN and VLP
              [1, 3, 1, 1],  # PR and ASN and VMP
              [1, 3, 2, 0],  # PR and ASN and VSP
              [1, 3, 3, 0],  # PR and ASN and VSN
              [1, 3, 4, 0],  # PR and ASN and VMN
              [1, 3, 5, 0],  # PR and ASN and VLN

              [1, 4, 0, 1],  # PR and AMN and VLP
              [1, 4, 1, 0],  # PR and AMN and VMP
              [1, 4, 2, 0],  # PR and AMN and VSP
              [1, 4, 3, 0],  # PR and AMN and VSN
              [1, 4, 4, 0],  # PR and AMN and VMN
              [1, 4, 5, 0],  # PR and AMN and VLN

              [1, 5, 0, 0],  # PR and ALN and VLP
              [1, 5, 1, 0],  # PR and ALN and VMP
              [1, 5, 2, 0],  # PR and ALN and VSP
              [1, 5, 3, 0],  # PR and ALN and VSN
              [1, 5, 4, 0],  # PR and ALN and VMN
              [1, 5, 5, 0]   # PR and ALN and VLN
              ])

max_episodes = 100
max_steps = 1000
total = 0

for episode in range(1, max_episodes + 1):
    positions = []
    angles = []
    angular_velocities = []
    done, state = init_state()
    ### Descomentar todas as linhas de codigo abaixo para ver o desenovlvimento
    ### passo a passo, incluindo o codigo comentado dentro do loop
    # print("    Normal:")
    # print(f"posicao: {state[0]} | angulo: {state[2]} | vel angular: {state[3]}")
    curr_position, curr_angle, curr_angular_vel = normalize_state(100, state)
    # print("    Com mudanca de escala:")
    # print(f"posicao: {curr_position} | angulo: {curr_angle} | vel angular: {curr_angular_vel}")
    for steps in range(1, max_steps + 1):
        # Para o caso de querer plotar a evolucao dos estados
        positions.append(curr_position)
        angles.append(curr_angle)
        angular_velocities.append(curr_angular_vel)

        control = control_signal(3,
                                 array([curr_position, curr_angle, curr_angular_vel]),
                                 array([position, angle, angular_velocity]),
                                 force,
                                 array([position_array, angle_array, ang_vel_array]),
                                 # membership
                                 force_matrix,
                                 fam_table
                                 )

        # Escolha da acao baseado no sinal de controle
        if control > 0:
            action = 1
        else:
            action = 0

        ### Descomentar abaixo para visualizar passo a passo
        # print(f"controle: {control}")
        # print(f"acao: {action}\n")
        done, state = act(action)
        # print("    Normal:")
        # print(f"posicao: {state[0]} | angulo: {state[2]} | vel angular: {state[3]}")
        curr_position, curr_angle, curr_angular_vel = normalize_state(100, state)
        # print("    Com mudanca de escala:")
        # print(f"posicao: {curr_position} | angulo: {curr_angle} | vel angular: {curr_angular_vel}")
        # input()
        if done:
            total += steps
            print(f"{steps} no episodio {episode} | media: {total / episode}")
            break
