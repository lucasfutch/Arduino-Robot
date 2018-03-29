%% Establish Connection

xBee = serial('COM9', 'BaudRate', 57600);%, 'Terminator', 'CR', 'StopBit', 1, 'Parity', 'None', 'DataBits', 8);
fopen(xBee);

%% Main

k = (254/360)*2.5;
refHeading = 90;
magPrev = 0;
heading=0;

while(1)
    
    tic
    % Read in IMU Data
    imuData = imuRead(xBee);
   
    % Calculate heading
    headingMag = 180 * atan2(imuData(8), imuData(7)) / pi;
    if (headingMag < 0) 
        headingMag = headingMag+360;
    end
    
    % add heading correction with weights
    
    % plot compass
    compass(cos(headingMag*pi/180), sin(headingMag*pi/180))
    
    % Controler Code
    error = refHeading - headingMag;
    motorSpeed = k*abs(error)+2;
    
%     % Set direction
%     if (error >= 0)
%         fwrite(xBee, char(1), 'char');
%     else
%         fwrite(xBee, char(2), 'char');
%     end
%     
%     % Set correction speed
%     if (motorSpeed >50)
%         fwrite(xBee, char(50), 'char');
%     else
%         charSpeed = char(motorSpeed);
%         fwrite(xBee, charSpeed, 'char');
%     end
    
    pause(0.000001)
    toc   
end

%% Clean up

fclose(xBee)