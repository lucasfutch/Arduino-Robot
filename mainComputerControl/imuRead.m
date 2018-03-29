function data = imuRead(xBee)
    
    fwrite(xBee, char(0), 'char');

    while(xBee.BytesAvailable==0)
    end
    ax = str2double(fscanf(xBee))/16384;
    ay = str2double(fscanf(xBee))/16384;
    az = str2double(fscanf(xBee))/16384;
    
    gx = str2double(fscanf(xBee))*(250 / 32768);
    gy = str2double(fscanf(xBee))*(250 / 32768);
    gz = str2double(fscanf(xBee))*(250 / 32768);
    
    mx = str2double(fscanf(xBee))*(1200 / 4096);
    my = str2double(fscanf(xBee))*(1200 / 4096);
    mz = str2double(fscanf(xBee))*(1200 / 4096);

    data = [ax ay az gx gy gz mx my mz];
    
    
end