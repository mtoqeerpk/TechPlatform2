import numpy as np
from obspy.core.utcdatetime import UTCDateTime
from miniseedReadWriteSlice import *


stime = np.loadtxt('starttime.txt', dtype=str)
etime = np.loadtxt('endtime.txt', dtype=str)

print(stime)
print(etime)


st = fileMerge()

# Filter the data using the 4th order butterworth filter
# with the passband 0.05Hz - 45Hz
st.filter('bandpass', freqmin=0.05, freqmax=45, corners=4, zerophase=False)

st.plot()

## Export sliced miniseed files
for jj in xrange(stime.size):
    t0 = UTCDateTime(stime[jj])
    t1 = UTCDateTime(etime[jj])
    #st0 = sliceTrace(st, t0, t1)
    st0 = st.slice(t0, t1)
    st0.plot(outfile="TEST%i" % jj + ".pdf")
    for tr in st0:
        tr.stats.location = 'TEST%i' % jj
        if tr.stats.channel == 'HHX':
            tr.stats.channel = 'HHE'
        elif tr.stats.channel == 'HHY':
            tr.stats.channel = 'HHN'
        
        tr.write(tr.id + ".miniseed", format="MSEED") 

