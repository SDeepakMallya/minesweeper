#!/usr/bin/env python

from graph_helper import extract_graph
from graph_layout import *
from mrpp_ideal.msg import VisitNode

import pygame
import rospy
import sys
import rospkg
import ConfigParser as CP
import numpy as np
import math
import time
from std_msgs.msg import Int32

colour = {'WHITE' : (255, 255, 255), 'BLACK' : (0, 0, 0)}

class Robot(pygame.sprite.Sprite):

	def __init__(self, g, init_node, robot_id, disp_params):
		
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface((6, 6))
		self.image.fill(colour['WHITE'])
		self.rect = self.image.get_rect()

		self.time_cur = 0.
		self.time_last = 0.

		self.g = g
		self.target_node = init_node
		[x_pos, y_pos] = self.g.get_location(init_node)

		self.x_pos = x_pos
		self.y_pos = y_pos
		
		self.x_tar = x_pos
		self.y_tar = y_pos

		self.dx = 0.
		self.dy = 0.

		self.disp_params = disp_params

		self.disp_x = 0
		self.disp_y = 0
		
		# 4 pixels off from center of the lane
		self.off = 4

		self.x_scale = 1
		self.y_scale = 1
		if (self.disp_params[2] - self.disp_params[0]) > 0:
			self.x_scale = float(self.disp_params[5] - 2 * self.disp_params[6])/(self.disp_params[2] - self.disp_params[0])
		if (self.disp_params[3] - self.disp_params[1]) > 0:
			self.y_scale = float(self.disp_params[4] - 2 * self.disp_params[6])/(self.disp_params[3] - self.disp_params[1])
		
		self.id = robot_id

		self.sub = rospy.Subscriber('robot_{}/target_node'.format(self.id), Int32, self.callback_odom)
		self.pub = rospy.Publisher('robot_{}/target_reached'.format(self.id), VisitNode, queue_size = 10)

		self.pub_msg = VisitNode()
		self.pub_msg.stamp = 0.0
		self.pub_msg.node_id = init_node
		self.pub_msg.robot_id = self.id

	def callback_odom(self, data):

		self.target_node = data.data

		[self.x_tar, self.y_tar] = self.g.get_location(self.target_node)

		if math.sqrt((self.x_pos - self.x_tar) ** 2 + (self.y_pos - self.y_tar) ** 2) > 0.001:
			(dx, dy) = (self.x_tar - self.x_pos, self.y_tar - self.y_pos)
			nf = math.sqrt(dx ** 2 + dy ** 2)
			(self.dx, self.dy) = (dx/nf, dy/nf)

	def update(self, t):

		self.old_disp_x = self.disp_x
		self.old_disp_y = self.disp_y

		self.time_last = self.time_cur
		self.time_cur = t
		
		x_new = self.x_pos
		y_new = self.y_pos

		if math.sqrt((self.x_pos - self.x_tar) ** 2 + (self.y_pos - self.y_tar) ** 2) <= 0.001:
			self.pub.publish(self.pub_msg)

		else:
			dt = float(self.time_cur - self.time_last) * 1e-03
			x_new += self.dx * dt
			y_new += self.dy * dt

			if cmp(self.x_tar, x_new) != cmp(self.dx, 0.) or cmp(self.y_tar, y_new) != cmp(self.dy, 0.):
				x_new = self.x_tar
				y_new = self.y_tar
				self.pub_msg.stamp = self.time_cur
				self.pub_msg.node_id = self.target_node

		self.disp_x = int((x_new - self.disp_params[0]) * self.x_scale) + self.disp_params[6]
		self.disp_y = int((y_new - self.disp_params[1]) * self.y_scale) + self.disp_params[6]
	
		## To make it appear as if following difrectional lanes
		# (d1, d2) = (-self.dy, self.dx)
		# self.disp_x = int(self.disp_x + 4 * d1)
		# self.disp_y = int(self.disp_y + 4 * d2)

		self.x_pos = x_new
		self.y_pos = y_new

		self.rect.center = (self.disp_x, self.disp_y)

	# def get_old_disp(self):

	# 	return (self.old_disp_x, self.old_disp_y)

	# def get_new_disp(self):

	# 	return (self.disp_x, self.disp_y)

def main(argv):

	rospy.init_node('plot_sim', anonymous = True)

	graph = str(argv[0])
	num_robots = int(argv[1])
	init_cond = str(argv[2])
	realtime_factor = float(argv[3])


	# plot = Plot_Sim(graph, num_robots, init_cond)

	dirname = rospkg.RosPack().get_path('mrpp_ideal')
	img_file = dirname + '/graph_png/' + graph + '.png'
	desc_file = dirname + '/graph_file/' + graph + '.in'

	config = CP.ConfigParser()
	config.read(dirname + '/config_file.txt')

	params = {}

	for option in config.options(graph):
		params[option] = config.get(graph, option)

	disp_params = []
	temp = eval(params['display_params'])
	g = extract_graph(desc_file, params['graph_type'] == 'Undirected')
	# print params['graph_type']
	# print type(temp)
	disp_params.append(float(temp[0]))
	disp_params.append(float(temp[1]))
	disp_params.append(float(temp[2]))
	disp_params.append(float(temp[3]))
	disp_params.append(int(temp[4]))
	disp_params.append(int(temp[5]))
	disp_params.append(int(temp[6]))

	pygame.init()
	clock = pygame.time.Clock()

	screen = pygame.display.set_mode((int(disp_params[5]), int(disp_params[4])))
	pygame.display.set_caption('Simaltion Window')
	layout = pygame.image.load(img_file).convert()

	robots_active = pygame.sprite.Group()
	for i in range(num_robots):
		robot = Robot(g, i, i, disp_params)
		robots_active.add(robot)

	done = False

	t0 = clock.get_time()
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

		dt = clock.get_time()
		t0 += dt * realtime_factor
		robots_active.update(t0)
		screen.blit(layout, (0, 0))
		robots_active.draw(screen)
		pygame.display.flip()
		clock.tick(30)


	pygame.quit()


if __name__ == '__main__':
	try:
		if len(sys.argv[1:]) == 4:
			main(sys.argv[1:])
		else:
			print 'Please pass the appropriate arguments'

	except rospy.ROSInterruptException:
		pass