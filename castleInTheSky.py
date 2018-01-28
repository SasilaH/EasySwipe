import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import pyautogui
from time import sleep
import pygame

#Variable Initializations
#turns = 0
turnDir = ""
swipeDir = ""
swipeFinger = ""
tapFinger = ""
screenTapFinger = ""
pinch = 0
grab = 0
fistTimer = 0
fingerCount = 0

class EasyListen(Leap.Listener):
    # finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    # bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    # state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        global swipeLeft
        global swipeRight
        global fistTimer
        global turnDir
        global swipeDir
        global swipeFinger
        global tapFinger
        global screenTapFinger
        global pinch
        global grab
        global fingerCount
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        turns=0

        #Configurating Gesture Settings
        controller.config.set("Gesture.Swipe.MinLength", 220)
        controller.config.set("Gesture.Swipe.MinVelocity", 100)
        controller.config.save()

        controller.config.set("Gesture.KeyTap.MinDownVelocity", 40.0)
        controller.config.set("Gesture.KeyTap.HistorySeconds", .3)
        controller.config.set("Gesture.KeyTap.MinDistance", 1.0)
        controller.config.save()

        controller.config.set("Gesture.ScreenTap.MinForwardVelocity", 20.0)
        controller.config.set("Gesture.ScreenTap.HistorySeconds", .5)
        controller.config.set("Gesture.ScreenTap.MinDistance", 1.0)
        controller.config.save()

        for gesture in frame.gestures():

            #Circle Gesture
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2):
                    turnDir = "CW"
                    turns += circle.progress
                    if(turns > 2.5):
                        pyautogui.hotkey('volumeup')
                        #sleep(.1)
                else:
                    turnDir = "CCW"
                    turns -= circle.progress
                    if(turns < -2.5):
                        pyautogui.hotkey('volumedown')
                        #sleep(.1)

                print(turnDir + " " + str(turns)) ######SWAP WITH FUCNTION

            #Swipe Gesture
            if gesture.type is Leap.Gesture.TYPE_SWIPE:
                swipe = Leap.SwipeGesture(gesture)

                swipeDir = swipe.direction
                swipeFinger = swipe.pointable

                if(swipeDir[0]<0):

                    pyautogui.moveTo(980,540,0)
                    pyautogui.click()
                    pyautogui.hotkey('left')
                    pyautogui.hotkey('alt', 'tab')
                    sleep(1.2)
                elif (swipeDir[0]>0):

                    pyautogui.moveTo(980,540,0)
                    pyautogui.click()
                    pyautogui.hotkey('right')
                    pyautogui.hotkey('alt', 'tab')
                    sleep(1.2)

                print("Swipe "+str(swipeFinger) + " " + str(swipeDir[0])) ######SWAP WITH FUCNTION

            #Key-Tap Gesture
            if gesture.type is Leap.Gesture.TYPE_KEY_TAP:
                tap = Leap.KeyTapGesture(gesture)
                tapFinger = tap.pointable
                tapDir = tap.direction

                print("Tap " + str(tapDir)) ######SWAP WITH FUCNTION


            #Screen-Tap Gesture
            if gesture.type is Leap.Gesture.TYPE_SCREEN_TAP:
                screenTap = Leap.ScreenTapGesture(gesture)
                screenTapFinger = screenTap.pointable

                print("ScreenTap " + str(screenTapFinger)) ######SWAP WITH FUCNTION

        for hand in frame.hands:

            #Identifies the hand
            handType = "Left" if hand.is_left else "Right"

            grab = hand.grab_strength
            pinch = hand.pinch_strength
            #print(handType + " p:" + str(pinch) + " g:"+ str(grab)) ######SWAP WITH FUCNTION
            if grab ==1:
                if(fistTimer > 2):
                    pyautogui.hotkey('volumemute')
                    print("g"+str(grab))
                    sleep(1.2)
                    fistTimer = 0
                else:
                    fistTimer +=1
            '''elif pinch > 0.99:
                pyautogui.hotkey('printscreen')
                print("p"+str(pinch))
                sleep(1.5)'''

def main():
    # Create a sample listener and controller
    listener = EasyListen()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
