#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class JetAutoMecanumSquare(Node):
    def __init__(self):
        super().__init__('jetauto_mecanum_square')
        # Tópico padrão confirmado no JetAuto [cite: 7, 16]
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def mover(self, vx, vy, tempo):
        msg = Twist()
        inicio = time.time()
        while time.time() - inicio < tempo:
            msg.linear.x = vx
            msg.linear.y = vy # Translação lateral
            msg.angular.z = 0.0
            self.pub.publish(msg)
            time.sleep(0.05)
        self.parar()

    def parar(self):
        msg = Twist()
        for _ in range(5): # Parada robusta conforme regra [cite: 11, 15]
            msg.linear.x = 0.0
            msg.linear.y = 0.0
            msg.angular.z = 0.0
            self.pub.publish(msg)
            time.sleep(0.05)

    def executar(self):
        vel = 0.1
        tempo = 1.0 # 10 cm a 0.1 m/s = 1 segundo

        self.get_logger().info('Iniciando Quadrado Lateral (Mecanum)...')
        time.sleep(1)

        # 1. Frente (Linear X)
        self.get_logger().info('1. Frente')
        self.mover(vel, 0.0, tempo)
        time.sleep(0.5)

        # 2. Direita (Linear Y Negativo)
        self.get_logger().info('2. Direita (Lateral)')
        self.mover(0.0, -vel, tempo)
        time.sleep(0.5)

        # 3. Trás (Linear X Negativo)
        self.get_logger().info('3. Trás')
        self.mover(-vel, 0.0, tempo)
        time.sleep(0.5)

        # 4. Esquerda (Linear Y Positivo)
        self.get_logger().info('4. Esquerda (Lateral)')
        self.mover(0.0, vel, tempo)

        self.parar()
        self.get_logger().info('Quadrado concluído!')

def main():
    rclpy.init()
    node = JetAutoMecanumSquare()
    node.executar()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
