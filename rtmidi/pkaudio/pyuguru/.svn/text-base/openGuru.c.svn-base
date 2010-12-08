/***************************************************************************
                          openGuru.c  -  description
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


#include <sys/io.h>
#include "openGuru.h"


/* Return: 
 *   TRUE if uGuru is detected
 *   FALSE if uGuru is not detected.
 *   -1 if permission denied
 */  
int
uGuru_Detect (void)
{
  int ret1;
  int ret2;

  unsigned char portData, portCommand;

  // Get i/o acces to the uGuru ports
  ret1 = ioperm (PORT_CMD, 1, TRUE);
  ret2 = ioperm (PORT_DATA, 1, TRUE);

  if (ret1 || ret2)
    return -1;

  // Read the ports
  portData = inb (PORT_DATA);
  portCommand = inb (PORT_CMD);

  // ***** Detect uGuru
  // After a reboot uGuru will hold 0x00 at data and 0xAC at Command. When this program
  // have end the ports will hold 0x08 at Data and 0xAC at Command, that's why we need to test both
  // combinations at the Data port.
  if (((portData == 0x00) || portData == 0x08) && (portCommand == 0xAC))
    {
      // uGuru was detected so put uGuru in ready state and return TRUE.
      uGuru_Ready ();
      return TRUE;
    }
  // uGuru was not detected
  return FALSE;
}


// Put uGuru in ready state. uGuru will hold 0x08 at Data port and 0xAC at Command port after this.
int
uGuru_Ready (void)
{
  int LockupCnt1 = 0;
  int LockupCnt2 = 0;

  // Wait until uGuru is in ready-state
  // The loop shouldn't be needed to execut more then one time
  while (inb (PORT_DATA) != 0x08)
    {
      outb (0x00, PORT_DATA);	// after 0x00 is written to Data port

      // Wait until 0x09 is read at Data port
      while (inb (PORT_DATA) != 0x09)
	{
	  // Prevent a lockup
	  if (LockupCnt2++ > 1000)
	    return FALSE;
	}

      LockupCnt2 = 0;

      // Wait until 0xAC is read at Cmd port
      while (inb (PORT_CMD) != 0xAC)
	{
	  // Prevent a lockup
	  if (LockupCnt2++ > 1000)
	    return FALSE;
	}

      // Prevent a lockup
      if (LockupCnt1++ > 1000)
	return FALSE;
    }

  return TRUE;
}

// Read a sensor
unsigned char
uGuru_ReadSensor (unsigned short SensorID)
{
  unsigned char SensorResult;
  unsigned char Port_hAddr, Port_lAddr;
  int LockupCnt = 0;

  // Get the high and low byte of address
  Port_hAddr = ((0xFF00 & SensorID) >> 8);
  Port_lAddr = (0x00FF & SensorID);

  // Ask to read from uGuru
  outb (Port_hAddr, PORT_DATA);	// Out BankID @ Data

  // I guess this is to se if uGuru is ready to take a command
  while (inb (PORT_DATA) != 0x08)	// In 0x08 @ Data
    {
      // Prevent a lockup
      if (LockupCnt++ > 1000)
	return FALSE;
    }
  // Whitch sensor to read?
  outb (Port_lAddr, PORT_CMD);	// Out Sensor ID @ Cmd

  LockupCnt = 0;
  // Wait until uGuru is ready to be read
  while (inb (PORT_DATA) != 0x01)
    {
      // Prevent a lockup
      if (LockupCnt++ > 1000)
	return FALSE;
    }

  // Read the sensor
  SensorResult = inb (PORT_CMD);

  // Put the chip in ready state
  uGuru_Ready ();

  // Return the result of the sensor
  return SensorResult;

}
