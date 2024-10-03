function Ryy=Relation(data,n)
l=length(data);
data=[data; zeros(max(n),1)];
Ryy=zeros(1,length(n));
for i=1:length(n)
    for j=1:l
        Ryy(i)=Ryy(i)+data(j)*data(j+n(i));
    end
end
end