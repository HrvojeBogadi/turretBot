/*
 * stm32f1xx_aci.h
 *
 * Application Communication Interface (ACI)
 *
 *  Created on: 6. lip 2021.
 *      Author: Hrvoje Bogadi
 *
 *      The application layer sends information in the form of left joystick and
 *	right joystick position. The positions are then recalculated into appropriate
 *	motor direction control signals and PWM signals.
 */

#include "main.h"

#ifndef INC_STM32F1XX_ACI_H_
#define INC_STM32F1XX_ACI_H_

void getInformationFromApplication(uint8_t *RxBuffer);

#endif /* INC_STM32F1XX_ACI_H_ */
