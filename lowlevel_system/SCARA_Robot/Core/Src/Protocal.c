/*
 * Protocal.c
 *
 *  Created on: Mar 8, 2022
 *      Author: Aon
 */
#include "Protocal.h"
#include "usart.h"
#include "stdio.h"

uint8_t checksum[2];
uint8_t data = 13;
uint8_t sum=0;

void CheckSum(uint8_t sum){
	char str[2];
	sum = ~sum;
	sum++;
	sprintf(str, "%x", sum);
	for (int i = 0; i<sizeof(checksum); i++) {
		checksum[i] = str[i];
	}
}

void clear_buffer(uint8_t package[],uint8_t size) {
    for (int i = 0; i<size; i++) {
        package[i] = 0;
    }
}

void package_state(uint8_t *state_check,uint8_t package[],uint8_t size) {
	uint8_t pack[size];
	memcpy(pack,package,size);
    for (int i = 1; i<size-2; i++) {
        sum += pack[i];
    }
    CheckSum(sum);
    if (pack[0] == 0xFF) { //header
        if (pack[11] == checksum[0] && pack[12] == checksum[1]) { //checksum
            if (pack[2] == 0x01) {
            	//jointjog
                *state_check = 1;
            } else if (pack[2] == 0x02) {
            	//to position
                *state_check = 2;
            } else if (pack[2] == 0x03) {
            	//run
                *state_check = 3;
            } else if (pack[2] == 0x04) {
				//req encoder
				*state_check = 4;
            } else if (pack[2] == 0x05) {
				//sethome
				*state_check = 5;
            } else {
                //err();
                clear_buffer(pack,size);
            }
        } else {
            //err();
            clear_buffer(pack,size);
        }
    } else {
        //err();
        clear_buffer(pack,size);
    }
    //memcpy(package,pack,size);
}

/*
//uint8_t checksum[2];
//uint8_t package[7];

char CheckSum (uint8_t sum) {
	char checksum[2];
	char str[2];
	sum = ~sum;
	sum++;
	sprintf(str, "%x", sum);
	for (int i = 0; i < sizeof(checksum); i++) {
		checksum[i] = str[i];
	}
	return (int)checksum;
}

void clear_buffer (uint8_t package[]) {
//    for (int i = 0; i<sizeof (checksum); i++) {
//		checksum[i] = 0;
//	}
    for (int i = 0; i<sizeof (package); i++) {
        package[i] = 0;
    }
}

uint8_t package_state (uint8_t package[7]) {
	uint8_t state_check = 0;
	uint8_t acknowledge[5] = {0xFF, 0x01, 0x01, 0x66, 0x65};
    uint8_t sum = 0;
    uint8_t checksum[2];

    for (int i = 1; i<sizeof (package) - 2; i++) {
        sum += package[i];
    }

//    checksum = CheckSum(sum);

    if (package[0] == 0xFF) {
        if (package[5] == checksum[0] && package[6] == checksum[1]) {
            if (package[2] == 0x01) {
            	//jointjog
            	HAL_UART_Transmit(&huart2,acknowledge,sizeof(acknowledge),100);
                state_check = 1;
            }
            else if (package[2] == 0x02) {
            	HAL_UART_Transmit(&huart2,acknowledge,sizeof(acknowledge),100);
            	state_check = 2;
            }
            else if (package[2] == 0x03) {
            	state_check = 3;
            }
            else {
                //err();
                clear_buffer(package);
            }
        }
        else {
            //err();
            clear_buffer(package);
        }
    }
    else {
        //err();
        clear_buffer(package);
    }
    return state_check;
}
*/
