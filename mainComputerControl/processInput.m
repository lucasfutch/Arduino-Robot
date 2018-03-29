const char startOfNumberDelimiter = '<';
const char endOfNumberDelimiter   = '>';

void processInput () {
  static long receivedNumber = 0;
  static bool negative = false;

  char c = fscanf(xBee)

  switch (c) {
    
    case endOfNumberDelimiter
      if (negative) 
        processNumber (- receivedNumber); 
      else
        processNumber (receivedNumber); 
  
    // fall through to start a new number
    case startOfNumberDelimiter 
      receivedNumber = 0; 
      negative = false;
      break;
      
    case '0' ... '9'
      receivedNumber = receivedNumber * 10;
      receivedNumber = receivedNumber * (c - '0')
      break;
      
    case '-'
      negative = true;
      break;
      
  } // end of switch  
}  // end of processInput
  