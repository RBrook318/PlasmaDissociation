# Initiation
 ncpu=$1 



 ../Code/get_geom.x t.0

 echo '$molecule' > f.inp
 cat geom.in >> f.inp
 echo '$end' >> f.inp
 cat sf_diis >> f.inp
    echo 'CIS_N_ROOTS' 1 >>f.inp
    echo 'CIS_STATE_DERIV' 1 >>f.inp
    echo '$end' >>f.inp

    qchem -save -nt $ncpu f.inp f.out wf

    if ! grep -q "Calculating analytic gradient of the CIS energy" f.out; then
     echo '$molecule' >f.inp
     cat geom.in >>f.inp
     echo '$end' >>f.inp
     cat sf_gmd >>f.inp
     echo 'CIS_N_ROOTS' 1 >>f.inp
     echo 'CIS_STATE_DERIV' 1 >>f.inp
     echo '$end' >>f.inp

     qchem -save -nt $ncpu f.inp f.out wf
    fi
if ! grep -q "Calculating analytic gradient of the CIS energy" f.out; then
cat error >ERROR
pwd >>../ERROR
exit 1
fi
cat  f.out >>  f.all
../Code/q_to_prop.x >>t.0

mv t.0 t.1
 cat t.1 > t1.all
 echo '---------------------------------------------------' >>t1.all



#Propagation
for i in {1..2500};do

 mv t.1 t.0

../Code/stop.x

if [ -f stop ]; then
  break
fi




 ../Code/prop_prelim.x t

 ../Code/get_geom.x t.p

 echo '$molecule' > f.inp
 cat geom.in >> f.inp
 echo '$end' >> f.inp
 cat sf_diis >> f.inp
    if [ -d wf ]; then
      echo 'SCF_GUESS           Read' >>f.inp
    fi
    echo 'CIS_N_ROOTS' 1 >>f.inp
    echo 'CIS_STATE_DERIV' 1 >>f.inp
    echo '$end' >>f.inp

     qchem -save -nt $ncpu f.inp f.out wf 

    if ! grep -q "Calculating analytic gradient of the CIS energy" f.out; then
     echo '$molecule' >f.inp
     cat geom.in >>f.inp
     echo '$end' >>f.inp
     cat sf_gmd >>f.inp
     if [ -d wf ]; then
       echo 'SCF_GUESS           Read' >>f.inp
     fi
     echo 'CIS_N_ROOTS' 1 >>f.inp
     echo 'CIS_STATE_DERIV' 1 >>f.inp
     echo '$end' >>f.inp

      qchem -save -nt $ncpu f.inp f.out wf
    fi
if ! grep -q "Calculating analytic gradient of the CIS energy" f.out; then
cat error >ERROR
pwd >>../ERROR
exit 1
fi



    cat  f.out >>  f.all



 ../Code/q_to_prop.x >>t.p
 ../Code/prop_corr.x t
 cat t.1 >> t1.all
 echo '---------------------------------------------------' >>t1.all
 cat t.te>>te.all

if [ "$(head -1 t.1)" != "$(head -1 t.p)" ]; then
  rm -r wf
  echo $i>>t.diss1
fi




done




