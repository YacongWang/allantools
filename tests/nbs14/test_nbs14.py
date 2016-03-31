"""
  NBS14 test for allantools (https://github.com/aewallin/allantools)

  nbs14 datasets are from http://www.ieee-uffc.org/frequency-control/learning-riley.asp
  
  Stable32 was used to calculate the deviations we compare against.

  The small dataset and deviations are from
  http://www.ieee-uffc.org/frequency-control/learning-riley.asp
  http://www.wriley.com/paper1ht.htm
  
  see also:
  NIST Special Publication 1065
  Handbook of Frequency Stability Analysis
  http://tf.nist.gov/general/pdf/2220.pdf
  around page 107
"""
import math
import time
import sys

import allantools as allan

# 10-point dataset and deviations
nbs14_phase = [ 0.00000, 103.11111, 123.22222, 157.33333, 166.44444, 48.55555,-96.33333,-2.22222, 111.88889, 0.00000 ]
nbs14_f     = [892,809,823,798,671,644,883,903,677]
nbs14_devs= [ (91.22945,115.8082),  # 0, ADEV(tau=1,tau=2)
              (91.22945, 85.95287), # 1, OADEV 
              (91.22945,74.78849),  # 2, MDEV
              #(91.22945,98.31100),  # TOTDEV, http://www.ieee-uffc.org/frequency-control/learning-riley.asp
              (91.22945, 93.90379), # 3, TOTDEV, http://tf.nist.gov/general/pdf/2220.pdf page 107
              (70.80608,116.7980),  # 4, HDEV
              (52.67135,86.35831),  # 5, TDEV 
              (70.80607, 85.61487), # 6, OHDEV
              #(75.50203, 75.83606),  # 7, MTOTDEV (published table, WFM bias correction)
              (6.4509e+01, 6.4794e+01), # MTOTDEV Stable32 v1.60, no bias-correction
              #(43.59112, 87.56794 ), # 8, TTOTDEV (published table, WFM bias correction)
              (3.7244e+01, 7.4818e+01), # TTOTDEV Stable32 v1.60, no bias-correction
              (70.80607, 91.16396 ), # 9 HTOTDEV (published table)
              (45.704, 81.470)] # 10 HTOTDEV Stable32
              # (100.9770, 102.6039)  # Standard Deviation (sample, not population)
              
              

              
# 1000 point deviations from:
# http://www.ieee-uffc.org/frequency-control/learning-riley.asp    Table III
# http://www.wriley.com/paper1ht.htm
# http://tf.nist.gov/general/pdf/2220.pdf  page 108
nbs14_1000_devs = [ [2.922319e-01, 9.965736e-02, 3.897804e-02],  # 0 ADEV 1, 10, 100 
                    [2.922319e-01, 9.159953e-02, 3.241343e-02],  # 1 OADEV
                    [2.922319e-01, 6.172376e-02, 2.170921e-02],  # 2 MDEV 
                    #[2.922319e-01, 9.172131e-02, 3.501795e-02],  # TOTDEV, http://www.ieee-uffc.org/frequency-control/learning-riley.asp
                    # "Calculated using bias-corrected reflected method from endpoint-matched phase data"
                    
                    [2.922319e-01, 9.134743e-02, 3.406530e-02],    # 3 TOTDEV, http://tf.nist.gov/general/pdf/2220.pdf page 108
                    # "Calculated using doubly reflected TOTVAR method"
                    
                    [2.943883e-01, 1.052754e-01, 3.910860e-02],   # 4 HDEV
                    [1.687202e-01, 3.563623e-01, 1.253382e-00],   # 5 TDEV
                    [2.943883e-01, 9.581083e-02, 3.237638e-02],   # 6 OHDEV
                    [2.884664e-01, 9.296352e-02, 3.206656e-02],   # 7 standard deviation,  sample (not population)
                    [2.943883e-01, 9.614787e-02, 3.058103e-02],   # 8 HTOTDEV
                    #[2.418528e-01, 6.499161e-02, 2.287774e-02],   # 9 MTOTDEV (from published table, WITH bias correction)
                    [2.0664e-01, 5.5529e-02, 1.9547e-02], # MTOTDEV (from Stable32 v1.60 decade run, NO bias correction)
                    #[1.396338e-01, 3.752293e-01, 1.320847e-00],    # 10 TTOTDEV (from published table, WITH bias correction)
                     [1.1930e-01, 3.2060e-01, 1.1285e+00 ] ] # TTOTDEV (from Stable 32 v1.60 decade run, NO bias correction)  
                    
