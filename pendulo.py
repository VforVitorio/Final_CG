from vpython import *
import numpy as np

# Constants
g = 9.80            # (m/s^2)
L = 10              # Length of the pendulums (m)
initialAngle = 1.2  # In radians

# Create the pendulum bob and rod
pend = sphere(pos=vector(L * np.sin(initialAngle), -L *
              np.cos(initialAngle), 0), radius=1, color=color.yellow)
rod = cylinder(pos=vector(0, 0, 0), axis=pend.pos, radius=0.1)
pend2 = sphere(pos=vector(-2, -L, 0), radius=1, color=color.red)
rod2 = cylinder(pos=vector(-2, 0, 0), axis=vector(pend2.pos.x +
                2, pend2.pos.y, pend2.pos.z), radius=0.1)


def position(right, t):
    """
    Only one of the pendulums is in motion at a given time. This function
    moves the moving pendulum to its new position. We use the equation:
        theta(t) = theta_0*cos(sqrt(g/L)*t)
    """
    theta = initialAngle * np.cos((g / L) ** (1 / 2) * t)

    if right:
        # Update position of bob
        pend.pos = vector(L * np.sin(theta), -L * np.cos(theta), 0)
        rod.axis = pend.pos  # Update rod's position
    else:
        pend2.pos = vector(L * np.sin(theta) - 2, -L *
                           np.cos(theta), 0)  # Update position of bob
        rod2.axis = vector(pend2.pos.x + 2, pend2.pos.y,
                           pend2.pos.z)  # Update rod's position

    # Once the moving pendulum reaches theta = 0, switch to the other one
    return theta > 0


# Increment time
i = 0
right = True  # The right pendulum is the first in motion
while True:
    rate(200)
    right = position(right, i)
    i += 0.01
