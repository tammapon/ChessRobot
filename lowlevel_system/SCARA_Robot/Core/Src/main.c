/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
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
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "spi.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

// #####################   Aon  Include   ################//
#include "Motor.h"
#include <string.h>
#include "Protocal.h"

// #####################   Klui Include   ################//
#include "stdio.h"
#include "AMT21.h"
#include "math.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

// #####################   Aon  typedef   ################//


// #####################   Klui typedef   ################//

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

// #####################   Aon  define   ################//


// #####################   Klui define   ################//
#define _USE_MATH_DEFINES
#define h1 371
#define h2 39.6
#define l1 486
#define l2 290

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

// #####################   Aon  Variable   ################//
Motor motor1;
Motor motor2;
Motor motor3;
Motor motor4;
int16_t PUL[2];

// #####################   Klui Variable   ################//
//serial gobol variable
uint8_t RX_Buffer[12]= {0};
uint8_t package[12];
uint8_t state_check = 0;
uint8_t uart_flag;
uint8_t sum_package=0;
//uint8_t state;
//uint8_t checksum[2];
uint8_t acknowledge[4] = {255, 1, 1, 1};

//timer flag
uint8_t control_flag;
uint8_t read_encoder_flag;
//encode variable
//amt103
int32_t encoder_1; //j1
int32_t encoder_2; //j2
//amt21
AMT21 encoder_3; //j3
AMT21 encoder_4; //j3
uint64_t err_count = 0;
uint64_t err_count1 = 0;
uint16_t Enc3_Pos;
uint16_t Enc4_Pos;
int64_t Pos_Joint3;
int32_t diff3;
//position read
float rpos[4]; //rad
float rpos_old[4];
//joint space var
float q1; //rad
float q2; //mm
float q3; //rad
float q4; //rad
//task space var
float rz;
float x;
float y;
float z;
//ref form highlevel
float rz_ref;
float x_ref;
float y_ref;
float z_ref;
float q1_ref;
float q2_ref;
float q3_ref;
float q4_ref;
//trajectory gen
float C[6][4];
float a,b,c;
float con_t = 0.005;
float t=0;
float pt[4];
float vt[4];
float at[4];
float p_start[4];
float p_final[4];
float v_start[4]={30,0,30,0};
float v_final[4]={30,0,30,0};
float a_start[4]={0,0,0,0};
float a_final[4]={0,0,0,0};
//PID
float POScurrent[4];
float POSlast[4];
float Pe[4];
float A[4]={0,0,0,0};
float V[4]={0,0,0,0};
float B[4]={0,0,0,0};
float kpp[4]={390,240,350,150};//{0.00000005,0,0,0};
float kpi[4]={0,0,0,0};
float kpd[4]={0,0,0,0};
//IK
int gramma=1;
int flag;

float v_rz;
float v_x;
float v_y;
float v_z;
float v_q1; //rad/s
float v_q2; //mm/s
float v_q3; //rad/s
float v_q4; //rad/s
float dq[4];
float timetraj=6.0;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

// ##############################################################   Aon  Declare Function   ################//
void Servo_Open (void);
void Servo_Close (void);
void setHome (void);

// ##############################################################   Klui  Declare Function   ################//
void CheckState(void);
void main_state(void);
void jogging(void);
void linearJog(void);
void update_q(void);
void read_position_ref(void);
void read_joint_ref(void);
void read_z_ref(void);
void traj_gen(float T);
void traj_eval(void);
void run(void);
void runz(void);
void control_J1(void);
void control_J2(void);
void control_J3(void);
void control_J4(void);
void IK(void);
//encoder test
void read_encoder(void);
void read_encoder2(void);
void enc2positionUnit(void);
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

// ##############################################################   Aon  Create Function Interrupt   #######################//