# this generates the nbs14 1000 point frequency dataset. 
# random number generator described in 
# http://www.ieee-uffc.org/frequency-control/learning-riley.asp
# http://tf.nist.gov/general/pdf/2220.pdf   page 107
# http://www.wriley.com/tst_suit.dat
def nbs14_1000():
    n = [0]*1000
    n[0] = 1234567890
    for i in range(999):
        n[i+1] = (16807*n[i]) % 2147483647
    # the first three numbers are given in the paper, so check them:
    assert( n[1] ==  395529916 and n[2] == 1209410747 and  n[3] == 633705974 )
    n = [x/float(2147483647) for x in n] # normalize so that n is in [0, 1]
    return n

def nbs14_tester( function, pdata, fdata, correct_devs, soft=False ):
    rate=1.0
    taus =[1, 10, 100]
    (taus2, devs, deverrs, ns) = function( phase=pdata, frequency=fdata, rate=rate, taus=taus)
    for i in range(3):
        if soft:
            print(' calculated ', devs[i] )
            print('      table ', correct_devs[i])
        else:
            assert( check_devs( devs[i], correct_devs[i] ) )

def test_nbs14_1000():
    fdata = nbs14_1000()
    print("nbs14 1000-point frequency data tests:")
    
    nbs14_tester( allan.adev, None,fdata, nbs14_1000_devs[0] )
    print("nbs14_1000 adev OK")

    nbs14_tester( allan.oadev, None,fdata, nbs14_1000_devs[1] )
    print("nbs14_1000 oadev OK")

    nbs14_tester( allan.mdev, None,fdata, nbs14_1000_devs[2] )
    print("nbs14_1000 mdev OK")

    nbs14_tester( allan.totdev, None,fdata, nbs14_1000_devs[3] )
    print("nbs14_1000 totdev OK")
    
    nbs14_tester( allan.hdev, None,fdata, nbs14_1000_devs[4] )
    print("nbs14_1000 hdev OK")

    nbs14_tester( allan.tdev, None,fdata, nbs14_1000_devs[5] )
    print("nbs14_1000 tdev OK")

    nbs14_tester( allan.ohdev, None,fdata, nbs14_1000_devs[6] )
    print("nbs14_1000 ohdev OK")

    print("nbs14_1000 mtotdev test. slow..")
    nbs14_tester( allan.mtotdev, None,fdata, nbs14_1000_devs[9], soft=False )
    print("nbs14_1000 mtotdev OK")
    
    print("nbs14_1000 ttotdev test. slow...")
    nbs14_tester( allan.ttotdev, None,fdata, nbs14_1000_devs[10], soft=False )
    print("nbs14_1000 ttotdev OK")
    


    #########################################################
    # now we test the same data, calling the _phase functions
    pdata = allan.frequency2phase(fdata, 1.0)
    print("nbs14 1000-point phase data tests:")
    
    nbs14_tester( allan.adev, pdata, None,nbs14_1000_devs[0] )
    print("nbs14_1000 adev_phase OK")

    nbs14_tester( allan.oadev, pdata, None,nbs14_1000_devs[1] )
    print("nbs14_1000 oadev_phase OK")

    nbs14_tester( allan.mdev, pdata, None,nbs14_1000_devs[2] )
    print("nbs14_1000 mdev_phase OK")

    nbs14_tester( allan.totdev, pdata, None,nbs14_1000_devs[3] )
    print("nbs14_1000 totdev_phase OK")
    
    nbs14_tester( allan.hdev, pdata, None,nbs14_1000_devs[4] )
    print("nbs14_1000 hdev_phase OK")

    nbs14_tester( allan.tdev, pdata, None,nbs14_1000_devs[5] )
    print("nbs14_1000 tdev_phase OK")

    nbs14_tester( allan.ohdev, pdata, None,nbs14_1000_devs[6] )
    print("nbs14_1000 ohdev_phase OK")
        
    print("nbs14_1000 all tests OK")

