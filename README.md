# PlasmaDissociation
            if(auto_clone=='YES') then
              brunit = 48759
  
              open(unit=brunit,file="Brforce-.out",status="unknown",access = 'append', iostat=ierr)
              do p=1,nclones
                allocate(ovrlp(size(bsetarr(p)%bs),size(bsetarr(p)%bs)))
                ovrlp=ovrlpmat(bsetarr(p)%bs)
                popdiff = 1
                if ((bsetarr(p)%bs(1)%orgpes==1)) then 
                  pophold1 = pop(bsetarr(p)%bs, 1, ovrlp)
                  pophold2 = pop(bsetarr(p)%bs, 2, ovrlp)
                  popdiff = (pophold1-pophold2)/(pophold1+pophold2)
                else if (bsetarr(p)%bs(1)%orgpes == 2) then
                  pophold1 = pop(bsetarr(p)%bs, 1, ovrlp)
                  pophold2 = pop(bsetarr(p)%bs, 2, ovrlp)
                  popdiff = (pophold2-pophold1)/(pophold1+pophold2)
                end if 
                if (popdiff.lt.1-(2*nbf_frac)) then 
                  if(nclones.lt.2**clonemax) then 
                    if (ccooldown(p).eq.0) then  
                      nclones = nclones+1 
                      write(6,*) 'number of clones is now ', nclones, 'at timestep', x, pophold1, pophold2
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
                deallocate(ovrlp) 
              end do   
              if (allocated(ccooldown)) then 
                do p = 1, size(ccooldown)
                  if (ccooldown(p).gt.0) then
                    ccooldown(p) = ccooldown(p) - 1 
                  end if 
                end do 
              end if 
              ! close(brunit)
            else if (auto_clone== 'NO') then
