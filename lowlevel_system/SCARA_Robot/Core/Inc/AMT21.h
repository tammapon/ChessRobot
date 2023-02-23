/*
 * AMT21.h
 *
 *  Created on: Jan 21, 2022
 *      Author: fame
 */

#ifndef INC_AMT21_H_
#define INC_AMT21_H_

/*
 * Include
 */
#include "stm32f4xx_hal.h"
#include "stdint.h"
/*
 * STRUCT
 */
typedef struct {
	UART_HandleTypeDef *uartHandle;
	GPIO_TypeDef *DE_port;
	uint16_t DE_pin;
	uint8_t address;

	uint16_t uart_buf;
	uint16_t position;
	uint8_t k0;
	uint8_t k1;
} AMT21;


/*
 * FUNCTIONS
 */
void AMT21_initialize(AMT21 *dev, UART_HandleTypeDef *uartHandle,
		uint8_t address, GPIO_TypeDef *DE_port, uint16_t DE_Pin);
void AMT21_read_value(AMT21 *dev);
void AMT21_set_zero(AMT21 *dev);
void AMT21_reset(AMT21 *dev);
HAL_StatusTypeDef AMT21_check_value(AMT21 *dev);



#endif /* INC_AMT21_H_ */
