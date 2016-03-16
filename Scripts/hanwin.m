function y = hanwin(x,npts)
% function y = hanwin(x,npts)
% function to apply a npts-length rise and a
% npts-length decay to the vector x, putting
% the result in y.

hann=hanning(2*npts);
han1=hann(1:npts);		% rise portion
han2=hann(npts+1:2*npts);	% decay portion

len = length(x);
k1=len-npts+1;

y = x;
y(1:npts)=y(1:npts).*han1;	%apply rise time
y(k1:len)=y(k1:len).*han2;	%apply decay
