#include "NU32.h"          // constants, funcs for startup and UART
#include "LCD.h"

#define MSG_LEN 100

int main() {
  char msg[MSG_LEN];

  NU32_Startup();         // cache on, interrupts on, LED/button init, UART init
  //LCD_Setup();



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
  OC2RS = 375;             //for 5% OC2RS/(PR3+1) = 5% --> 1ms
  OC2R = 375;              //25%
  OC2CONbits.ON = 1;       //Turn on OC2
  //****************************************************************


  //***********PWM TIMER 3 OC3 Servo 2 pin D2 *********************************
  OC3CONbits.OCM = 0b110;  //PWM mode without fault pin; other OC1CON bits are defaults
  OC3CONbits.OCTSEL = 1;  //Connect to timer 3
  OC3RS = 375;             //for 5% OC3RS/(PR3+1) = 5% --> 1ms
  OC3R = 375;              //25%
  OC3CONbits.ON = 1;       //Turn on OC3
  //****************************************************************

  

  int motor = 2500;
  int serv1 = 375;
  int serv2 = 375;

  while (1) {
    //OC1RS = 2500;    //for 5% OC1RS/(PR3+1) = 5% --> 1ms
    NU32_WriteUART3("Type motor serv1 serv2 \r\n");
    NU32_LED1 = 0;
    NU32_ReadUART3(msg, MSG_LEN);             // get the response
    sscanf(msg, "%d %d %d", motor, serv1, serv2);

    if(serv1>150 && serv1<600){//safe range
      OC2RS = serv1;
    }
    if(serv2>150 && serv2<600){//safe range
      OC3RS = serv2;
    }

    sprintf(msg, "motor = %d, s1 = %d, s2 = %d\r\n", motor, serv1, serv2);//testing
    NU32_WriteUART3(msg);//testing
    NU32_LED1 = 1;
    OC1RS = motor;


    int i = 0;
    for (i=0; i<50000; i++)
      asm("nop");
  }
  return 0;
}
