#!/usr/bin/env python
from __future__ import print_function

import roslib
import actionlib
import sys
import rospy
import numpy as np
import cv2
import os
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from gazebo_msgs.msg import ModelStates, ModelState
from geometry_msgs.msg import Quaternion, Pose, Twist

roslib.load_manifest('team2_gazebo')

models = ModelStates()

# This example shows how to extract model info from gazebo topics
def model_callback(msg):
  models = msg
  for i, model in enumerate(msg.name):
    if model == 'plastic_cup':
      cup = i
      #print ('Pose of plastic_cup:')
      #print (msg.pose[i])


def random_objects(n):
  """Pick n random objects, from the 3-10 available desk objects."""
  pass


def shuffle_objects(msg):
  """Shuffle objects on table."""
  table_height = msg.pose[msg.find('table')][3]  # Get height of table from message

  for i, model_name in enumerate(msg.name):
    mover = rospy.Publisher('/gazebo/set_model_state',ModelState, queue_size = 10)
    random_pose = ModelState()
    random_pose.model_name = model_name
    random_pose.pose.orientation = Quaternion(0,0,0,0)
    random_pose.pose.position.z = 0.9 # height of table
  pass


def publish_and_save_new_config():
  """Push changes to object configuration, and take picture."""


class ImageConverter:
  """Subscribe to image feed and publish to output_image/."""

  def __init__(self):
    self.image_pub = rospy.Publisher("/team2/output_image", Image, queue_size=10)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/head_camera/rgb/image_raw",Image,self.callback)


  # def save_img(self, subdir, prefix='scene', suffix='.png'):
  #   try:
  #     cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
  #     # Get number to append to image name
  #     n = len([name for name in os.listdir(subdir) if os.path.isfile(name)])
  #     cv2.imwrite(os.path.join(subdir, prefix + str(n) + suffix), cv_image)
  #   except CvBridgeError as e:
  #     print(e)


  def callback(self,data):
    prefix = 'scene'
    suffix = '.png'
    subdir = 'messy_imgs'
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      path = os.path.join(os.getcwd(), subdir)
      print("saving image to: ", path)
      if os.path.isdir(subdir):
        n = len([name for name in os.listdir(subdir) if os.path.isfile(name)])
      else:
        n = 0

      img_path = os.path.join(path, prefix + str(n) + suffix)
      cv2.imwrite(img_path, cv_image)
      print("saved image to: ", path)
      cv2.imshow('image', cv_image)
      cv2.waitKey(3)
    except CvBridgeError as e:
      print(e)



def main(args):

  rospy.init_node('model_spawner', anonymous=True)
  rospy.Subscriber('/gazebo/model_states', ModelStates, model_callback)

  # Setup camera for saving images
  ic = ImageConverter()

  # Here shows how to manipulate objects using ros publisher
  cup_mover = rospy.Publisher('/gazebo/set_model_state',ModelState, queue_size = 10)
  random_pose = ModelState()
  random_pose.model_name = 'plastic_cup'
  random_pose.pose.orientation = Quaternion(0,0,0,0)
  random_pose.pose.position.z = 0.9 # height of table

  r = rospy.Rate(1) # 1Hz
  while not rospy.is_shutdown():
    random_pose.pose.position.x = np.random.uniform(-0.25,0.25)
    random_pose.pose.position.y = np.random.uniform(-0.75,0.75)
    cup_mover.publish(random_pose)
    r.sleep()
  cv2.destroyAllWindows()


if __name__ == '__main__':
  main(sys.argv)
