subroutine rdist(n, nbins, vp, rcut, rdf_y, rdf_x)
    implicit none

    integer*4,              intent(in) :: n
    integer*4,              intent(in) :: nbins
    real*8, dimension(n,3), intent(in) :: vp
    real*8                            :: rcut

    real*8, dimension(nbins), intent(out)   :: rdf_x, rdf_y
    real*8, dimension(:), allocatable       :: gr2

    real*8 :: x(n), y(n), z(n), xbox, ybox, zbox, mdl
    real*8 :: xmin, ymin, zmin, xmax, ymax, zmax
    real*8 :: xb2, yb2, zb2, xb22, yb22, zb22
    real*8 :: dva, a, rm, rm2, xl, dx, dy, dz, r2, dn, cf, xi, yi, zi
    real*8 :: ro, xlr, dxlr, dr, pi, rr1, rr2


    integer*4 :: m, n1, i, j, i1, i2, gr2size
     
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
    
    xb2 = xbox/2.
    yb2 = ybox/2.
    zb2 = zbox/2.
    
    xb22 = xb2 * xb2
    yb22 = yb2 * yb2
    zb22 = zb2 * zb2
       
    mdl = ((xb22 + yb22 + zb22)**(1./3.))**2

    gr2size = int(mdl)

    print *,"GR2 size: ", gr2size

    allocate(gr2(gr2size))
    
    ! size of gr2 is half box size square

    xl=600.
    ro=0.3
    xlr=(dble(n)/ro)**(1./3.)
    dxlr=xlr/600.
    cf=xl/xlr
    dva=2.
    rm=xl/2.
    rm2=rm*rm
    dn=2./dble(n)
    a=2.**52-0.5
    
    if (rcut .gt. rm) rcut = rm

    print *, "Particles accepted: ",n
    print *, "Bins for rdf_y: ",nbins
    print *, "Bins for gr2: ", nbins*nbins
    print *, "RCUT set to: "


    print *, "Acquiring coordinates"
    do i = 1, n
        x(i) = vp(i,1)
        y(i) = vp(i,2)
        z(i) = vp(i,3)
    end do
    print *, "Done"

    print *, "Multiplying coords"
    do i = 1, n
        x(i) = x(i) * cf
        y(i) = y(i) * cf
        z(i) = z(i) * cf
    end do
    print *, "Done"

    print *,"Zeroing the gr2"
    do i = 1,nbins*nbins
        gr2(i) = 0.
    end do
    print *,"Done"

    n1 = n - 1

    m = 0
    print *,"Filling histogram gr2"
    do i = 1, n1
        i1 = i + 1
        xi = x(i)
        yi = y(i)
        zi = z(i)
        
        do j = i1, n
            dx = abs(x(j) - xi)
            dy = abs(y(j) - yi)
            dz = abs(z(j) - zi)

            if(dx.gt.rm) dx = xl - dx
            if(dy.gt.rm) dy = xl - dy
            if(dz.gt.rm) dz = xl - dz

            r2 = dx*dx + dy*dy + dz*dz

            if(r2.lt.1.) then
                write(*,*) r2
                stop
            end if

            if(r2.gt.rm2) then 
                cycle
            else
                !print *,i,j,m,gr2(m),dn
                m = idint(r2) + 1
                gr2(m) = gr2(m) + dn
                
            end if
         end do
     end do
    print *,"Done"


    print *,"Filling rdf_y"
    do i = 1, nbins
        rdf_y(i) = 0.
        i1 = (i - 1)**2 + 1
        i2 = i**2
        do j = i1, i2
            rdf_y(i) = rdf_y(i) + gr2(j)
         end do
    end do
    print *, "Done"

    ro = dble(n) / xl**3.
    pi = 3.141592654
    dr = 1.

    print *,"Normalizing histogram rdf_y"
    do i = 1, nbins
        rr1 = dr * (i - 1)
        rr2 = dr * i
        dn  = ro * 4. * pi * (rr2**3. - rr1**3.) / 3.
        rdf_y(i) = rdf_y(i) / dn
    end do
    print *,"Done"   

      print *, "Printing RDF to screen"
      do i=1,nbins
        rdf_x(i)=dxlr*(i-0.5)
        !print *, i     
        !write(*,22) rdf_x(i), rdf_y(i)
      end do
      print *, "Done"
! 22   format(f10.5,f14.6)

    deallocate(gr2)

end subroutine rdist
