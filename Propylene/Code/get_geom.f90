real r0(3)
character (len=1)  atom
character (len=50) f_inp

call getarg(1,f_inp)

open(1,file=f_inp)
open(2,file='geom.in')
read(1,*) natom, nst
read(1,*) 
read(1,*) 


! Read geometry
read(1,*) mc, mult
write(2,'(2i3)') mc, mult
do i=1,natom
  read(1,*) atom,r0
  write(2,'(a1,3f15.8)') atom,r0*0.529177
end do
end

