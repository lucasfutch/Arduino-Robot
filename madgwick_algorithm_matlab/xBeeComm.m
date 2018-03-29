
xBee = serial('COM9', 'BaudRate', 57600);%, 'Terminator', 'CR', 'StopBit', 1, 'Parity', 'None', 'DataBits', 8);
fopen(xBee);


%%
% addpath('quaternion_library');      % include quaternion library
% 
% AHRS = MadgwickAHRS('SamplePeriod', 0.15, 'Beta', 0.1);


count = 1;
ax = zeros(1000, 1);
ay = zeros(1000, 1);
az = zeros(1000, 1);
gx = zeros(1000, 1);
gy = zeros(1000, 1);
gz = zeros(1000, 1);
mx = zeros(1000, 1);
my = zeros(1000, 1);
mz = zeros(1000, 1);

A = [-0.5 -0.5 -0.5];
B = [0.5 -0.5 -0.5];
C = [-0.5 0.5 -0.5];
D = [-0.5 -0.5 0.5];
E = [-0.5 0.5 0.5];
F = [0.5 -0.5 0.5];
G = [0.5 0.5 -0.5];
H = [0.5 0.5 0.5];
P = [A;B;F;H;G;C;A;D;E;H;F;D;E;C;G;B];

while(1)
    tic
    
    figure(1)
    
    fwrite(xBee, char(0), 'char');
    while(xBee.BytesAvailable==0)
    end
    ax(count) = str2double(fscanf(xBee))/16384;
    ay(count) = str2double(fscanf(xBee))/16384;
    az(count) = str2double(fscanf(xBee))/16384;
    gx(count) = str2double(fscanf(xBee))*(250 / 32768);
    gy(count) = str2double(fscanf(xBee))*(250 / 32768);
    gz(count) = str2double(fscanf(xBee))*(250 / 32768);
    mx(count) = str2double(fscanf(xBee))*(1200 / 4096);
    my(count) = str2double(fscanf(xBee))*(1200 / 4096);
    mz(count) = str2double(fscanf(xBee))*(1200 / 4096);
    
%     AHRS.Update([gx(count) gy(count) gz(count)]*(pi/180),[ax(count) ay(count) az(count)], [mx(count) my(count) mz(count)]);	% gyroscope units must be radians
%     AHRS.Quaternion;
    
    hold on
    subplot(4,1,1)
    title('accel')
    plot(ax(1:count), 'color', [0 0 1])
    plot(ay(1:count), 'color', [0 1 0])
    plot(az(1:count), 'color', [1 0 0])
    xlim([0 count])
    
    hold on
    subplot(4,1,2)
    title('gyro')
    plot(gx(1:count), 'color', [0 0 1])
    plot(gy(1:count), 'color', [0 1 0])
    plot(gz(1:count), 'color', [1 0 0])
    xlim([0 count])
    
    hold on
    subplot(4,1,3)
    title('magn')
    plot(mx(1:count), 'color', [0 0 1])
    plot(my(1:count), 'color', [0 1 0])
    plot(mz(1:count), 'color', [1 0 0])
    xlim([0 count])
    
%     quaternion = AHRS.Quaternion;
%     euler = quatern2euler(quaternConj(quaternion));
%     
% %     hold off
%     subplot(2,1,1)
%     gui(P, euler(1), euler(2), euler(3));
%     
%     subplot(2,1,2)
%     heading = 180 * atan2(my(count), mx(count)) / pi;
%     if (heading < 0) 
%         heading = heading+360;
%     end
%     compass(cos(heading*pi/180), sin(heading*pi/180))
% %     
    count = count+1;
    if count >= 1000
        count = 1;
    end
    %xBee.BytesAvailable
    %while (toc < 0.2)
    %end
    pause(0.00000000001)
    toc
end


