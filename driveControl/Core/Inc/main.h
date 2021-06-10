/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"


/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

#include "stm32f1xx_misc.h"
/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */
enum motorDirection{FORWARD, BACKWARD};

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define RightMotorPWM_Pin GPIO_PIN_8
#define RightMotorPWM_GPIO_Port GPIOA
#define LeftMotorPWM_Pin GPIO_PIN_9
#define LeftMotorPWM_GPIO_Port GPIOA
#define MotorDriverIN1_Pin GPIO_PIN_10
#define MotorDriverIN1_GPIO_Port GPIOA
#define MotorDriverIN2_Pin GPIO_PIN_11
#define MotorDriverIN2_GPIO_Port GPIOA
#define MotorDriverIN3_Pin GPIO_PIN_15
#define MotorDriverIN3_GPIO_Port GPIOA
#define MotorDriverIN4_Pin GPIO_PIN_3
#define MotorDriverIN4_GPIO_Port GPIOB
#define LeftMotorOpto_Pin GPIO_PIN_7
#define LeftMotorOpto_GPIO_Port GPIOB
#define LeftMotorOpto_EXTI_IRQn EXTI9_5_IRQn
#define RightMotorOpto_Pin GPIO_PIN_8
#define RightMotorOpto_GPIO_Port GPIOB
#define RightMotorOpto_EXTI_IRQn EXTI9_5_IRQn
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
