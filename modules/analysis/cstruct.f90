subroutine cutstruct(xbox, ybox, zbox, n, points, ncut, cpoints)

	integer*4, intent(in)                  :: n, ncut
	real*8,    intent(in)                  :: xbox, ybox, zbox
	real*8, dimension(n,3), intent(in)     :: points

	real*8, dimension(ncut,3), intent(out) :: cpoints



end subroutine cutstruct
