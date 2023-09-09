# PlasmaDissociation

else if(auto_clone=='BF') then
                allocate(clonehere(nclones))
                clonehere = 0
                brunit = 48759
    
                open(unit=brunit,file="Brforce-.out",status="unknown",access = 'append', iostat=ierr)
    
                do p=1,nclones
                  do j=1,nbf
                    normar = 0.0d0
                    do r=1,npes
                      normar = normar + dconjg(bsetarr(p)%bs(j)%a_pes(r))*bsetarr(p)%bs(j)%a_pes(r)
                    end do
                    !!!! The line below needs changing to acount for multiple PESs
                    brforce = ((abs(bsetarr(p)%bs(j)%a_pes(1)*bsetarr(p)%bs(j)%a_pes(2))**2.0)/(normar**2.0))
                    if ((brforce.gt.thresh)) then
                      ! write(brunit,*) 'cloneblock hit for repeat', reps, 'clone', p, 'timestep', x, brforce
                      clonehere(p) = clonehere(p) + 1
                    end if 
                  end do 
                end do 
                do p=1,nclones
                  if (clonehere(p).ge.nbf*nbf_frac) then
                
                    if (ccooldown(p).eq.0) then
  
                      if (x.lt.(tnum-52)) then    
                        if(nclones.lt.2**clonemax) then 
                          ! write(6,*) 'the number of straddled functions is, ', clonehere(p), 'so clone'
                          nclones = nclones+1 
                          write(brunit,*) 'clone', p, 'from rep', reps, ' into clones ', p, nclones, 'at step', x, x*dtinit
                          !$omp critical
                          call v1cloning(bsetarr(p)%bs,nbf,bsetarr(p)%bs,bsetarr(nclones)%bs)
                          !$omp end critical 
                          clonememflg=1
                          allocate(ccooldownhold(nclones))
                          do j=1, size(ccooldown)
                            ccooldownhold(j) = ccooldown(j)
                          end do 
                          deallocate(ccooldown)
                          ccooldownhold(p) = clonefreq
                          ccooldownhold(nclones) = clonefreq
                          allocate(ccooldown(nclones)) 
                          do j=1,nclones
                            ccooldown(j) = ccooldownhold(j)
                          end do 
                          deallocate(ccooldownhold)
                        end if 
                      end if  
                    end if 
                  end if 
                  if (ccooldown(p).gt.0) then
                    ccooldown(p) = ccooldown(p) - 1
                  end if 
                
                end do 
                ! close(brunit)
                deallocate(clonehere) 
