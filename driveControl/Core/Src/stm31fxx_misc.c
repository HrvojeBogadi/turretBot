/*
 * stm31fxx_misc.c
 *
 *  Created on: Jun 5, 2021
 *      Author: Hrvoje Bogadi
 */

#include "stm32f1xx_misc.h"
#include "main.h"

volatile int leftPWM;
volatile int rightPWM;


void setLeftMotorPWM(int pwmPercentage){
	TIM1->CCR2 = pwmPercentage * 10;
}

void setRightMotorPWM(int pwmPercentage){
	TIM1->CCR1 = pwmPercentage * 10;
}

int getLeftMotorPWM(){
	leftPWM = TIM1->CCR2 / 10;
	return (leftPWM);
}

int getRightMotorPWM(){
	rightPWM = TIM1->CCR1 / 10;
	return (rightPWM);
}

// 0 - forward; 1 - backward
void setLeftMotorDirection(int direction){
	if(direction == 0){
		HAL_GPIO_WritePin(MotorDriverIN1_GPIO_Port, MotorDriverIN1_Pin, GPIO_PIN_RESET);
		HAL_GPIO_WritePin(MotorDriverIN2_GPIO_Port, MotorDriverIN2_Pin, GPIO_PIN_SET);
	}else if(direction == 1){
		HAL_GPIO_WritePin(MotorDriverIN1_GPIO_Port, MotorDriverIN1_Pin, GPIO_PIN_SET);
		HAL_GPIO_WritePin(MotorDriverIN2_GPIO_Port, MotorDriverIN2_Pin, GPIO_PIN_RESET);
	}else{
		Error_Handler();
	}
}

void setRightMotorDirection(int direction){
	if(direction == 0){
		HAL_GPIO_WritePin(MotorDriverIN3_GPIO_Port, MotorDriverIN3_Pin, GPIO_PIN_SET);
		HAL_GPIO_WritePin(MotorDriverIN4_GPIO_Port, MotorDriverIN4_Pin, GPIO_PIN_RESET);
	}else if(direction == 1){
		HAL_GPIO_WritePin(MotorDriverIN3_GPIO_Port, MotorDriverIN3_Pin, GPIO_PIN_RESET);
		HAL_GPIO_WritePin(MotorDriverIN4_GPIO_Port, MotorDriverIN4_Pin, GPIO_PIN_SET);
	}else{
		Error_Handler();
	}
}