def check_devs(dev2, dev1, soft=False):
    rel_error = (dev2-dev1)/dev1
    tol = 1e-4
    verbose = 1

    if ( abs(rel_error) < tol ):
        if verbose:
            print(" OK   %0.6f \t    %0.6f \t %0.6f" % (dev1,dev2, rel_error))
        return True
    else:
        print(" ERROR   %0.6f \t %0.6f \t %0.6f" % (dev1,dev2, rel_error))
        print("  bias corr %.4f" % pow(dev2/dev1,2))
        if soft:
            return True
        return False

def test_nbs14_10():
    taus = [1, 2]
    devs = []
    tol = 1e-4
    f_fract = [ float(f) for f in nbs14_f]
    
    # first tests that call the _phase functions
    print("nbs14 10-point tests:")
    
    print("ADEV")
    (taus1,adevs1,aerrs1,ns1) = allan.adev( phase= nbs14_phase, rate=1.0, taus=taus)
    (taus2,adevs2,aerrs2,ns2) = allan.adev( frequency=f_fract, rate=1.0, taus=taus)
    adevs = nbs14_devs[0]
    assert( check_devs( adevs1[0], adevs[0] ) )
    assert( check_devs( adevs1[1], adevs[1] ) )
    assert( check_devs( adevs2[0], adevs[0] ) )
    assert( check_devs( adevs2[1], adevs[1] ) )
    print("nbs14 adev OK\n")
    
    print("OADEV")
    (taus1,adevs1,aerrs1,ns1) = allan.oadev( phase = nbs14_phase, rate=1.0, taus=taus)
    (taus2,adevs2,aerrs2,ns2) = allan.oadev( frequency=f_fract, rate=1.0, taus=taus)
    oadevs = nbs14_devs[1]
    assert( check_devs( adevs1[0], oadevs[0] ) )
    assert( check_devs( adevs1[1], oadevs[1] ) )
    assert( check_devs( adevs2[0], oadevs[0] ) )
    assert( check_devs( adevs2[1], oadevs[1] ) )
    print("nbs14 oadev OK\n")
    
    print("MDEV")
    (taus2,adevs2,aerrs2,ns2) = allan.mdev( phase=nbs14_phase, rate=1.0, taus=taus)
    mdevs = nbs14_devs[2]
    assert( check_devs( adevs2[0], mdevs[0] ) )
    assert( check_devs( adevs2[1], mdevs[1] ) )
    print("nbs14 mdev OK\n")
    
    print("TOTDEV")
    (taus2,adevs2,aerrs2,ns2) = allan.totdev( phase=nbs14_phase, rate=1.0,taus= taus)
    totdevs = nbs14_devs[3]
    assert( check_devs( adevs2[0], totdevs[0] ) )
    assert( check_devs( adevs2[1], totdevs[1] ) )
    print("nbs14 totdev OK\n")
    
    print("HDEV")
    (taus2,adevs2,aerrs2,ns2) = allan.hdev( phase =nbs14_phase, rate=1.0, taus=taus)
    hdevs = nbs14_devs[4]
    assert( check_devs( adevs2[0], hdevs[0] ) )
    assert( check_devs( adevs2[1], hdevs[1] ) )
    print("nbs14 hdev OK\n")
    
    print("TDEV")
    (taus2,adevs2,aerrs2,ns2) = allan.tdev( phase=nbs14_phase, rate=1.0, taus=taus)
    tdevs = nbs14_devs[5]
    assert( check_devs( adevs2[0], tdevs[0] ) )
    assert( check_devs( adevs2[1], tdevs[1] ) )
    print("nbs14 tdev OK\n")
    
    print("OHDEV")
    (taus2,adevs2,aerrs2,ns2) = allan.ohdev( phase =nbs14_phase, rate=1.0, taus=taus)
    ohdevs = nbs14_devs[6]
    assert( check_devs( adevs2[0], ohdevs[0] ) )
    assert( check_devs( adevs2[1], ohdevs[1] ) )
    print("nbs14 ohdev OK\n")

    print("MTOTDEV")
    (taus2,adevs2,aerrs2,ns2) = allan.mtotdev( phase =nbs14_phase, rate=1.0, taus=taus)
    mtotdevs = nbs14_devs[7]
    assert( check_devs( adevs2[0], mtotdevs[0] ) )
    assert( check_devs( adevs2[1], mtotdevs[1] ) )
    print("nbs14 mtotdev OK\n")
    
    print("TTOTDEV")
    (taus2,adevs2,aerrs2,ns2) = allan.ttotdev( phase =nbs14_phase, rate=1.0, taus=taus)
    ttotdevs = nbs14_devs[8]
    assert( check_devs( adevs2[0], ttotdevs[0] ) )
    assert( check_devs( adevs2[1], ttotdevs[1] ) )
    print("nbs14 ttotdev OK\n")
    
    print("HTOTDEV")
    (taus2,adevs2,aerrs2,ns2) = allan.htotdev( phase =nbs14_phase, rate=1.0, taus=taus)
    htotdevs = nbs14_devs[9]
    htotdevs2 = nbs14_devs[10]
    assert( check_devs( adevs2[0], htotdevs[0] , soft=True) )
    assert( check_devs( adevs2[1]/math.sqrt(0.995), htotdevs[1] , soft=True) ) # MANUAL bias correction!!
    #assert( check_devs( adevs2[0], htotdevs2[0] , soft=True) ) # test against Stable32 value
    #assert( check_devs( adevs2[1], htotdevs2[1] , soft=True) ) # test against Stable32 value
    print("nbs14 htotdev OK\n")
    
    # then the same tests for frequency data
    print("nbs14 10-point tests for frequency data:")

    (taus2,adevs2,aerrs2,ns2) = allan.mdev( frequency=f_fract, rate=1.0, taus=taus)
    mdevs = nbs14_devs[2]
    assert( check_devs( adevs2[0], mdevs[0] ) )
    assert( check_devs( adevs2[1], mdevs[1] ) )
    print("nbs14 freqdata mdev OK")

    (taus2,adevs2,aerrs2,ns2) = allan.totdev( frequency=f_fract, rate=1.0, taus=taus)
    totdevs = nbs14_devs[3]
    assert( check_devs( adevs2[0], totdevs[0] ) )
    assert( check_devs( adevs2[1], totdevs[1] ) )
    print("nbs14 freqdata totdev OK")
    
    (taus2,adevs2,aerrs2,ns2) = allan.hdev( frequency=f_fract, rate=1.0, taus=taus)
    hdevs = nbs14_devs[4]
    assert( check_devs( adevs2[0], hdevs[0] ) )
    assert( check_devs( adevs2[1], hdevs[1] ) )
    print("nbs14 freqdata hdev OK")

    (taus2,adevs2,aerrs2,ns2) = allan.tdev( frequency=f_fract, rate=1.0, taus=taus)
    tdevs = nbs14_devs[5]
    assert( check_devs( adevs2[0], tdevs[0] ) )
    assert( check_devs( adevs2[1], tdevs[1] ) )
    print("nbs14 freqdata tdev OK")

    (taus2,adevs2,aerrs2,ns2) = allan.ohdev( frequency=f_fract, rate=1.0, taus=taus)
    ohdevs = nbs14_devs[6]
    assert( check_devs( adevs2[0], ohdevs[0] ) )
    assert( check_devs( adevs2[1], ohdevs[1] ) )
    print("nbs14 freqdata ohdev OK")

    (taus2,adevs2,aerrs2,ns2) = allan.mtotdev( frequency=f_fract, rate=1.0, taus=taus )
    mtotdevs = nbs14_devs[7]
    assert( check_devs( adevs2[0], mtotdevs[0] ) )
    assert( check_devs( adevs2[1], mtotdevs[1] ) )
    print("nbs14 freqdata mtotdev OK")
    
    (taus2,adevs2,aerrs2,ns2) = allan.ttotdev( frequency=f_fract, rate=1.0, taus=taus )
    ttotdevs = nbs14_devs[8]
    assert( check_devs( adevs2[0], ttotdevs[0] ) )
    assert( check_devs( adevs2[1], ttotdevs[1] ) )
    print("nbs14 freqdata ttotdev OK")
    
    print("nbs14 all test OK")

if __name__ == "__main__":
    test_nbs14_10()
    test_nbs14_1000()