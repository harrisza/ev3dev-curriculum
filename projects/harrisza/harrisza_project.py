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
    print(" - Use IR remote channel 3 to draw shapes")
    print(" - Use IR remote channel 4 to dance!")
    print(" - Press the Back button on EV3 to exit")
    print("--------------------------------------------")
    ev3.Sound.speak("I R Remote")

    ev3.Leds.all_off()  # Turn the leds off
    robot = robo.Snatch3r()

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
    rc3.on_red_up = lambda button_state: draw_triangle(button_state, robot)
    rc3.on_red_down = lambda button_state: draw_square(button_state, robot)
    rc3.on_blue_up = lambda button_state: draw_pentagon(button_state, robot)
    rc3.on_blue_down = lambda button_state: draw_hexagon(button_state, robot)
    rc4.on_red_up = lambda button_state: dance_1(button_state, robot)
    rc4.on_red_down = lambda button_state: dance_2(button_state, robot)
    rc4.on_blue_up = lambda button_state: dance_3(button_state, robot)
    rc4.on_blue_down = lambda button_state: dance_4(button_state, robot)

    dc = DataContainer()

    while dc.running:
        # DONE: 5. Process the RemoteControl objects.
        btn.process()
        rc1.process()
        rc2.process()
        rc3.process()
        rc4.process()
        time.sleep(0.01)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True


def handle_move_left_forward(button_state, robot):
    robot.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    if button_state:
        robot.left_motor.run_forever(speed_sp=900)
    else:
        robot.left_motor.stop()


def handle_move_left_back(button_state, robot):
    robot.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    if button_state:
        robot.left_motor.run_forever(speed_sp=-900)
    else:
        robot.left_motor.stop()


def handle_move_right_forward(button_state, robot):
    robot.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
    if button_state:
        robot.right_motor.run_forever(speed_sp=900)
    else:
        robot.right_motor.stop()


def handle_move_right_back(button_state, robot):
    robot.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
    if button_state:
        robot.right_motor.run_forever(speed_sp=-900)
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


def draw_triangle(button_state, robot):
    if button_state:
        ev3.Sound.speak("Drawing triangle").wait()
        turn_amount1 = 120 * 5
        for k in range(3):
            robot.drive_inches(25, 900)
            robot.turn_degrees(turn_amount1, 900)


def draw_square(button_state, robot):
    if button_state:
        ev3.Sound.speak("Drawing square").wait()
        turn_amount2 = 90 * 5
        for k in range(4):
            robot.drive_inches(25, 900)
            robot.turn_degrees(turn_amount2, 900)


def draw_pentagon(button_state, robot):
    if button_state:
        ev3.Sound.speak("Drawing pentagon").wait()
        turn_amount3 = 72 * 4.75
        for k in range(5):
            robot.drive_inches(25, 900)
            robot.turn_degrees(turn_amount3, 900)


def draw_hexagon(button_state, robot):
    if button_state:
        ev3.Sound.speak("Drawing hexagon").wait()
        turn_amount4 = 60 * 4.5
        for k in range(6):
            robot.drive_inches(25, 900)
            robot.turn_degrees(turn_amount4, 900)


def dance_1(button_state, robot):
    """Handle IR / button event."""
    if button_state:
        robot.left_motor.run_forever(speed_sp=400)
        robot.right_motor.run_forever(speed_sp=-400)
        while button_state:
            play_song_by_individual_tones()

            if not button_state:
                break
    else:
        robot.left_motor.stop()
        robot.right_motor.stop()


def dance_2(button_state, robot):
    """Handle IR / button event."""
    if button_state:
        robot.left_motor.run_forever(speed_sp=-400)
        robot.right_motor.run_forever(speed_sp=400)
        while button_state:
            play_song_by_notes_list()

            if not button_state:
                break
    else:
        robot.left_motor.stop()
        robot.right_motor.stop()


def dance_3(button_state, robot):
    """Handle IR / button event."""
    if button_state:
        robot.arm_up()
        robot.left_motor.run_forever(speed_sp=-400)
        robot.right_motor.run_forever(speed_sp=400)
        while button_state:
            ev3.Sound.speak('Everything is awesome!')
            time.sleep(1)
            if not button_state:
                break
    else:
        robot.left_motor.stop()
        robot.right_motor.stop()
        robot.arm_down()


