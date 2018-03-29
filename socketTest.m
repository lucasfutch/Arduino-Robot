t = tcpip('0.0.0.0', 5560, 'NetworkRole', 'client');
fopen(t);

data_set_size = 1000;

data = zeros(data_set_size, 2);
count = 1;
tic
while(1)
    if (t.BytesAvailable)
        
        if (count > data_set_size)
            count = 1;
        end
        data(count,2) = fread(t, 1);
        data(count,1) = toc;
        count = count +1;
    
    end
    
    plot(data(1:count-1,1), data(1:count-1,2));
    pause(0.00000001);
end
