! dynamics.f90

subroutine preliminary_propagation(natom, nst, branch, time, TimeStep, nc, mult, atom, r0, p0, Es0, Fs0, Cs0)
  implicit none
  integer, intent(in) :: natom, nst, branch, nc, mult
  real (kind=8), intent(in) :: time, TimeStep
  character (len=1), intent(in) :: atom(natom)
  real (kind=8), intent(in) :: r0(natom*3), p0(natom*3), Es0(nst), Fs0(natom*3,nst), Cs0(natom*3,nst,nst)

  ! Your Fortran code for dynamics goes here, using the provided inputs
  ! ...
    ! Velocities and Ehrenfest force
    V0 = P0 / M
    F0 = CompForceEhr(A0, Fs0, Es0, Cs0, nst, ndim)
    E0 = sum(Es0 * (abs(A0)**2)) + sum(P0 * V0) / 2.

    ! Electronic Hamiltonian
    do n1 = 1, nst
    HE_0(n1, n1) = Es0(n1) + 77.67785291
    do n2 = n1+1, nst
        HE_0(n1, n2) = -ii * sum(V0 * Cs0(:, n1, n2))
        HE_0(n2, n1) = -HE_0(n1, n2)
    end do
    end do

    ! Begin propagation
    Ab = matmul(magnus2(-ii*HE_0, -ii*HE_0, TimeStep/20), A0)
    F0 = CompForceEhr(A0, Fs0, Es0, Cs0, nst, ndim) / 10.

    do im = 1, 9
    A1 = matmul(magnus2(-ii*HE_0, -ii*HE_0, TimeStep/10), Ab)
    Ab = A1
    F0 = F0 + CompForceEhr(Ab, Fs0, Es0, Cs0, nst, ndim) / 10.
    end do

    R1 = R0 + TimeStep * V0 + TimeStep**2/2.d0 * F0 / M
    P1 = P0 + TimeStep * F0
    V1 = P1 / M

    time = time + TimeStep

    !Write preliminary final point data
    open(2, file=trim(f_inp)//'.p')
    write(2, '(2i5)') natom, nst
    write(2, '(i10)') branch
    write(2, '(2f15.6)') time, TimeStep

    ! Write geometry and momenta
    write(2, '(2i3)') nc, mult
    do i = 1, natom
        write(2, '(a1,3f22.16)') atom(i), r1(i*3-2:i*3)
    end do
    write(2, *)
    do i = 1, natom
        write(2, '(3e25.16)') p1(i*3-2:i*3)
    end do

    ! Write amplitudes
    write(2, *)
    do i = 1, nst
        write(2, *) A1(i)
    end do
    write(2, *)
    close(2)

    ! End preliminary propagation

    deallocate (A0, A1, Es0, Fs0, Cs0, HE_0, F0, V0, V1, M)
    deallocate (r0, p0, r1, p1, atom)


end subroutine dynamics

Function CompForceEhr(A,F,E,C,nst,ndim) result(ForceVector)
      implicit none
      real (kind=8) :: ForceVector(ndim)
      real (kind=8) :: F(ndim,nst)
      real(kind=8)::C(ndim,nst,nst)
      real (kind=8) :: f1(ndim),f2(ndim)
      real (kind=8) :: E(nst),ae
      complex(8)    :: a(nst)
      integer  :: ndim,nst,i,j
      F1=0.d0
      F2=0.d0
      do i=1,nst
        F1=F1+F(:,i)*cdabs(A(i))**2
      end do
      do i=1,nst
        do j=i+1,nst
          ae=2.d0*dreal(dconjg(A(i))*A(j))*(E(i)-E(j))
          F2=F2+ae*C(:,i,j)
        end do
      end do
      ForceVector=F1+F2
      return
end function CompForceEhr


function magnus2( H0, H1, dt ) result( magH )
! - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
! -
complex*16,intent(in) :: H0(:,:), H1(:,:)
real*8 :: dt
complex*16,dimension(size(H0,1),size(H0,2)) :: magH

complex*16,dimension(size(H0,1),size(H0,2)) :: a0, a1, a2, W1, Htr    !derivatives at t/2
complex*16 :: Hav
integer :: ndim, i

ndim = size(H0,1)

! Calculate the average
Hav = 0.d0
do i = 1, ndim
   Hav = Hav + H0(i,i) + H1(i,i)
enddo
Hav = Hav / dble( 2*ndim )

! THe trace matrix
Htr = 0.d0
do i = 1, ndim
   Htr(i,i) = Hav
enddo

a0 =        (H1+H0)/2.d0 - Htr

W1 = dt * a0

!magH = matrix_exponential( W1 )*exp(Hav*dt)
 magH = exp_pade( W1)*exp(Hav*dt)

return
end function magnus2

function exp_pade( A, t_in ) result ( expA )
! - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
! -

complex*16,intent(in) :: A(:,:)
real*8,    optional   :: t_in
complex*16            :: expA(size(A,1),size(A,2))

integer :: n

integer :: ideg, m , ipiv(size(A,1)), &
           iexph, & ! locates the start of expA inthe work array wsp
           lwsp, ldh, ns, iflag
complex*16 :: wsp( 4*size(A,1)**2 + 10 +1 )
real*8 ::  t

t = 1.d0
if( present(t_in) ) t = t_in

ideg = 6
m    = size(A,1)
ldh  = m
lwsp = size(wsp)

if( maxval(abs(A)) < 1.d-7 )then
   expA = 0.
   do n = 1, m
      expA(n,n) = (1.d0,0.d0)
   enddo
else
   call ZGPADM( ideg, m, t, A, ldh, wsp, lwsp, ipiv, iexph, ns, iflag )
   expA = reshape( wsp(iexph:iexph+m**2-1), (/m,m/) )
endif


return
end function exp_pade