def dance_4(button_state, robot):
    """Handle IR / button event."""
    if button_state:
        while button_state:
            play_wav_file()
            robot.arm_up()
            robot.arm_down()


def play_song_by_individual_tones():
    """
    Exam of using the ev3.Sound.tone method to play a single tone. For music the ev3.Sound.tone method
    often sounds better with the list approach below. Just showing it doesn't have to be a list.
    """
    tone_map = {"c4": 261.6, "c4s": 277.2, "d4": 293.7, "d4s": 311.1, "e4": 329.6, "f4": 349.2, "f4s": 370.0,
                "g4": 392.0, "g4s": 415.3, "a4": 440, "a4s": 466.2, "b4": 493.9, "c5": 523.3, "c5s": 554.4,
                "d5": 587.3,
                "d5s": 622.3, "e5": 659.3, "f5": 698.5, "f5s": 740.0, "g5": 784.0, "g5s": 830.6, "a5": 880,
                "a5s": 932.3, "b5": 987.8, "c6": 1046.5}

    tempo_ms = 20
    ev3.Sound.tone(tone_map["e5"], tempo_ms * 3).wait()  # Units are in milliseconds
    ev3.Sound.tone(tone_map["e5"], tempo_ms * 6).wait()
    ev3.Sound.tone(tone_map["e5"], tempo_ms * 3).wait()
    time.sleep(tempo_ms / 1000 * 3)  # Units are in seconds so divide by 1000
    ev3.Sound.tone(tone_map["c5"], tempo_ms * 3).wait()
    ev3.Sound.tone(tone_map["e5"], tempo_ms * 6).wait()
    ev3.Sound.tone(tone_map["g5"], tempo_ms * 12).wait()
    ev3.Sound.tone(tone_map["g4"], tempo_ms * 12).wait()
    # Didn't add the rest of the song to make testing faster.


def play_song_by_notes_list():
    """
    Pass in a list of notes to the ev3.Sound.tone method
    From: http://python-ev3dev.readthedocs.io/en/latest/other.html#sound

    List of tuples, where each tuple contains up to three numbers.
    The first number is frequency in Hz, the second is duration in milliseconds, and the
    third is delay in milliseconds between this and the next tone in the sequence.
    """
    ev3.Sound.tone([
        (392, 350, 100), (392, 350, 100), (392, 350, 100), (311.1, 250, 100),
        (466.2, 25, 100), (392, 350, 100), (311.1, 250, 100), (466.2, 25, 100),
        (392, 700, 100), (587.32, 350, 100), (587.32, 350, 100), (587.32, 350, 100),
        (622.26, 250, 100), (466.2, 25, 100), (369.99, 350, 100), (311.1, 250, 100),
        (466.2, 25, 100), (392, 700, 100),
        (784, 350, 100), (392, 250, 100), (392, 25, 100), (784, 350, 100),
        (739.98, 250, 100), (698.46, 25, 100), (659.26, 25, 100),
        (622.26, 25, 100), (659.26, 50, 400), (415.3, 25, 200), (554.36, 350, 100),
        (523.25, 250, 100), (493.88, 25, 100), (466.16, 25, 100), (440, 25, 100),
        (466.16, 50, 400), (311.13, 25, 200), (369.99, 350, 100),
        (311.13, 250, 100), (392, 25, 100), (466.16, 350, 100), (392, 250, 100),
        (466.16, 25, 100), (587.32, 700, 100), (784, 350, 100), (392, 250, 100),
        (392, 25, 100), (784, 350, 100), (739.98, 250, 100), (698.46, 25, 100),
        (659.26, 25, 100), (622.26, 25, 100), (659.26, 50, 400), (415.3, 25, 200),
        (554.36, 350, 100), (523.25, 250, 100), (493.88, 25, 100),
        (466.16, 25, 100), (440, 25, 100), (466.16, 50, 400), (311.13, 25, 200),
        (392, 350, 100), (311.13, 250, 100), (466.16, 25, 100),
        (392.00, 300, 150), (311.13, 250, 100), (466.16, 25, 100), (392, 700)
    ]).wait()


def play_wav_file():
    # File from http://www.moviesoundclips.net/ev3.Sound.php?id=288
    # Had to convert it to a PCM signed 16-bit little-endian .wav file
    # http://audio.online-convert.com/convert-to-wav
    ev3.Sound.play("/home/robot/csse120/assets/sounds/awesome_pcm.wav")


main()
