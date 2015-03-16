! RDIST, Python FORTRAN module (f2py compliant)
! Copyright Alfredo Metere, 2012-06-17. All Rights Reserved
!
! This code is published with an LGPL License.
! Further informations here ( PUT THE LGPL LICENSE INFO )
!
! For info: alfredo.metere@mmk.su.se
!           alfredo.metere@molworx.com
!
! Abstract:
! --------
!
! This routine calculates a radial distribution of a particle set and outputs
! it in a table [r; i], where r is the particle-particle distance and i is the
! number of particles at that distance from other particles.
! 
! ------------------------------------------------------------------------------
subroutine rdist(n, nbins, vp, rcut, rdf_y, rdf_x)


    implicit none
! n                      = Number of particles
! vp                     = Array storing particles positions
! rd_tbl	             = Radial Distribution Table
! d_mode	             = Number of decimals digits on the distances
! xj, yj, zj, xi, yi, zi = Variables storing particles coordinates for the loop
!                          generating the neighbor list
! dx, dy, dz, mdl        = Variables used for computing vector modulus
! m, i, j                = Neighbour list array size and counters
! rpn                    = Restricted table particle numbers

    integer*4, intent(in)                            :: n
    integer*4, intent(in)                            :: nbins !, d_mode
    real*8, intent(in), dimension(n,3)               :: vp
    real*8, intent(in)                               :: rcut
   
    real*8, parameter                                :: pi = 3.141592654

    real*8, dimension(nbins*nbins)                   :: rdf_y2
    real*8, dimension(nbins), intent(out)            :: rdf_y
    real*8, dimension(nbins), intent(out)            :: rdf_x

    real*8                                           :: cmax, cmin, ctemp
    real*8                                           :: cval, drr
    real*8                                           :: xj,yj,zj
    real*8                                           :: xi,yi,zi
    real*8                                           :: xmax,ymax,zmax
    real*8                                           :: xmin,ymin,zmin
    real*8                                           :: xbox, ybox, zbox
    real*8                                           :: xb2, yb2, zb2
    real*8                                           :: dx,dy,dz,dr,mdl, dn
    real*8                                           :: rho, mdlbox
    integer*4                                        :: i,j,k,kk, nn
    integer*4                                        :: m, i1, i2

    integer*2                                        :: m2(4)
    
    equivalence (mdl,m2(1)),(m2(3),m)
! Processes all the unique particle couples and calculates their distances
    k = 0

! Needed now
    
    !pi = 3.141592654
!    m = (n**2 - n)

