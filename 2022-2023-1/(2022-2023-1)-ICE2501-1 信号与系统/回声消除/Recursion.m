function func=Recursion(s,t1,t2,data,x1,x2)
if t1>t2
    tmp=t1;
    t1=t2;
    t2=tmp;
end
if s<=0
    func=0;
elseif s<=t1
    func=data(s);
else
    func=data(s)-x1*Recursion(s-t1,t1,t2,data,x1,x2)-x2*Recursion(s-t2,t1,t2,data,x1,x2);
end