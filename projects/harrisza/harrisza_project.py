#!/usr/bin/env python3
"""
Author: Zachery Harrison.
"""
import ev3dev.ev3 as ev3
import time

import robot_controller as robo


def main():
    print("--------------------------------------------")
    print("IR Remote")
    print(" - Use IR remote channel 1 to drive around")
    print(" - Use IR remote channel 2 to for the arm")
    print(" - Press the Back button on EV3 to exit")
    print("--------------------------------------------")
    ev3.Sound.speak("I R Remote")

    ev3.Leds.all_off()  # Turn the leds off
    robot = robo.Snatch3r()
    dc = DataContainer()

    # DONE: 4. Add the necessary IR handler callbacks as per the instructions above.
    # Remote control channel 1 is for driving the crawler tracks around (none of these functions exist yet below).
    # Remote control channel 2 is for moving the arm up and down (all of these functions already exist below).

    rc1 = ev3.RemoteControl(channel=1)
    rc2 = ev3.RemoteControl(channel=2)
    rc3 = ev3.RemoteControl(channel=3)
    rc4 = ev3.RemoteControl(channel=4)

    # For our standard shutdown button.
    btn = ev3.Button()
    btn.on_backspace = lambda state: handle_shutdown(state, dc)

    robot.arm_calibration()  # Start with an arm calibration in this program.

    rc1.on_red_up = lambda button_state: handle_move_left_forward(button_state, robot)
    rc1.on_red_down = lambda button_state: handle_move_left_back(button_state, robot)
    rc1.on_blue_up = lambda button_state: handle_move_right_forward(button_state, robot)
    rc1.on_blue_down = lambda button_state: handle_move_right_back(button_state, robot)
    rc2.on_red_up = lambda button_state: handle_arm_up_button(button_state, robot)
    rc2.on_red_down = lambda button_state: handle_arm_down_button(button_state, robot)
    rc2.on_blue_up = lambda button_state: handle_calibrate_button(button_state, robot)
    rc2.on_blue_down = lambda button_state: handle_shutdown(button_state, robot)

    while dc.running:
        # DONE: 5. Process the RemoteControl objects.
        btn.process()
        rc1.process()
        rc2.process()
        time.sleep(0.01)


def handle_move_left_forward(button_state, robot):
    robot.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    if button_state:
        robot.left_motor.run_forever(speed_sp=300)
    else:
        robot.left_motor.stop()


def handle_move_left_back(button_state, robot):
    robot.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    if button_state:
        robot.left_motor.run_forever(speed_sp=-300)
    else:
        robot.left_motor.stop()


def handle_move_right_forward(button_state, robot):
    robot.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
    if button_state:
        robot.right_motor.run_forever(speed_sp=300)
    else:
        robot.right_motor.stop()


def handle_move_right_back(button_state, robot):
    robot.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
    if button_state:
        robot.right_motor.run_forever(speed_sp=-300)
    else:
        robot.right_motor.stop()


def handle_arm_up_button(button_state, robot):
    """
    Moves the arm up when the button is pressed.

    Type hints:
      :type button_state: bool
      :type robot: robo.Snatch3r
    """
    if button_state:
        robot.arm_up()


def handle_arm_down_button(button_state, robot):
    """
    Moves the arm down when the button is pressed.

    Type hints:
      :type button_state: bool
      :type robot: robo.Snatch3r
    """
    if button_state:
        robot.arm_down()


def handle_calibrate_button(button_state, robot):
    """
    Has the arm go up then down to fix the starting position.

    Type hints:
      :type button_state: bool
      :type robot: robo.Snatch3r
    """
    if button_state:
        robot.arm_calibration()


def handle_shutdown(button_state, dc):
    """
    Exit the program.

    Type hints:
      :type button_state: bool
      :type dc: DataContainer
    """
    if button_state:
        dc.running = False


main()