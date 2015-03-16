subroutine bond_id(n,positions,r0,r1,bn,b0,b1)

    implicit none

    integer*4, intent(in)                    :: n,bn
    real*8,    intent(in)                    :: r0,r1
    real*8,    intent(in)                    :: positions(n,3)

    integer*4,dimension(bn), intent(out)     :: b0,b1

    integer*4 :: i,j,bnt


    real*8 :: xi,yi,zi,xj,yj,zj,dx,dy,dz,mdl    

    bnt = 1

    print *,"Bond_id called with particles:",n

    do i = 1, (n - 1)
        xi = positions(i,1)
        yi = positions(i,2)
        zi = positions(i,3)

        do j = 1, n
            if (i .ge. j) cycle
            xj = positions(j,1)
            yj = positions(j,2)
            zj = positions(j,3)

            dx = abs(xj-xi)
            dy = abs(yj-yi)
            dz = abs(zj-zi)

            mdl = sqrt(dx*dx + dy*dy + dz*dz)

            if (mdl .ge. r0 .and. mdl .le. r1) then
                b0(bnt) = i - 1
                b1(bnt) = j - 1
                bnt = bnt + 1
            else
                cycle
            end if
        end do
    end do

!    do i = 1,n
!        if (couples(i,1) .le. r1 .and. couples(i,1) .ge. r0) then
!            b0(bnt) = int(couples(i,2))
!            b1(bnt) = int(couples(i,3))
!            bnt = bnt + 1
!        end if
!    end do

    
    print *,"Bond indexer: "
    print *,"Min: ",r0
    print *,"Max: ",r1
    print *,"Couples in this interval: ", bn
    print *,"Total couples: ",n*(n-1)/2
    print *,"--------------------------------"
    print *

    return
end subroutine bond_id
