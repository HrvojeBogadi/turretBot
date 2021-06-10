/*
 * stm32f1xx_misc.h
 *
 *  Created on: Jun 5, 2021
 *      Author: Hrvoje Bogadi
 */

#ifndef INC_STM32F1XX_MISC_H_
#define INC_STM32F1XX_MISC_H_

void setLeftMotorPWM(int pwmPercentage); /* Parameter must be a percentage value [(X)Y(Z)] */
void setRightMotorPWM(int pwmPercentage); /* Parameter must be a percentage value [(X)Y(Z)] */
int getLeftMotorPWM();
int getRightMotorPWM();
void setLeftMotorDirection(int direction); // 0 - forward; 1 - backward
void setRightMotorDirection(int direction); // 0 - forward; 1 - backward



#endif /* INC_STM32F1XX_MISC_H_ */
