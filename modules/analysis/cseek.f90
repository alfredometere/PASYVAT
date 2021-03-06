subroutine cseek(bxmin, bxmax, bymin, bymax, bzmin, bzmax, n, points)!, ncut)

    implicit none

    integer*4, intent(in)              :: n
    real*8, intent(in)                 :: bxmin, bymin, bzmin
    real*8, intent(in)                 :: bxmax, bymax, bzmax
    real*8, dimension(n,3), intent(in) :: points
    

    !integer*4, intent(out)             :: ncut

    integer*4 :: i

	!ncut = 0

    open (6, file = 'cropped.csv', access = 'sequential', status = 'replace', & 
         form = 'formatted')

    do i = 1, n
    
        if (points(i,1) .le. bxmax .and. points(i,1) .ge. bxmin .and. &
           &points(i,2) .le. bymax .and. points(i,2) .ge. bymin .and. &
           &points(i,3) .le. bxmax .and. points(i,3) .ge. bxmin) then

            !write(*,*) points(i,1),points(i,2),points(i,3)
            write(6,'(f15.4,a1,f15.4,a1,f15.4)') points(i,1),',', points(i,2),&
                                               &',', points(i,3)
		!ncut = ncut + 1
        end if
    end do


    close(6)

end subroutine cseek
