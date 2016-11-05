from dispel4py.seismo.seismo import SeismoPE
from obspy.core import read
import scipy


class StreamProducer(SeismoPE):
    INPUT_NAME = 'file'
    OUTPUT_NAME = 'output'

    def __init__(self, numIterations=1):
        SeismoPE.__init__(self)
        self._add_input('file')

    def getDataStreams(self, inputs):
        
        self._timestamp = {'starttime': None, 'endtime': None}
        self._location = {'channel': None, 'network': None, 'station': None}
        inputStr = inputs['file']
        self.attr = {'network': None, 'channel': None, 'station': None,
                     'location': None, 'starttime': None, 'endtime': None,
                     'sampling_rate': None, 'npts': None}
        return {"streams": [{'data': inputStr, 'attr': self.attr}]}

    def compute(self):
        
        stream = read(self.st)
        # fills gaps with 0, gap correction should be implemented as PE
        stream.merge()
        outputattr = dict(self.attr)
        outputattr['starttime'] = str(stream[0].stats.starttime)
        outputattr['endtime'] = str(stream[0].stats.endtime)
        outputattr['sampling_rate'] = stream[0].stats.sampling_rate
        outputattr['npts'] = stream[0].stats.npts
        outputattr['location'] = stream[0].stats.location
        outputattr['network'] = stream[0].stats.network
        outputattr['channel'] = stream[0].stats.channel
        outputattr['station'] = stream[0].stats.station

        self._timestamp['starttime'] = outputattr['starttime']
        self._timestamp['endtime'] = outputattr['endtime']
        self._location['network'] = outputattr['network']
        self._location['channel'] = outputattr['channel']
        self._location['station'] = outputattr['station']

        self.outputattr = [outputattr]
        self.outputstreams = [stream[0].data]


class DetrendPE(SeismoPE):

    def __init__(self):
        SeismoPE.__init__(self)

    def compute(self):
        return scipy.signal.detrend(self.st, type='linear')
