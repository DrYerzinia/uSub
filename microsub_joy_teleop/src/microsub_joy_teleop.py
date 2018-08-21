#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import Joy
from uuv_gazebo_ros_plugins_msgs.msg import FloatStamped

ROLL_AXES  = 0
PITCH_AXES = 1
TWIST_AXES = 2
THROT_AXES = 3

roll_val  = 0.0
pitch_val = 0.0
twist_val = 0.0
throt_val = 0.0

TWIST_EFFORT    = 0.5
TRANLATE_EFFORT = 1.0

THRUSTER_POWER = 300.0

def joystick_state(data):

    global roll_val
    global pitch_val
    global twist_val
    global throt_val

    roll_val  = data.axes[ROLL_AXES]
    pitch_val = data.axes[PITCH_AXES]
    twist_val = data.axes[TWIST_AXES]
    throt_val = data.axes[THROT_AXES]

def microsub_joy_teleop():

    global roll_val
    global pitch_val
    global twist_val
    global throt_val

    pub_t0_dir = rospy.Publisher('/microsub/thruster0_position_controller/command', Float64, queue_size=10)
    pub_t1_dir = rospy.Publisher('/microsub/thruster1_position_controller/command', Float64, queue_size=10)
    pub_t2_dir = rospy.Publisher('/microsub/thruster2_position_controller/command', Float64, queue_size=10)
    pub_t3_dir = rospy.Publisher('/microsub/thruster3_position_controller/command', Float64, queue_size=10)

    pub_t0_eff = rospy.Publisher('/microsub/thrusters/0/input', FloatStamped, queue_size=10)
    pub_t1_eff = rospy.Publisher('/microsub/thrusters/1/input', FloatStamped, queue_size=10)
    pub_t2_eff = rospy.Publisher('/microsub/thrusters/2/input', FloatStamped, queue_size=10)
    pub_t3_eff = rospy.Publisher('/microsub/thrusters/3/input', FloatStamped, queue_size=10)

    rospy.init_node('microsub_joy_teleop', anonymous=True)
    rospy.Subscriber("/joy", Joy, joystick_state)
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():

        front_val = roll_val*TRANLATE_EFFORT   + twist_val*TWIST_EFFORT
        back_val  = roll_val*TRANLATE_EFFORT   - twist_val*TWIST_EFFORT
        left_val  = -pitch_val*TRANLATE_EFFORT + twist_val*TWIST_EFFORT
        right_val = -pitch_val*TRANLATE_EFFORT - twist_val*TWIST_EFFORT

        t0_setpoint = Float64()
        t0_setpoint.data = front_val
        pub_t0_dir.publish(t0_setpoint)

        t1_setpoint = Float64()
        t1_setpoint.data = back_val
        pub_t1_dir.publish(t1_setpoint)

        t2_setpoint = Float64()
        t2_setpoint.data = left_val
        pub_t2_dir.publish(t2_setpoint)

        t3_setpoint = Float64()
        t3_setpoint.data = right_val
        pub_t3_dir.publish(t3_setpoint)

        thrust0 = FloatStamped()
        thrust0.header.stamp = rospy.Time.now()
        thrust0.data = throt_val*THRUSTER_POWER
        pub_t0_eff.publish(thrust0)

        thrust1 = FloatStamped()
        thrust1.header.stamp = rospy.Time.now()
        thrust1.data = throt_val*THRUSTER_POWER
        pub_t1_eff.publish(thrust1)

        thrust2 = FloatStamped()
        thrust2.header.stamp = rospy.Time.now()
        thrust2.data = throt_val*THRUSTER_POWER
        pub_t2_eff.publish(thrust2)

        thrust3 = FloatStamped()
        thrust3.header.stamp = rospy.Time.now()
        thrust3.data = throt_val*THRUSTER_POWER
        pub_t3_eff.publish(thrust3)

        rate.sleep()

if __name__ == '__main__':
    try:
        microsub_joy_teleop()
    except rospy.ROSInterruptException:
        rospy.loginfo("Mother fucker!")