// ##############################################################   Klui Create Function Interrupt   #######################//
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
	uart_flag = 1;
	memcpy(package,RX_Buffer,12);
	HAL_UART_Receive_IT(&huart2, RX_Buffer, 12);
}

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim) {
// #################################   Aon  Call Timer Interrupt   ################################# //

// #################################   Klui Call Timer Interrupt   ################################# //
  if (htim == &htim6 )
  {
	  control_flag = 1;
  }
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USART2_UART_Init();
  MX_TIM1_Init();
  MX_TIM2_Init();
  MX_TIM3_Init();
  MX_TIM4_Init();
  MX_SPI2_Init();
  MX_USART3_UART_Init();
  MX_TIM6_Init();
  MX_TIM8_Init();
  MX_TIM5_Init();
  MX_TIM11_Init();
  /* USER CODE BEGIN 2 */

  // #################################################################   Aon  Initialize   ################//
  Motor_Initialize(&motor1, &htim3, TIM_CHANNEL_1, DIR_M1_GPIO_Port, DIR_M1_Pin, 15, 150); //M1
  Motor_Initialize(&motor2, &htim4, TIM_CHANNEL_1, DIR_M2_GPIO_Port, DIR_M2_Pin, 5, 1300); //M2
  Motor_Initialize(&motor3, &htim2, TIM_CHANNEL_3, DIR_M3_GPIO_Port, DIR_M3_Pin, 0, 700); //M3
  Motor_Initialize(&motor4, &htim1, TIM_CHANNEL_2, DIR_M4_GPIO_Port, DIR_M4_Pin, 10, 500); //M4
//  HAL_TIM_PWM_Start(&htim10, TIM_CHANNEL_1);

  // #################################################################   Klui Initialize   ################//
  HAL_TIM_Base_Start_IT(&htim6);

  AMT21_initialize(&encoder_3, &huart3, 0x34, MAX485_CONTROL_GPIO_Port, MAX485_CONTROL_Pin);
  AMT21_initialize(&encoder_4, &huart3, 0x04, MAX485_CONTROL_GPIO_Port, MAX485_CONTROL_Pin);

  HAL_UART_Receive_IT(&huart2, RX_Buffer, 12);
  HAL_TIM_Encoder_Start(&htim5, TIM_CHANNEL_ALL);
  HAL_TIM_Encoder_Start(&htim8, TIM_CHANNEL_ALL);
  TIM5->CNT = 100; //en1 init
  TIM8->CNT = 1000; //en2 init
  //AMT21_set_zero(&encoder_3);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */

// #########################   Aon  Variable    #########################//
//  Drive_Motor(&motor1, -70);
//  Drive_Motor(&motor2, 1200);
//  HAL_Delay(4000);
//  Drive_Motor(&motor1, 0);
//  Drive_Motor(&motor2, 0);
//  HAL_Delay(500);

// #########################   Klui  Variable   #########################//
  setHome();
//  Enc3_Pos = 0;
//  Enc4_Pos = 0;
  read_encoder();
  //init position
  q1 = -M_PI/2; //rad
  q2=0; //mm
  q3=(3*M_PI)/4; //rad
  q4=0; //rad
  enc2positionUnit();
  for(int i = 0;i<=4;i++){
	  rpos_old[i]=rpos[i];
  }
  read_encoder_flag=0;
  while (1)
  {
// #########################   Aon   #########################//
//	  if (!HAL_GPIO_ReadPin(Limit_M2_GPIO_Port, Limit_M2_Pin)) {
//	  		  HAL_GPIO_TogglePin(LED1_GPIO_Port, LED1_Pin);
//	  	  }

// #########################   Klui  #########################//
	  if (control_flag==1) {
//		  package_state(&state_check,package,sizeof(package));
		  main_state();
		  if(read_encoder_flag==0){
			  read_encoder();
			  read_encoder_flag=1;
		  }else{
			  read_encoder2();
			  read_encoder_flag=0;
		  }
		  update_q();
		  control_flag = 0;
	  }
	  if (uart_flag == 1) {
		  CheckState();
//		  if(state_check!=0){
//			  HAL_UART_Transmit(&huart2,acknowledge,sizeof(acknowledge),100);
//			  state_check=0;
//		  }
		  uart_flag = 0;
	  }

    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }

  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 8;
  RCC_OscInitStruct.PLL.PLLN = 180;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 2;
  RCC_OscInitStruct.PLL.PLLR = 2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Activate the Over-Drive mode
  */
  if (HAL_PWREx_EnableOverDrive() != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

// #########################   Aon   #########################//
void setHome (void) {
	while(1){
		if (control_flag==1) {
			if(read_encoder_flag==0){
				read_encoder();
				read_encoder_flag=1;
			}else{
				read_encoder2();
				read_encoder_flag=0;
			}
			if (HAL_GPIO_ReadPin(Limit_M1_GPIO_Port, Limit_M1_Pin) &&
				HAL_GPIO_ReadPin(Limit_M2_GPIO_Port, Limit_M2_Pin) &&
				(Enc3_Pos >= 3498 && Enc3_Pos <= 3502) &&
				( Enc4_Pos >= 1387 && Enc4_Pos <= 1393)) {
				Drive_Motor(&motor1, 0);
				Drive_Motor(&motor2, 0);
				Drive_Motor(&motor3, 0);
				Drive_Motor(&motor4, 0);
				TIM5->CNT = 100;
				TIM8->CNT = 1000;
				break;
			}
			if ( Enc3_Pos >= 3497 && Enc3_Pos <= 3503) {
				Drive_Motor(&motor3, 0);
			}
			else if (Enc3_Pos > 3503) {
				Drive_Motor(&motor3, 55);
			}
			else if (Enc3_Pos < 3497) {
				Drive_Motor(&motor3, -55);
			}
			if ( Enc4_Pos >= 1387 && Enc4_Pos <= 1393) {
				Drive_Motor(&motor4, 0);
			}
			else if (Enc4_Pos > 1393) {
				Drive_Motor(&motor4, 40);
			}
			else if (Enc4_Pos < 1387) {
				Drive_Motor(&motor4, -40);
			}
			if (!HAL_GPIO_ReadPin(Limit_M1_GPIO_Port, Limit_M1_Pin)) {
				Drive_Motor(&motor1, 70);
			}
			else Drive_Motor(&motor1, 0);
			if (!HAL_GPIO_ReadPin(Limit_M2_GPIO_Port, Limit_M2_Pin)) {
				Drive_Motor(&motor2, -1200);
			}
			else Drive_Motor(&motor2, 0);
			control_flag = 0;
		}
	}
//	HAL_Delay(1000);
}

void Servo_Open () {
	TIM10->CCR1 = 205; //
	HAL_Delay(1000);
}

void Servo_Close () {
	TIM10->CCR1 = 165; //keep
	HAL_Delay(1000);
}

// #########################   Klui  #########################//
void CheckState(void) {
    for (int i = 1; i<12-1; i++) {
        sum_package += package[i];
    }
    if (package[0] == 255) { //header
        if (package[11] == sum_package) { //checksum
            state_check = package[2];
            sum_package = 0;
        } else {
            //err();
        	for (int i = 0; i<12; i++) {
				package[i] = 0;
			}
        	sum_package = 0;
        }
    } else {
        //err();
    	for (int i = 0; i<12; i++) {
			package[i] = 0;
		}
    	sum_package = 0;
    }
    //memcpy(package,pack,size);
}

void main_state(void){
	//state_check > 1
	if (state_check == 1){
		jogging();
		HAL_UART_Transmit(&huart2,acknowledge,sizeof(acknowledge),100);
		state_check = 0;
	}
	else if (state_check == 2){
		read_position_ref();
		IK();
		p_start[0]=q1;
		p_start[1]=q2;
		p_start[2]=q3;
		p_start[3]=q4;
		p_final[0]=q1_ref;
		p_final[1]=q2_ref;
		p_final[2]=q3_ref;
		p_final[3]=q4_ref;
		for(int i=0;i<4;i++){
			v_start[i]=0;
			v_final[i]=0;
			a_start[i]=0;
			a_final[i]=0;
		}
		traj_gen(timetraj);
//		HAL_UART_Transmit(&huart2,acknowledge,sizeof(acknowledge),100);
		state_check = 4;
	}
	else if (state_check == 3){
		read_joint_ref();
		p_start[0]=q1;
		p_start[1]=q2;
		p_start[2]=q3;
		p_start[3]=q4;
		p_final[0]=q1_ref;
		p_final[1]=q2_ref;
		p_final[2]=q3_ref;
		p_final[3]=q4_ref;
		for(int i=0;i<4;i++){
			v_start[i]=0;
			v_final[i]=0;
			a_start[i]=0;
			a_final[i]=0;
		}
		traj_gen(timetraj);
//		HAL_UART_Transmit(&huart2,acknowledge,sizeof(acknowledge),100);
		state_check = 4;
	}
	else if (state_check == 4){
		run();
//		HAL_UART_Transmit(&huart2,acknowledge,sizeof(acknowledge),100);
//		state_check = 0;
	}
	else if (state_check == 5){
		setHome();
//		HAL_Delay(5000);
		HAL_UART_Transmit(&huart2,acknowledge,sizeof(acknowledge),100);
		state_check = 0;
		//init position
		q1 = -M_PI/2; //rad
		q2=0; //mm
		q3=(3*M_PI)/4; //rad
		q4=0; //rad
		enc2positionUnit();
		for(int i = 0;i<=4;i++){
		  rpos_old[i]=rpos[i];
		}
		read_encoder_flag=0;
	}
	else if (state_check == 6){
		if(package[10] == 1){
			Servo_Close();
		}
		else{
			Servo_Open();
		}
		HAL_UART_Transmit(&huart2,acknowledge,sizeof(acknowledge),100);
		state_check = 0;
	}
	else if (state_check == 7){
		read_z_ref();
		IK();
		p_start[1]=q2;
		p_final[1]=q2_ref;
		for(int i=0;i<4;i++){
			v_start[i]=0;
			v_final[i]=0;
			a_start[i]=0;
			a_final[i]=0;
		}
		traj_gen(5.0);
//		HAL_UART_Transmit(&huart2,acknowledge,sizeof(acknowledge),100);
		state_check = 8;
	}
	else if (state_check == 8){
		runz();
	}
}
void jogging (void) {
	switch (package[10]) {
		case 5:
			Drive_Motor(&motor1, 60);
			break;

		case 6 :
			Drive_Motor(&motor1, -60);
			break;
		case 7 :
			Drive_Motor(&motor2, -1200);
			break;

		case 8 :
			Drive_Motor(&motor2, 1200);
			break;

		case 9 :
			Drive_Motor(&motor3, 100);
			break;

		case 10 :
			Drive_Motor(&motor3, -100);
			break;

		case 11 :
			Drive_Motor(&motor4, 200);
			break;

		case 12 :
			Drive_Motor(&motor4, -200);
			break;

		case 1 :
			v_x = 60;
			v_y = 0;
			linearJog();
			break;

		case 3 :
			v_x = 0;
			v_y = 50;
			linearJog();
			break;

		case 2 :
			v_x = -60;
			v_y = 0;
			linearJog();
			break;

		case 4 :
			v_x = 0;
			v_y = -50;
			linearJog();
			break;

		case 255 :
			v_x = 0;
			v_y = 0;
			Motor_Stop_All();
			break;

		default:
			//err();
			//clear_buffer();
			v_x = 0;
			v_y = 0;
			Motor_Stop_All();
	}
}

void read_position_ref(void){
	rz_ref = (int16_t)(package[3]<<8)+(package[4]);
	x_ref = (int16_t)(package[5]<<8)+(package[6]);
	y_ref = (int16_t)(package[7]<<8)+(package[8]);
	z_ref = (int16_t)(package[9]<<8)+(package[10]);
	rz_ref = rz_ref/1000;
	x_ref = x_ref/10;
	y_ref = y_ref/10;
	z_ref = z_ref/10;
}
void read_z_ref(void){
	z_ref = (int16_t)(package[9]<<8)+(package[10]);
	z_ref = z_ref/10;
}
void read_joint_ref(void){
	q1_ref = (int16_t)(package[3]<<8)+(package[4]);
	q2_ref = (int16_t)(package[5]<<8)+(package[6]);
	q3_ref = (int16_t)(package[7]<<8)+(package[8]);
	q4_ref = (int16_t)(package[9]<<8)+(package[10]);
	q1_ref = q1_ref/1000;
	q2_ref = q2_ref/100;
	q3_ref = q3_ref/1000;
	q4_ref = q4_ref/1000;
}
void traj_gen(float T){
	for(int i=0;i<4;i++){
		C[0][i] = p_start[i];
		C[1][i] = v_start[i];
		C[2][i] = a_start[i]/2.0;
		a = p_final[i] - (p_start[i] + (v_start[i]*T) + (a_start[i]*(pow(T,2))/2));
		b = v_final[i] - (v_start[i] + (a_start[i]*T));
		c = a_final[i] - a_start[i];
		C[3][i] = (10.0*a/(pow(T,3))) - (4.0*b/(pow(T,2))) + (c/(2.0*T));
		C[4][i] = (-15.0*a/(pow(T,4))) + (7.0*b/(pow(T,3))) - (c/(pow(T,2)));
		C[5][i] = (6.0*a/(pow(T,5))) - (3.0*b/(pow(T,4))) + (c/(2.0*(pow(T,3))));
	}
}
void traj_eval(void){
	t += con_t;
	for(int i=0;i<4;i++){
		 pt[i] = C[0][i] + (C[1][i]*t) + (C[2][i]*(pow(t,2))) + (C[3][i]*(pow(t,3))) + (C[4][i]*(pow(t,4))) + (C[5][i]*(pow(t,5)));
		 vt[i] = C[1][i] + (2.0*C[2][i]*t) + (3.0*C[3][i]*(pow(t,2))) + (4.0*C[4][i]*(pow(t,3))) + (5.0*C[5][i]*(pow(t,4)));
		 at[i] = (2.0*C[2][i]) + (6.0*C[3][i]*t) + (12.0*C[4][i]*(pow(t,2))) + (20.0*C[5][i]*(pow(t,3)));
	}
}
void run(void){
	traj_eval();
	control_J1();
	control_J2();
	control_J3();
	control_J4();
	if(t>=timetraj){
		HAL_UART_Transmit(&huart2,acknowledge,sizeof(acknowledge),100);
		state_check=0;
		Motor_Stop_All();
		t=0;
	}
}
void runz(void){
	traj_eval();
	control_J2();
	if(t>=5.0){
		HAL_UART_Transmit(&huart2,acknowledge,sizeof(acknowledge),100);
		state_check=0;
		Motor_Stop_All();
		t=0;
	}
}

void control_J1(void){
//	float setpoint = pt[0];
	POScurrent[0] = q1;
//	POSlast[0] = POScurrent[0];
	Pe[0] = pt[0] - POScurrent[0];
	A[0] = A[0] + Pe[0];
	V[0] = (kpp[0] * Pe[0])+(kpi[0] * A[0])+(kpd[0] * (Pe[0] - B[0]));
	B[0] = Pe[0];
	Drive_Motor(&motor1, -V[0]);
}
void control_J2(void){
//	float setpoint = pt[0];
	POScurrent[1] = q2;
//	POSlast[0] = POScurrent[0];
	Pe[1] = pt[1] - POScurrent[1];
	A[1] = A[1] + Pe[1];
	V[1] = (kpp[1] * Pe[1])+(kpi[1] * A[1])+(kpd[1] * (Pe[1] - B[1]));
	B[1] = Pe[1];
	Drive_Motor(&motor2, V[1]);
}
void control_J3(void){
//	float setpoint = pt[0];
	POScurrent[2] = q3;
//	POSlast[0] = POScurrent[0];
	Pe[2] = pt[2] - POScurrent[2];
	A[2] = A[2] + Pe[2];
	V[2] = (kpp[2] * Pe[2])+(kpi[2] * A[2])+(kpd[2] * (Pe[2] - B[2]));
	B[2] = Pe[2];
	Drive_Motor(&motor3, -V[2]);
}
void control_J4(void){
//	float setpoint = pt[0];
	POScurrent[3] = q4;
//	POSlast[0] = POScurrent[0];
	Pe[3] = pt[3] - POScurrent[3];
	A[3] = A[3] + Pe[3];
	V[3] = (kpp[3] * Pe[3])+(kpi[3] * A[3])+(kpd[3] * (Pe[3] - B[3]));
	B[3] = Pe[3];
	Drive_Motor(&motor4, -V[3]);
}
void IK(void){
    q2_ref = h1 - h2 - z_ref;
    float c3 = ((pow(x_ref,2))+(pow(y_ref,2))-(pow(l1,2))-(pow(l2,2)))/(2*l1*l2);
    float s3 = gramma*(sqrt(1-(c3*c3)));
    q1_ref = atan2(y_ref,x_ref)-atan2(l2*s3,l1+(l2*c3));
    q3_ref = atan2(s3,c3);
    if(sqrt((x_ref*x_ref)+(y_ref*y_ref)) >= l1+l2){
        flag = 1;
    }
    else {flag = 0;}
    if (flag==0){
//        q4_ref = rz_ref+q1_ref+q3_ref;
    }
    else{
        //error
    }
}
//encoder function
void read_encoder(void){
	encoder_1 = (TIM5->CNT)-100;
	encoder_2 = (TIM8->CNT)-1000;
	AMT21_read_value(&encoder_3);
	HAL_StatusTypeDef rep3 = AMT21_check_value(&encoder_3);
	if (rep3 == HAL_ERROR){
		//err_count++;
	}
	else{
		Enc3_Pos = encoder_3.position;
	}
}
void read_encoder2(void){
	encoder_1 = (TIM5->CNT)-100;
	encoder_2 = (TIM8->CNT)-1000;
	AMT21_read_value(&encoder_4);
	HAL_StatusTypeDef rep4 = AMT21_check_value(&encoder_4);
	if (rep4 == HAL_ERROR){
		//err_count1++;
	}
	else{
		Enc4_Pos = encoder_4.position;
	}
}

void linearJog(void) {

	v_q1 = -(v_x*cos(q1 + q3))/(l1*cos(q1 + q3)*sin(q1)-l1*sin(q1 + q3)*cos(q1)) -
			(v_y*sin(q1 + q3))/(l1*cos(q1 + q3)*sin(q1)-l1*sin(q1 + q3)*cos(q1));
	v_q2 = v_z;
	v_q3 = (v_x*(l2*cos(q1 + q3) + l1*cos(q1)))/(l1*l2*cos(q1 + q3)*sin(q1) -
			l1*l2*sin(q1 + q3)*cos(q1)) + (v_y*(l2*sin(q1 + q3) + l1*sin(q1))) /
			(l1*l2*cos(q1 + q3)*sin(q1) - l1*l2*sin(q1 + q3)*cos(q1));
	v_q4 = v_rz - (v_x*cos(q1))/(l2*cos(q1 + q3)*sin(q1) - l2*sin(q1 + q3)*cos(q1)) -
			(v_y*sin(q1))/(l2*cos(q1 + q3)*sin(q1) - l2*sin(q1 + q3)*cos(q1));

	Drive_Motor(&motor1, -(int16_t)(v_q1*381.97186));
	Drive_Motor(&motor3, -(int16_t)(v_q3*381.97186));

}

void update_q(void){
	enc2positionUnit();
	q1 = q1+(rpos[0]-rpos_old[0]);
	q2 = q2+(rpos[1]-rpos_old[1]);
	q3 = q3+(rpos[2]-rpos_old[2]);
	q4 = q4+(rpos[3]-rpos_old[3]);
	for(int i = 0;i<4;i++){
		rpos_old[i]=rpos[i];
	}
}

void enc2positionUnit(void){
	rpos[0]=(2*M_PI*encoder_1)/8192; //rad
	rpos[1]=(5.0*encoder_2)/1600; //mm
	rpos[2]=(2*M_PI*Enc3_Pos)/4096; //rad
	rpos[3]=(2*M_PI*Enc4_Pos)/4096; //rad
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

