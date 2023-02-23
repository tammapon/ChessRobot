/*
 * Motor.h
 *
 *  Created on: Mar 6, 2022
 *      Author: Aon
 */

#ifndef INC_MOTOR_H_
#define INC_MOTOR_H_

#include "stm32f4xx_hal.h"

typedef struct Motor {
	TIM_HandleTypeDef *Timer;
	uint32_t Channel;
	GPIO_TypeDef *GPIO_Port;
	uint16_t GPIO_Pin;
	int16_t min;
	int16_t max;
}Motor;

void Drive_Motor (Motor *M, int16_t Hz);

void Motor_Initialize (Motor *M, TIM_HandleTypeDef *Timer, uint32_t Channel, GPIO_TypeDef *GPIO_Port, uint16_t GPIO_Pin, int16_t main, int16_t max);

void Motor_Stop_All (void);

#endif /* INC_MOTOR_H_ */
