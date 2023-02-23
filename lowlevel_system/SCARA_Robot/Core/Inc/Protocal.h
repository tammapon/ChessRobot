/*
 * Protocal.h
 *
 *  Created on: Mar 8, 2022
 *      Author: Aon
 */
#include "stdint.h"
#include "stdio.h"

#ifndef INC_PROTOCAL_H_
#define INC_PROTOCAL_H_

void CheckSum(uint8_t sum);
void clear_buffer(uint8_t package[],uint8_t size);
void package_state(uint8_t *state_check,uint8_t package[],uint8_t size);

//char CheckSum(uint8_t sum);
//void clear_buffer(uint8_t package[]);
//uint8_t package_state(uint8_t package[]);

#endif /* INC_PROTOCAL_H_ */
