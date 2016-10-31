import glob
import obspy
from obspy.core.utcdatetime import UTCDateTime

def fileMerge(sourceReadPath='./',targetWritePath='./'):
    listing = glob.glob(sourceReadPath+'/*centaur-3*.miniseed')
    print listing
    countStart=True
    for infile in listing:
        #st=obspy.read(infile)
        if(countStart):
            #st=obspy.read(sourceReadPath+"/"+infile)
            st=obspy.read(infile)
            countStart=False
        else:
            #st+=obspy.read(sourceReadPath+"/"+infile)
            st+=obspy.read(infile)


    print '*unsorted*'
    print(st.__str__(extended=True))

    st.sort(['starttime']) 

    print '*sorted*'
    print(st.__str__(extended=True))

    #st.write(targetWritePath+"/"+"outall.miniseed",format="MSEED")

    print '*merged*'
    st.merge(fill_value=0)
    print(st.__str__(extended=True))
    return st
    
def sliceTrace(st,startTime,endTime):
    st_out = st.slice(startTime, endTime)
    return st_out

#st=fileReadWrite("raw data files","merged")
#startTime=UTCDateTime("2016-09-26T02:20:20")
#endTime=UTCDateTime("2016-09-26T02:20:25")
    
#sliceTrace(st,startTime,endTime)
