/*
 MIDI accordion for Mega
 Dimon Yegorenkov
 alpha from 03-10-2010
 optointerruptors version 14-11-2010
 beta 12-12-2010

*/

#include <WProgram.h>
#include <LiquidCrystal.h>


// this part of reading BMP085 sensor
#include <Wire.h>
#define I2C_ADDRESS 0x77 //77?
const unsigned char oversampling_setting = 0; //oversamplig for measurement
const unsigned char pressure_waittime[4] = { 5, 8, 14, 26 };

boolean DEBUG = true;

//just taken from the BMP085 datasheet
int ac1;
int ac2; 
int ac3; 
unsigned int ac4;
unsigned int ac5;
unsigned int ac6;
int b1; 
int b2;
int mb;
int mc;
int md;


// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(31,30,29,28,27,26,25,24,23,22);


char st_0[] = "unknown";
char st_30[] = "F#";
char st_31[] = "G";
char st_32[] = "G#";
char st_33[] = "A";
char st_34[] = "A#";
char st_35[] = "B";
char st_36[] = "C2";
char st_37[] = "C#2";
char st_38[] = "D2";
char st_39[] = "D#2";
char st_40[] = "E2";
char st_41[] = "F2";
char st_42[] = "F#2";
char st_43[] = "G2";
char st_44[] = "G#2";
char st_45[] = "A2";
char st_46[] = "А#2";
char st_47[] = "B2";
char st_48[] = "C3";
char st_49[] = "C#3";
char st_50[] = "D3";
char st_51[] = "D#3";
char st_52[] = "E3";
char st_53[] = "F3";
char st_54[] = "F#3";
char st_55[] = "G3";
char st_56[] = "G#3";
char st_57[] = "A3";
char st_58[] = "A#3";
char st_59[] = "B3";
char st_60[] = "C4";
char st_61[] = "C#4";
char st_62[] = "D4";
char st_63[] = "D#4";
char st_64[] = "E4";
char st_65[] = "F4";
char st_66[] = "F#4";
char st_67[] = "G4";
char st_68[] = "G#4";
char st_69[] = "A4";
char st_70[] = "A#4";
char st_71[] = "B4";
char st_72[] = "C5";
char st_73[] = "C#5";
char st_74[] = "D5";
char st_75[] = "D#5";
char st_76[] = "E5";
char st_77[] = "F5";
char st_78[] = "F#5";
char st_79[] = "G5";
char st_80[] = "G#5";
char st_81[] = "A5";
char st_82[] = "A#5";
char st_83[] = "B5";
char st_84[] = "C6";
char st_85[] = "C#6";
char st_86[] = "D6";
char st_87[] = "D#6";
char st_88[] = "E6";
char st_89[] = "F6";
char st_90[] = "F#6";
char st_91[] = "G6";
char st_92[] = "G#6";
char st_93[] = "A6";


#include <avr/pgmspace.h>
//  these pins have not to be configured one by one, numbers just for reference,
//  that's 8 lines of PortF and they are read as a byte later.

char left_row_pins[] = { 12, 11, 10};
char right_row_pins[] = { 2, 3, 4, 5, 6, 7};
//const unsigned char right_row_pins[] = { 2};


//byte reg_f_values = 0;
//byte reg_k_values = 0;
byte reg_values = 0;

// array to store up/down status of left keys
int LeftKeysStatus[] = {  
  B0000000,
  B0000000,
  B0000000
};

// array to store up/down status of right keys
int RightKeysStatus[] = {  
  B0000000,
  B0000000,
  B0000000,
  B0000000,
  B0000000,
  B0000000
};

// store in program memory to save RAM
const prog_char notes_in_bytes[][8] = {
 {'F','F2','E','E2','D#','D#2','D','D2'},
 {'C#','C#2','C','C2','B','B2','A#','A#2'},
 {'A','A2','G#','G#2','G','G2','F#','F#2'}
  };

const prog_char *left_note_names[][8] = {
  {st_62,st_38,st_63,st_39,st_64,st_40,st_65,st_41},
  {st_58,st_46,st_59,st_47,st_60,st_36,st_61,st_37},
  {st_54,st_42,st_55,st_43,st_56,st_44,st_57,st_45}
};


const prog_char left_notes_midi_numbers[][8] = {
  {62,38,63,39,64,40,65,41},
  {58,46,59,47,60,36,61,37},
  {54,42,55,43,56,44,57,45}
  };

