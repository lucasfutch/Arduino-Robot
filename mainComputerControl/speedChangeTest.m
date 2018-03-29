for i = 100:-2.5:4
    fwrite(xBee, char(round(i)), 'char')
    disp(i)
    pause(0.1)
end
