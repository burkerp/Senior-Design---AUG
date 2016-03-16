function vrms=rms1(x)
%function to return rms voltage of an array x
x2=x.^2;
power=mean(x2);
vrms=sqrt(power);
