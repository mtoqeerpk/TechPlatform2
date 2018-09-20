import os
import glob
import numpy as np
import obspy
from obspy.core.utcdatetime import UTCDateTime

# - Merge Files ------------------------------------------------
listing = glob.glob('*.miniseed')

print '* Merging the following files:'
print listing
countStart=True
for infile in listing:
	if(countStart):
		st=obspy.read(infile)
		countStart=False
	else:
		st+=obspy.read(infile)
print '* Data is unsorted'
print(st.__str__(extended=True))
st.sort(['starttime']) 

print '* Data sorted'
print(st.__str__(extended=True))

print '* Traces merged'
st.merge(fill_value=0)
print(st.__str__(extended=True))

st.plot()

# - Load Test Names, Start Times, and End Times ----------------
stime = np.loadtxt('starttime.txt', dtype=str)
etime = np.loadtxt('endtime.txt', dtype=str)
testList = np.loadtxt('testname.txt', dtype=str)

# - Slice traces and create files ------------------------------
if not os.path.isdir('./Output'):
    print '* Creating Output Directory'
    os.mkdir('./Output') 

print '* Slicing merged traces'	
# Export sliced miniseed files
for jj in xrange(stime.size):
    if stime.size == 1:
        t0 = UTCDateTime(str(stime))
        t1 = UTCDateTime(str(etime))
        test = str(testList)
    else:
        t0 = UTCDateTime(str(stime[jj]))
        t1 = UTCDateTime(str(etime[jj]))
        test = str(testList[jj])
    print '    Slicing: ' + test + '  Start: ' + str(t0) + '  End: ' + str(t1)
    st0 = st.slice(t0, t1)

    for tr in st0:
        tr.stats.location = test
        if tr.stats.channel == 'HHX':
            tr.stats.channel = 'HHE'
        elif tr.stats.channel == 'HHY':
            tr.stats.channel = 'HHN'
	st0.plot(outfile = './Output/' + test + '.pdf')
	filename = './Output/' + tr.stats.network + '.' + tr.stats.station + '.' + test + '.miniseed' 
    st0.write(filename, format='MSEED')
	
print '* HVSR test miniseed files created'