const prog_char *right_note_names[][8] = {
  {st_60,st_59,st_58,st_57,st_56,st_55,st_54,st_53},
  {st_68,st_67,st_66,st_65,st_64,st_63,st_62,st_61},
  {st_76,st_75,st_74,st_73,st_72,st_71,st_70,st_69},
  {st_84,st_83,st_82,st_81,st_80,st_79,st_78,st_77},
  {st_92,st_91,st_90,st_89,st_88,st_87,st_86,st_85},
  {0,0,0,0,0,0,0,st_93}
  };

const prog_char right_notes_midi_numbers[][8] = {
  {60,59,58,57,56,55,54,53},
  {68,67,66,65,64,63,62,61},
  {76,75,74,73,72,71,70,69},
  {84,83,82,81,80,79,78,77},
  {92,91,90,89,88,87,86,85},
  {0,0,0,0,0,0,0,93}
  };


int LeftNotesStatus[]={
  B0000000,
  B0000000,
  B0000000,
  B0000000,
  B0000000,
  B0000000, 
  B0000000,
  B0000000,
  B0000000,
  B0000000,
  B0000000,
  B0000000 
};

int RightNotesStatus[]={
  B0000000,
  B0000000,
  B0000000,
  B0000000,
  B0000000,
  B0000000, 
  B0000000,
  B0000000,
  B0000000,
  B0000000,
  B0000000,
  B0000000
};

byte register_pins_right[] = {32,33,34,35};
byte register_pins_left[] =  {36,37,38};
bool use_left_register = 1;
bool use_right_register = 1;
byte midi_channel_num_right[] = {39,40};
byte midi_channel_num_left[] = {41,42};

char st_regR_1[] = "Piccolo";
char st_regR_2[] = "Clarinet";
char st_regR_3[] = "Bassoon";
char st_regR_4[] = "Oboe";
char st_regR_5[] = "Violin";
char st_regR_6[] = "Musette";
char st_regR_7[] = "MusetteR";
char st_regR_8[] = "Organ";
char st_regR_9[] = "Harmonium";
char st_regR_10[] = "Bandoneon";
char st_regR_11[] = "Accordion";
char st_regR_12[] = "Master";

const prog_char *register_names_right[] = {
  st_regR_1,st_regR_2,st_regR_3,st_regR_4,st_regR_5,st_regR_6,st_regR_7,st_regR_8,st_regR_9,st_regR_10,st_regR_11,st_regR_12
};

// adding special case -127 never happens in accord, so, using to mute the register
// special case -126 means same note tuned slightly lower than the basic middle reed rank
// special case -125 means same note tuned slightly higher than the basic middle reed rank
// some day we will handle that by the tunings of different MIDI channels. why not.
// here [12][4] just because all reels are never turned on at once. richest sound will be screwed up with middle (say Clarinet) line

char register_right_changes[][5] = {
  {12,-127,-127,-127},
  {0,-127,-127,-127},
  {-12,-127,-127,-127},
  {12,0,-127,-127},
  {0,-125,-127,-127},
  {12,0,-125,-127},
  {-126,0,-125,-127},
  {12,-12,-127,-127},
  {12,0,-12,-127},
  {0,-12,-127,-127},
  {0,-12,-126,-127},
  {12,-125,-126,-12}
};

char st_regL_1[] = "Soprano";
char st_regL_2[] = "Alto";
char st_regL_3[] = "Tenor";
char st_regL_4[] = "Master";
char st_regL_5[] = "S Bass";
char st_regL_6[] = "S Tenor";
char st_regL_7[] = "Bass";


const prog_char *register_names_left[] = {
  st_regL_1,st_regL_2,st_regL_3,st_regL_4,st_regL_5,st_regL_6,st_regR_7
};


// [7][5] because all the reels are used in left hand
// special case -126 uses 36,37,38,39,40,41,30,31,32,33,34,35 octave


char register_left_changes[][5] = {
  {0,-127,-127,-127,-127},
  {24,-127,-127,-127,-127},
  {24,12,-127,-127,-127},
  {24,12,0,-127,-127},
  {24,12,0,-12,-126},
  {-12,0,-126,-127,-127},
  {12,0,-127,-127,-127},
  {-12,12,24,-127,-127}
};



char notes_to_play[5];
byte curr_register_left = 0;
byte curr_register_right = 0;


byte ledPin = 13; 
byte midi_channel1 = 0;
byte midi_channel2 = 1;
byte midi_volume_ctrl = 0xB0;
int lastUpdate = 0;
byte curr_velocity = 127;
byte velocity = 127;
boolean velocity_active = false;
int time = micros();
int temperature = 0;
long pressure = 0;
long calibration_pressure = 0;
int delta_pressure=0;
int pressure_counter = 0;
int pressure_loops = 2;
int min_pressure = -4000;
int max_pressure = +4000;
int pressure_step = max_pressure/127;

