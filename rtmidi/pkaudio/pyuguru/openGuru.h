/***************************************************************************
                          openGuru.h  -  Read uGuru sensors
                             -------------------
    begin                : mån feb 28 2005
    copyright            : (C) 2005 by olle sandberg
    email                : ollebull@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/


/*
 * This file was modified by Patrick Stinson to fit the needs of the
 * uguru python module.
 */

// Two i/o-ports are used by uGuru
#define PORT_DATA 0xE4		// Mostly used to check if uGuru is busy
#define PORT_CMD 0xE0		// Used to tell uGuru what to read and read the
					// actual data

// Every sensor down to the RPM are placed in bank 1.
// Temp sensors
#define SENS_CPUTEMP		0x2100	// 255C max
#define SENS_SYSTEMP		0x2101	// 255C max
#define SENS_PWMTEMP		0x210F	// 255C max
// Voltage sensors
#define SENS_VCORE		0x2103	// 3.49V max
#define SENS_DDRVDD		0x2104	// 3.49V max
#define SENS_DDRVTT		0x210A	// 3.49V max
#define SENS_NBVDD		0x2108	// 3.49V max
#define SENS_SBVDD		0x210E	// 3.49V max
#define SENS_HTV			0x2102	// 3.49V max
#define SENS_AGP			0x2109	// 3.49V max
#define SENS_5V			0x2106	// 6.25V max
#define SENS_3V3			0x2105	// 4.36V max
#define SENS_5VSB		0x210B	// 6.25V max
#define SENS_3VDUAL		0x210D	// 4.36V max

// Fans. These are placed at bank 2
#define SENS_CPUFAN	    	0x2600	// 15300RPM max
#define SENS_NBFAN	   	0x2601	// 15300RPM max
#define SENS_SYSFAN	   	0x2602	// 15300RPM max
#define SENS_AUXFAN1    	0x2603	// 15300RPM max
#define SENS_AUXFAN2    	0x2604	// 15300RPM max


// Multipliers used to convert from the 8bit value to what the
// sensors should display. No multiplier for temps,
#define MLTP_3V49   		3.49f/255
#define MLTP_4V36   		4.36f/255
#define MLTP_6V25   		6.25f/255
#define MLTP_FAN    		15300/255

#define TRUE 	1
#define FALSE 	0


// Return TRUE if uGuru is detected
int uGuru_Detect (void);
// Put uGuru in ready state. uGuru will hold 0x08 at Data port and 0xAC at Command
// port after this.
int uGuru_Ready (void);
// End uGuru session
void uGuru_End (void);
// Read a sensor
unsigned char uGuru_ReadSensor (unsigned short SensorID);
