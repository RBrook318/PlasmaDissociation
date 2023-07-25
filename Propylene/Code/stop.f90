open(1,file='t.0')
read(1,*)
read(1,*)
read(1,*) t
close(1)
if (t.ge.25000.) then
open(1,file='stop')
write(1,*) 'stop'
close(1)
end if
end
