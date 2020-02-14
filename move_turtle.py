#!/usr/bin/env python


#Importando as bibliotecas necessarias e declarando algumas variaveis
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
PI = 3.1415926535897
x = 0
y = 0
z = 0
yaw = 0


#Função para a posição do turtlesim
def poseCallback(pose_message):
    global x
    global y,z, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta


#Função para movimentar o turtlesim
def move(speed, distance, is_foward):
        velocity_message = Twist()
        global x, y
        x0 = x
        y0 = y

        #Checando a direção do movimento
        if (is_foward):
            velocity_message.linear.x = abs(speed)
        else:
            velocity_message.linear.x =-abs(speed)

        distance_moved = 0.0
        loop_rate = rospy.Rate(10)
        cmd_vel_topic ='/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 10)

        #Loop para o movimento em linha reta
        while True:
                rospy.loginfo("Turtlesim moves fowards")
                velocity_publisher.publish(velocity_message)

                loop_rate.sleep()

                distance_moved = distance_moved + abs(0.5 * math.sqrt(((x-x0) ** 2) + ((y - y0) ** 2)))
                print(distance_moved)

                #Quebrando o loop para parar o turtlesim
                if not (distance_moved < distance):
                    rospy.loginfo("reached")
                    break

        velocity_message.linear.x = 0
        velocity_publisher.publish(velocity_message)


#Função para rotacionar
def rotate(speed, angle, clockwise):

    #Convertendo de angulos para radianos
    angular_speed = speed*2*PI/360
    relative_angle = angle*2*PI/360

    vel_msg = Twist()
    vel_msg.linear.x=0
    vel_msg.linear.y=0
    vel_msg.linear.z=0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    # Checando o sentido da rotação
    if clockwise:
        vel_msg.angular.z = -abs(angular_speed)
    else:
        vel_msg.angular.z = abs(angular_speed)

    t0 = rospy.Time.now().to_sec()
    current_angle = 0
    loop_rate = rospy.Rate(10)

    #Loop para o movimento rotacional
    while(current_angle < relative_angle):
        rospy.loginfo("Turtlesim rotates")
        velocity_publisher.publish(vel_msg)
        loop_rate.sleep()
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed*(t1-t0)

        #Parando o loop
        if (current_angle > relative_angle):
            rospy.loginfo("reached")
            break

    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)


#Função para intercalar os movimentos a serem realizados
def move_and_rotate():

    move(1.0, 6.0, True)
    rotate(30, 90, 0)
    move(1.0, 6.0, True)
    rotate(30, 90, 0)
    move(1.0, 6.0, True)
    rotate(30, 90, 0)
    move(1.0, 6.0, True)
    pass


if __name__ == '__main__':
    try:

        rospy.init_node('turtlesim_motion_pose', anonymous = True)

        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 10)
        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)
        time.sleep(2)
        move_and_rotate()

    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")

