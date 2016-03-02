#include "NU32.h"          // constants, funcs for startup and UART
#include "LCD.h"
#include <stdio.h>

#define MSG_LEN 1000

int main() {
  char msg[MSG_LEN];
  char msg1[MSG_LEN];
  char msg2[MSG_LEN];
  char msg3[MSG_LEN];
  NU32_Startup();         // cache on, interrupts on, LED/button init, UART init
  LCD_Setup();



  //***********************Timer 3 Setup********************************
  T3CONbits.TCKPS = 0b101;     //Prescaler N=32
  PR3 = 50000;              //50Hz p = (PR+1)*N*12.5^-9  -->1600000/N = PR+1
  TMR3 = 0;                //Reset Timer 3 to 0
  T3CONbits.ON = 1;        //Turn Timer 3 on
  //********************************************************************


  //***********PWM TIMER 3 OC1 MOTOR pin D0 *********************************
  OC1CONbits.OCM = 0b110;  //PWM mode without fault pin; other OC1CON bits are defaults
  OC1CONbits.OCTSEL = 1;  //Connect to timer 3
  OC1RS = 2500;             //for 5% OC1RS/(PR3+1) = 5% --> 1ms
  OC1R = 2500;              //25%  
  OC1CONbits.ON = 1;       //Turn on OC1
  //****************************************************************


  //***********PWM TIMER 3 OC2 Servo 1 pin D1 *********************************
  OC2CONbits.OCM = 0b110;  //PWM mode without fault pin; other OC1CON bits are defaults
  OC2CONbits.OCTSEL = 1;  //Connect to timer 3
  OC2RS = 3750;             //for 5% OC2RS/(PR3+1) = 5% --> 1ms
  OC2R = 3750;              //25%
  OC2CONbits.ON = 1;       //Turn on OC2
  //****************************************************************


  //***********PWM TIMER 3 OC3 Servo 2 pin D2 *********************************
  OC3CONbits.OCM = 0b110;  //PWM mode without fault pin; other OC1CON bits are defaults
  OC3CONbits.OCTSEL = 1;  //Connect to timer 3
  OC3RS = 3750;             //for 5% OC3RS/(PR3+1) = 5% --> 1ms
  OC3R = 3750;              //25%
  OC3CONbits.ON = 1;       //Turn on OC3
  //****************************************************************

  

  int motor = 2500;
  int serv1 = 3750;
  int serv2 = 3750;
  NU32_LED1 = 0;
  NU32_LED2 = 0;

  while (1) {

    //NU32_WriteUART3("Type motor serv1 serv2 \r\n");
    
    NU32_ReadUART3(msg, MSG_LEN);             // get the response
     
    

    LCD_Move(0,0);
    LCD_Clear();
    LCD_WriteString(msg);

    NU32_LED1 = 1;

    char * split;
    split = strtok (msg,",");
    sprintf (msg1, "%s", split);    
    split = strtok (NULL, ",");
    sprintf (msg2, "%s", split);
    split = strtok (NULL, ",");
    sprintf (msg3, "%s", split);

    motor = atoi(msg1);
    serv1 = atoi(msg2);
    serv2 = atoi(msg3);
    NU32_LED2 = 1;

       
    if(serv1>1500 && serv1<6000){//safe range
      OC2RS = serv1;
    }
    if(serv2>1500 && serv2<6000){//safe range
      OC3RS = serv2;
    }       
    OC1RS = motor;

    //sprintf(msg2, "\nm=%d, s1=%d, s2=%d\r\n", OC1RS, OC2RS, OC3RS);    
    //NU32_WriteUART3(msg2);    
    //NU32_WriteUART3("\r\n");


    int i = 0;
    for (i=0; i<50000; i++)
      asm("nop");

  }
  return 0;
}
