void init_key_pins(char *row_pins, int size){
  for (int i; i<size; i++){
    pinMode(row_pins[i], OUTPUT);
    digitalWrite(row_pins[i], LOW);
  }  
}

void init_dumb_pins(){
  pinMode(dumb_switch_left,INPUT);
  digitalWrite(dumb_switch_left,HIGH);
  pinMode(dumb_switch_right,INPUT);
  digitalWrite(dumb_switch_right,HIGH);
}

void redefine_register(byte hand_pins[], int size, bool left) {
  for (int i; i<size;i++){
    pinMode(hand_pins[i], INPUT);
    digitalWrite(hand_pins[i], HIGH);
    delay(1);
    if(!digitalRead(hand_pins[i])){
      if (left) {
	curr_register_left |= (1<<i);
      }
      else {
	curr_register_right |= (1<<i);
      }
    }
    else{ 
      if (left) {
	curr_register_left &= ~(1<<i); 
      }
      else {
	curr_register_right &= ~(1<<i);
      }
    }
  }
}


void get_notes_to_play(char register_used[][5],byte button, byte reg_num, boolean on, boolean left){
  //Serial.println("gonna play a few notes");
  unsigned char note_of_12=0;
  unsigned char octave=0;
  unsigned char note_status_byte=0;
  unsigned char new_note=0;

  for (int c=0; c<5;c++){
    notes_to_play[c] = 0;
    switch(register_used[reg_num][c]) {
      case -125:
        // some logic here to handle special case detune up
        // just playing the same note now
	notes_to_play[c] = button + 0;
	break;
      case -126:
        // some logic here to handle special case detune down
        // just playing the same note now
	notes_to_play[c] = button + 0;    
	break;
      case -127:
	notes_to_play[c] = 0;
	break;
      default:  
	//checking if this exact note plays already
	// calculating note name(position in octave) and octave
	new_note = button + register_used[reg_num][c];
	octave = int(new_note/12);
	note_of_12 = new_note - octave*12;
	
	if (left) {
	  note_status_byte = LeftNotesStatus[note_of_12];
	}
	else {
	  note_status_byte = RightNotesStatus[note_of_12];
	}
	if (on != true){
	  notes_to_play[c] = new_note;  //sending midi OFF for all the registers
	  if (left){
	    LeftNotesStatus[note_of_12] &= ~(1 << octave) ;
	  }
	  else {
	    RightNotesStatus[note_of_12] &= ~(1 << octave) ; 
	  }
	  }

	if (note_status_byte & (1 << octave)) {
	  if (on & DEBUG){
	    Serial.print(" eating up ");
	    Serial.print(note_of_12,DEC); 
	    Serial.print(" note "); 
	    Serial.print(octave, DEC); 
	    Serial.print(" octave. status byte "); 
	    Serial.println(note_status_byte,BIN);
	  }

	} else {
	  notes_to_play[c] = new_note;
	  if (on) {
	    if (left){
	    LeftNotesStatus[note_of_12] |= (1 << octave) ; //setting up/down status
	    }
	    else {
	    RightNotesStatus[note_of_12] |= (1 << octave) ; //setting up/down status
	    }
	  }
	}
    }
  }
}
