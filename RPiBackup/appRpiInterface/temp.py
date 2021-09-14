import gpio
import three_d

theta, rho = three_d.get_angles()
print((theta, rho))
gpio.shoot(-theta, rho)