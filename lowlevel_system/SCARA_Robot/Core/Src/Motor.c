/*
 * Motor.c
 *
 *  Created on: Mar 6, 2022
 *      Author: Aon
 */

#include "Motor.h"

void Motor_Initialize (Motor *M, TIM_HandleTypeDef *Timer, uint32_t Channel,
		GPIO_TypeDef *GPIO_Port, uint16_t GPIO_Pin, int16_t min, int16_t max) {
	M->Timer = Timer;
	M->Channel = Channel;
	M->GPIO_Port = GPIO_Port;
	M->GPIO_Pin = GPIO_Pin;
	M->min = min;
	M->max = max;
	HAL_TIM_PWM_Start(Timer, Channel);
	__HAL_TIM_SET_COMPARE(M->Timer, M->Channel, 0);
}

void Drive_Motor (Motor *M, int16_t Hz) {
	if (Hz == 0) {
		__HAL_TIM_SET_COMPARE(M->Timer, M->Channel, 0);
	}
	else if (Hz > 0) {
		if (Hz > M->max) {Hz = M->max;}
		else if (Hz < M->min) {Hz = M->min;}
		M->Timer->Instance->ARR	= (60000/Hz)-1;
		HAL_GPIO_WritePin(M->GPIO_Port, M->GPIO_Pin, 1);
		__HAL_TIM_SET_COMPARE(M->Timer, M->Channel, (M->Timer->Instance->ARR+1)/2);
	}
	else if (Hz < 0){
		if (-Hz < M->min) {Hz = -M->min;}
		else if (-Hz > M->max) {Hz = -M->max;}
		M->Timer->Instance->ARR	= (60000/-Hz)-1;
		HAL_GPIO_WritePin(M->GPIO_Port, M->GPIO_Pin, 0);
		__HAL_TIM_SET_COMPARE(M->Timer, M->Channel, (M->Timer->Instance->ARR+1)/2);
	}
}

void Motor_Stop_All (void) {
	TIM3->CCR1 = 0;
	TIM4->CCR1 = 0;
	TIM2->CCR3 = 0;
	TIM1->CCR2 = 0;
}
