subroutine bsel(n, vp, rcut, dimcouples)

    implicit none
    integer*4, intent(in)                  :: n
    real*8,    intent(in)                  :: rcut
    real*8,    intent(in) , dimension(n,3) :: vp
    integer*8, intent(out)                 :: dimcouples

    integer*4                              :: i,j
    real*8                                 :: xi,yi,zi,xj,yj,zj,dx,dy,dz,mdl
    real*8                                 :: rcutsq

    rcutsq = rcut*rcut


    do i = 1, (n - 1)
        xi = vp(i,1)
        yi = vp(i,2)
        zi = vp(i,3)

        do j = 1, n
            if (i >= j) cycle

            xj = vp(j,1)
            yj = vp(j,2)
            zj = vp(j,3)

            dx = abs(xj - xi)
            dy = abs(yj - yi)
            dz = abs(zj - zi)

            mdl = dx*dx + dy*dy + dz*dz
            !mdl = int(mdl * 10.0**3) / 10.0**3

            if (mdl > rcutsq) then
                cycle
            else
                dimcouples = dimcouples + 1        
            end if
        end do
    end do

    print *,"Bonds detected in the specified cutoff:",dimcouples

    return
end subroutine bsel
