subroutine bondseek(n,positions,r0,r1,bn)

    implicit none

    integer*4, intent(in)       :: n
    real*8,    intent(in)       :: r0,r1
    real*8,    intent(in)       :: positions(n,3)

    integer*4 :: i,j,k
    integer*4, intent(out) :: bn

    real*8 :: xi,yi,zi,xj,yj,zj,dx,dy,dz,mdl

    bn = 0

    do i = 1, (n - 1)
        xi = positions(i,1)
        yi = positions(i,2)
        zi = positions(i,3)
        do j = 1, n
            if (i .ge. j) cycle
            xj = positions(j,1)
            yj = positions(j,2)
            zj = positions(j,3)

            dx = abs(xj - xi)
            dy = abs(yj - yi)
            dz = abs(zj - zi)

            mdl = sqrt(dx * dx + dy * dy + dz * dz)

            if (mdl .ge. r0 .and. mdl .le. r1) bn = bn + 1

        end do
    end do
    return
end subroutine bondseek