struct tag {
    char lname[20];      /* last name */
    char fname[20];      /* first name */
    int age;             /* age */
    float rate;          /* e.g. 12.75 per hour */
};

struct tag my_struct;       /* declare the structure my_struct */



void setup() {  
  Serial1.begin(115200);  // start bluetooth midi port
  Wire.begin();
  bmp085_get_cal_data();
  //  start debug port:
  Serial.begin(115200);
  if (DEBUG){  Serial.println("Setting up BMP085 or what?");};
  //pinMode(ledPin, OUTPUT);
  // set up the LCD's number of columns and rows: 
  lcd.begin(8, 2);
  // Print a message to the LCD.
  lcd.print("ready!");
  for (int i=0; i<32; i++){
    calibration_pressure += bmp085_read_up();
  }
  calibration_pressure = calibration_pressure/32;

  lcd.println("calibration");
  // initializing keyboard byte select pins
  init_key_pins(right_row_pins,sizeof(right_row_pins));
  init_key_pins(left_row_pins,sizeof(right_row_pins));

  // read register value from hardcoded setup
  redefine_register(register_pins_right, sizeof(register_pins_right), false);
  redefine_register(register_pins_left, sizeof(register_pins_left), true);

  
  if (DEBUG){
    Serial.println("value of registers right/left");
    Serial.println(register_names_right[curr_register_right]);
    Serial.println(register_names_left[curr_register_left]);
  }
  
  for (int i; i<sizeof(register_pins_left); i++){
    pinMode(i, INPUT);
    digitalWrite(i, HIGH);
  }  

  // activity marker
  pinMode(13, OUTPUT);   
  // PortF as left input and turn on pullup resistors
  DDRF = B00000000;
  PORTF = B11111111; 
  // PortK as right input and turn on pullup resistors
  DDRK = B00000000;
  PORTK = B11111111; 
  //blink(5,20);
  if (DEBUG){
    for (int i=0; i<20; i++){
      time_delta("start");
      scan_keys(left_row_pins, sizeof(left_row_pins), LeftKeysStatus, true); 
      scan_keys(right_row_pins, sizeof(left_row_pins), RightKeysStatus, false);
    }
  Serial.println(calibration_pressure);
  time_delta("stop");
  Serial.println("stop of setup");
  }
}



void time_delta(String message){
  int newtime = micros();
  Serial.print(message);
  Serial.println(newtime - time);
  time=newtime;
}

void bmp085_read_temperature_and_pressure(int& temperature, long& pressure);

//int my_abs(int i){
//  //return i < 0 ? -i : i;
//  return i;
//}

void noteOn(int midi_cmd, int pitch, int midi_vel){
  Serial1.print(midi_cmd, BYTE);
  Serial1.print(pitch, BYTE);
  Serial1.print(midi_vel, BYTE);
}

void loop() {
  //use this, take most from arduino language 
  // apply the calibration to the sensor reading
  //sensorValue = map(sensorValue, sensorMin, sensorMax, 0, 255);
  // in case the sensor value is outside the range seen during calibration
  //sensorValue = constrain(sensorValue, 0, 255);  


  pressure = bmp085_read_up();    
  delta_pressure = abs(pressure - calibration_pressure);
  //    noteOn(midi_volume_ctrl,0x07,delta_pressure/pressure_step);    
  // setting up minimal pressure to start a sound
  if (delta_pressure < 10){
    // we have to get to send message controller to zero once it got to zero
    if (curr_velocity>0){
      noteOn(midi_volume_ctrl,0x0B,0);
      //Serial.println("Zero crossed");
      curr_velocity = 0;
    }
  }
  else { 
    velocity_active = true;
  }
  // log(0) is a bad style
  if(delta_pressure > 0){
    velocity = int((log(float(delta_pressure)/100.0)+4.8)/0.03814) ;
  }
  else {
    velocity = 0;
  }
  //Serial.print("vel ");
  //Serial.print(velocity, DEC);
  if ((velocity_active) && (curr_velocity != velocity)) {
    noteOn(midi_volume_ctrl,0x0B,velocity);
    curr_velocity = velocity;
    velocity_active = false;
    //Serial.print("Velocity ");
    //Serial.println(curr_velocity, DEC);
  }

    //    pressure_counter = pressure_loops;
  
  
  scan_keys(left_row_pins, sizeof(left_row_pins), LeftKeysStatus, true); 
  scan_keys(right_row_pins, sizeof(right_row_pins), RightKeysStatus, false);
  //delay(100);
}

void blink(int pin, int cycles){
  for (int a=0;a<cycles;a++){
    digitalWrite(pin,!digitalRead(pin));
    delay(50);
  }
}

