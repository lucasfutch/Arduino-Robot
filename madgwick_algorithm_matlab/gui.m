function y = gui(P, roll, pitch, yaw)
    
    dcm = angle2dcm(yaw, pitch, roll);
    Cube = P*dcm;
    plot3(Cube(:,1),Cube(:,2),Cube(:,3)) % rotated cube
    xlim([-2 3])
    ylim([-2 3])
    zlim([-2 3])
    grid on
    y=1;

end
