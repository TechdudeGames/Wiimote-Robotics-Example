import time
import RPi.GPIO as GPIO
def motor_movement(ticks,perc,divider,kilohertz,pin1,pin2):
    peroid = 1/(kilohertz*1000)
    duty_part = abs(perc/divider)*peroid
    if peroid-duty_part < 0:
        print("Perc/Percent Duty cycle too large. Defaulting to 90% Duty Cycle.")
        duty_part = abs(90/divider)*peroid
    try:
        GPIO.setup(pin1,GPIO.OUT)
        GPIO.setup(pin2, GPIO.OUT)
    except:
        print("LOG:Pins must have already been setup")
    if ticks > 0:
        GPIO.output(pin1,True)
        for count in range(0,ticks):
            time.sleep(peroid-duty_part)
            GPIO.output(pin2,True)
            time.sleep(duty_part)
            GPIO.output(pin2,False)
    if ticks < 0:
        GPIO.output(pin1,False)
        for count in range(0,abs(ticks)):
            time.sleep(peroid-duty_part)
            GPIO.output(pin2,True)
            time.sleep(duty_part)
            GPIO.output(pin2,False)
    GPIO.output(pin2, False)
    GPIO.output(pin1, False)
