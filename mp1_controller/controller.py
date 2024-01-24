"""
This file is the main controller file

Here, you will design the controller for your for the adaptive cruise control system.
"""

from mp1_simulator.simulator import Observation
import logging


# NOTE: Very important that the class name remains the same
class Controller:
    def __init__(self, target_speed: float, distance_threshold: float):
        self.target_speed = target_speed
        self.distance_threshold = distance_threshold
        self.i_e = 0.0

    def run_step(self, obs: Observation, estimate_dist) -> float:
        """This is the main run step of the controller.

        Here, you will have to read in the observatios `obs`, process it, and output an
        acceleration value. The acceleration value must be some value between -10.0 and 10.0.

        Note that the acceleration value is really some control input that is used
        internally to compute the throttle to the car.

        Below is some example code where the car just outputs the control value 10.0
        """

        ego_velocity = obs.velocity
        target_velocity = obs.target_velocity
        dist_to_lead = obs.distance_to_lead

        k_p = -1.0
        k_i = 1.0

        error = target_velocity - ego_velocity
        self.i_e += error
        self.i_e = self.i_e * 0.03

        acc = (k_p * error) + (k_i * self.i_e)

        if dist_to_lead < self.distance_threshold:
            acc = min(0.0, acc)
        else:
            # Maintain or increase speed if safe
            acc = min(10.0, acc)

        acc = max(-10.0, acc)

        # Do your magic...

        return acc