!    print *, "Number of particles (N) = ", size(vp)/3
!    print *, "Number of unique pairs (M) = ", (n*n)
!    if(size(couples)/3 .eq. m) then
!        print *, "M size is correct"
!    else
!        print *, "Some error must be occurred"
!        print *, "M ", m
!        stop
!    end if

    print *,"Determining system boundaries"

    xmin   = 0.0
    ymin   = 0.0
    zmin   = 0.0
    xmax   = 0.0
    ymax   = 0.0
    zmax   = 0.0

    cval   = 0.0
    rdf_x  = 0.0
    rdf_y  = 0.0
    rdf_y2 = 0.0 
    cmin   = 0.0

    nn     = 0.0
    dn     = 2.0 / n

    

    do i=1, n
        if (vp(i,1) > xmax) xmax = vp(i,1)
        if (vp(i,2) > ymax) ymax = vp(i,2)
        if (vp(i,3) > zmax) zmax = vp(i,3)

        if (vp(i,1) < xmin) xmin = vp(i,1)
        if (vp(i,2) < ymin) ymin = vp(i,2)
        if (vp(i,3) < zmin) zmin = vp(i,3)
    end do
    print *,"Absolute boundaries of the system"
    write(6,'(a4,f10.6,a5,f10.6,a5,f10.6)') "X0: ",xmin," Y0: ",ymin," Z0: ",zmin
    write(6,'(a4,f10.6,a5,f10.6,a5,f10.6)') "X1: ",xmax," Y1: ",ymax," Z1: ",zmax

    xbox = xmax - xmin
    ybox = ymax - ymin
    zbox = zmax - zmin

    rho = n / (xbox*ybox*zbox)

    xb2 = xbox / 2.
    yb2 = ybox / 2.
    zb2 = zbox / 2.

    mdlbox = xb2 * xb2 + yb2 * yb2 + zb2 * zb2

    ctemp = rcut/float(nbins)
    !ctemp = sqrt(mdlbox)/float(nbins)
    write(6,'(a6,f15.8)'), "Step: ", ctemp

    do i=1,nbins
        rdf_x(i) = i * ctemp
        !rdf_x(i) = (n/rho)**(1./3.) * (i-0.5)
    end do

    print *,"Box size"
    print *,"RHO: ",rho
    write(6,'(a5,f10.6,a1,f10.6,a1,f10.6,a1)') "XYZ (",xbox,",",ybox,",",zbox,")"

    open (8, file = 'restricted_rd.csv', access = 'sequential', status = 'replace', form = 'formatted')

    print *,"Computing particle neighbours"
    do i = 1, (n - 1)
        xi = vp(i,1)
        yi = vp(i,2)
        zi = vp(i,3)

        do j = 1, n
            if (i .ge. j) cycle

            xj = vp(j,1)
            yj = vp(j,2)
            zj = vp(j,3)

            dx = abs(xj - xi)
            dy = abs(yj - yi)
            dz = abs(zj - zi)

	    !dx = xj - xi
            !dy = yj - yi
            !dz = zj - zi

	    ! these are added
	    !if (dx .gt. xb2) dx = xbox - dx
	    !if (dy .gt. yb2) dy = ybox - dy
	    !if (dz .gt. zb2) dz = zbox - dz

        !mdl = sqrt(dx*dx + dy*dy + dz*dz)
	    mdl = sqrt(dx*dx + dy*dy + dz*dz)
        if (mdl .lt. 1.) print *,mdl
        
	    !if (mdl .ge. mdlbox/2) mdl = mdl - mdlbox/2

            if (mdl .gt. rcut) then! (mdl .ge. rcut)
                cycle
	    


            !    rdf_y(m) = rdf_y(m) + (2./n)
            !end if		
            else
    !            m = int(mdl) + 1
            !print *,"m = int(mdl) + 1",m
                ! Slides the whole  RDF histogram
                do k = 1,nbins
                    cval = rdf_x(k) + ctemp
                    cmin = rdf_x(k) - ctemp
                    if (mdl >= cmin .and. mdl <= cval) then
			 ! nn Counts how many couples fall in the cutoff radius.
			 !    It is needed to normalize the histogram values
	!		 nn = nn + 1.0 
		                rdf_y(k) = rdf_y(k) + 1.0
                    end if
                end do

             end if
             !m = int(mdl) + 1
             !rdf_y2(m)=rdf_y2(m) + dn
        end do
    end do

!    do i = 1, nbins
!        rdf_y(i) = 0.
!        i1 = (i-1)**2 + 1
!        i2 = i**2
!        do j = i1, i2
!             rdf_y(i) = rdf_y(i) + rdf_y2(j)
!        end do
!    end do

    do k = 1,nbins
    cval = rdf_x(k) + ctemp
    cmin = rdf_x(k) - ctemp
	!cval = 1. *  k
	!cmin = 1. * (k-1)
	drr = cval*cval*cval - cmin*cmin*cmin
	dr = rho * 4.0 * pi * drr / 3.0
! Normalizes to a spherical shell the bin values to avoid recurrencies
!        rdf_y(k) = rdf_y(k) / (4.0 / 3.0 * pi * (cval**3 - cmin**3))
	rdf_y(k) = rdf_y(k) / dr
	!rdf_y(k) = (rdf_y(k) / nn) / (4.0 / 3.0 * pi * dr) * rho
	!rdf_y(k) = rdf_y(k) * rho
    end do

    write (*,*)
    print *,"Done"
 
! Writes a CSV file containing the RDF plot coordinates   
    open (7, file = 'full_rd.csv', access = 'sequential', status = 'replace', form = 'formatted')
    print *,"Exporting CSV file (full_rd.csv)"
    do k = 1, nbins
        write(7,'(f15.4,a1,f15.4)') rdf_x(k),',',rdf_y(k)
    end do
    print *,"Done"
    close(7)
    close(8)

end subroutine rdist