void scan_keys(char *row_pins, int size, int *KeysStatus, bool left) {
  //delay(1000);  
  for (int i=0; i<size;i++){    
    digitalWrite(row_pins[i], HIGH);
    delayMicroseconds(500);      
    //delay(300);
    if (left) {
      reg_values = ~PINF;
    }
    else {
      reg_values = ~PINK;
      }
    digitalWrite(row_pins[i], LOW);
    // checking for activity
    // "if{} inside if{}" is to save time if nothing happens
    if (reg_values != KeysStatus[i]){
      if (reg_values > KeysStatus[i]){             
          check_key(reg_values ^ KeysStatus[i],i,true,left);  //sending modified bits only
      }
      else {
	check_key(reg_values ^ KeysStatus[i],i,false,left); //sending modified bits only
      }           
    }        
  }
 
}

void check_key(int reg, int group, boolean up, boolean left){
   // saving 4 iterations, dividing byte by 2
   if (reg & 0xF0) {
     for(int i=0; i<4; i++){
       if ((reg >> 4+i) & 1){
	 if (left) {
	   note_midi(group,i+4,up,register_left_changes,left);
	 }
	 else {
	   note_midi(group,i+4,up,register_right_changes,left);
	 }
       }
     }
   }
   else if (reg & 0x0F) { 
    for(int i=0; i<4; i++){
       if ((reg >> i) & 1){
	 if (left) {
	   note_midi(group,i,up,register_left_changes,left);
	 }
	 else{
	   note_midi(group,i,up,register_right_changes,left); 
	 }
       }
     }     
   }
}


void note_midi(int group, int position, boolean on, char register_used[][5], boolean left){
  int pitch;
  String str_warn;
  char midi_cmd;
  char curr_register;
  char midi_vel;

  if (left){
    pitch = left_notes_midi_numbers[group][position];
    curr_register = curr_register_left;
  }
  else{
    pitch = right_notes_midi_numbers[group][position];
    curr_register = curr_register_right;
  }


  if (on & left){
    str_warn = "Left note gets on ";
    midi_cmd = midi_channel1 | 0x90;
    LeftKeysStatus[group] |= (1 << position);  //setting bit value
    midi_vel = curr_velocity;
  }
  else if (~on & left) {
    str_warn = "Left note gets off ";
    midi_cmd = midi_channel1 | 0x80;
    LeftKeysStatus[group] &= ~(1 << position);  //setting bit value
    midi_vel = 0;
  }
  else if(on & ~left) {
    str_warn = "Right note gets on ";
    midi_cmd = midi_channel2 | 0x90;
    RightKeysStatus[group] |= (1 << position);  //setting bit value
    midi_vel = curr_velocity;
  }
  else if(~on & ~left) {
    str_warn = "Right note gets off ";
    midi_cmd = midi_channel2 | 0x80;
    RightKeysStatus[group] &= ~(1 << position);  //setting bit value
    midi_vel = 0;
  }
    
  if (DEBUG){
    Serial.print(str_warn);
    Serial.print(pitch,DEC);
    Serial.print(" ");
    if (left) {
      Serial.println(left_note_names[group][position]);
    }
    else {
      Serial.println(right_note_names[group][position]); 
    }
    Serial.println(delta_pressure);
  };
  //MIDI output is more complex, number of notes sent depends on register
  if (left){
    if (use_left_register){
      get_notes_to_play(register_used, left_notes_midi_numbers[group][position], curr_register, on, left);
    }
    else {
      notes_to_play[0] = left_notes_midi_numbers[group][position];
      notes_to_play[1] = 0;
      notes_to_play[2] = 0;
      notes_to_play[3] = 0;
      notes_to_play[4] = 0;
    }
  }
  else{
    if (use_right_register){
      get_notes_to_play(register_used, right_notes_midi_numbers[group][position], curr_register, on, left);
    }
    else{
      notes_to_play[0] = right_notes_midi_numbers[group][position];
      notes_to_play[1] = 0;
      notes_to_play[2] = 0;
      notes_to_play[3] = 0;
      notes_to_play[4] = 0;
    }
  }
  for (int i=0; i<sizeof(notes_to_play);i++){
    if (notes_to_play[i]){
      Serial1.print(midi_cmd, BYTE);
      Serial1.print(notes_to_play[i], BYTE);
      Serial1.print(midi_vel, BYTE);
      if(DEBUG){
	Serial.print(" ");
	Serial.print(notes_to_play[i],DEC);
      }
    }
   
  }
if (DEBUG) {Serial.println(" notes");}
  // LCD output
  //lcd.clear();
  lcd.print(left_note_names[group][position]);
  lcd.print(curr_velocity);
}


void diode(){
  //digitalWrite(ledPin,!digitalRead(ledPin));
}




