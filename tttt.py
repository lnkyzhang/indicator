import talib as ta
import pandas as pd
import numpy as np
from  MyTT import *     


micro=5
mini=10
short=20
mid=60
long=120
huge=250

contiShortShortDays = 10

# self.trendValue = []

# self.CLOSE = None
# self.OPEN = None
# self.LOW = None
# self.HIGH = None
# self.VOL = None

# self.microSma = []
# self.miniSma = []
# self.shortSma = []
# self.midSma = []
# self.longSma = []
# self.hugeSma = []

# self.atrShort = []
# natrShort = []
# natrShortSma = []

# self.shortVolumeSma = []
# self.longVolumeSma = []
# self.volumeFloor = []

class Indicator:
    # CLOSE = None
    # OPEN  = None
    # LOW = None
    # HIGH = None
    # VOL = None
    # miniSlope = None
    # microSma = None
    # miniSma = None
    # shortSma = None
    # midSma = None
    # longSma = None
    # hugeSma = None
    # atrShort = None
    # natrShort = None
    # ntr = None
    # shortVolumeSma = None
    # longVolumeSma = None
    # volumeFloor = None
    # trendValue = None
    # extraMiniSlopePosHighest = None
    # shortRangeDurationDays = None
    # extraMiniSlopePosi = None
    # lowDiffMid = None
    # bigEntity = None
    
    # smallShortVolume = None
    # shortBigVolumeNoBreak = None
    # shortBigVolumeUpNoBreak = None
        
    def __init__(self, close,open,low,high,volume):
        self.CLOSE = np.array(close)
        self.OPEN = np.array(open)
        self.LOW = np.array(low)
        self.HIGH = np.array(high)
        self.VOL = np.array(volume)
        
        self.microSma=MA(self.CLOSE,micro)
        self.miniSma=MA(self.CLOSE,mini)
        self.shortSma=MA(self.CLOSE,short)
        self.midSma=MA(self.CLOSE,mid)
        self.longSma=MA(self.CLOSE,long)
        self.hugeSma=MA(self.CLOSE,huge)

        self.microSlope=SLOPE(self.CLOSE,micro)/self.microSma*100
        self.miniSlope=SLOPE(self.CLOSE, mini)/self.miniSma*100
        self.shortSlope=SLOPE(self.CLOSE, short)/self.shortSma*100
        self.midSlope=SLOPE(self.CLOSE, mid)/self.midSma*100
        self.longSlope=SLOPE(self.CLOSE, long)/self.longSma*100
        self.hugeSlope=SLOPE(self.CLOSE, huge)/self.hugeSma*100
        
        self.atrShort = ATR(self.CLOSE, self.HIGH, self.LOW ,short)
        ntr = ATR(self.CLOSE, self.HIGH, self.LOW ,1)/self.shortSma
        natrShort = self.atrShort/self.shortSma
        
        self.bigWave = IF(ntr/natrShort>1.2,1,0)
        self.smallWave = IF(ntr/natrShort<0.8,1,0)
        
        entity = ABS(self.CLOSE - self.OPEN)
        entityShortSma = MA(entity, short)
        self.bigEntity = IF(entity>entityShortSma*1.2,1,0)
        self.smallEntity = IF(entity<entityShortSma*0.8,1,0)
        
        self.lowDiff = (self.CLOSE-LLV(MIN(self.CLOSE, self.OPEN), 15))/self.atrShort
        self.highDiff = (HHV(MAX(self.CLOSE, self.OPEN), 15)-self.CLOSE)/self.atrShort
        self.lowDiffMid = (self.CLOSE-LLV(MIN(self.CLOSE, self.OPEN), 55))/self.atrShort
        
        self.shortVolumeSma = MA(self.VOL, 5)
        self.longVolumeSma = MA(self.VOL, 89)
        self.volumeFloor = IF(self.longVolumeSma - self.shortVolumeSma>0, ((self.longVolumeSma - self.shortVolumeSma)/self.longVolumeSma*0.4 + 0.8)*self.longVolumeSma, self.longVolumeSma)
        
        self.shortBigVolume = IF(((self.VOL > 1.2*self.longVolumeSma) & (self.HOD(self.VOL, 20) <= 2)) | ((self.VOL > 1.5*MIN(self.longVolumeSma, self.shortVolumeSma)) & (self.HOD(self.VOL, 20) <= 3)) | (self.VOL > 2.5*self.longVolumeSma) | (self.HOD(self.VOL,34)==1),0.15, 0)
        self.superShortBigVolume = IF((self.VOL > 1.2*self.shortVolumeSma) & ((self.VOL > 1.5*self.longVolumeSma) & (self.HOD(self.VOL, 20) <= 2)) | ((self.VOL > 1.8* MIN(self.longVolumeSma, self.shortVolumeSma)) & (self.HOD(self.VOL, 20) <= 3)) | (self.VOL > 2.5*self.longVolumeSma) | (self.HOD(self.VOL,55)==1),0.85,0)
        self.midBigVolume = IF((self.VOL > BOLL(self.VOL, mid, 1)[0]) & (self.VOL > self.volumeFloor), 0.1, 0)
        self.superMidBigVolume = IF((self.VOL > BOLL(self.VOL, mid, 2)[0]) & (self.VOL > self.volumeFloor), 0.9, 0)
        self.longBigVolume = IF((self.VOL > BOLL(self.VOL, long, 1)[0]) & (self.VOL > self.volumeFloor), 0.05, 0)
        self.superLongBigVolume = IF((self.VOL > BOLL(self.VOL, long, 2)[0]) & (self.VOL > self.volumeFloor), 0.95, 0)
        self.bigVolume = (self.shortBigVolume>0) | (self.midBigVolume>0)
        self.superBigVolume = (self.superShortBigVolume>0) | (self.superMidBigVolume>0)
        self.skyVolume = IF((self.VOL > BOLL(self.VOL, short, 3)[0])  & (self.VOL > 2*self.longVolumeSma), 1.0, 0)
        self.hugeVolume = IF(((self.VOL > BOLL(self.VOL, short, 3)[0])| (self.VOL > BOLL(self.VOL, long, 3)[0]) | (self.VOL>2.8*self.longVolumeSma)) & (self.VOL > 2*self.longVolumeSma), 1.05, 0)

        self.smallShortVolume =IF(self.VOL < BOLL(self.VOL, short, 1)[0], 0.15, 0)
    
        self.extraMiniSlopeNeg=IF(self.LOD(self.miniSlope, long) <= 2, self.miniSlope, None)
        self.extraMiniSlopePosi=IF(((self.HOD(self.miniSlope, long) <= 2 )| (self.HOD(self.miniSlope, mid) <=1)) & (self.miniSlope>1.5), self.miniSlope, None)

        self.extraMiniSlopeNegLowest=IF((BARSLAST(self.extraMiniSlopeNeg) < BARSLAST(self.miniSlope>0)) & (self.CLOSE >self.shortSma),
                                LLV(self.LOW, (BARSLAST((self.miniSlope>0) & (self.CLOSE >self.shortSma))+1)[-1]),
                                0)
        self.extraMiniSlopePosHighest=IF((BARSLAST(self.extraMiniSlopePosi) < BARSLAST(self.miniSlope<0)) & (self.CLOSE <self.shortSma),
                                    HHV(self.HIGH, (BARSLAST((self.miniSlope<0) & (self.CLOSE <self.shortSma))+1)[-1]),
                                    0)
        self.TrendValue()
        self.ShortRange()
        self.VolIndicate()
        self.EPoint()

    def LOD(self, npArray:np.array, period):
        return self.sortRank(npArray, period, "self.LOD")
        
    def HOD(self, npArray:np.array, period):
        return self.sortRank(npArray, period, "self.HOD")

    def sortRank(self, npArray:np.array, period, ascending="self.LOD"):
        '''
        self.HOD is ascending
        self.LOD is ~ ascending
        '''
        matrix = np.lib.stride_tricks.sliding_window_view(npArray,period)
        
        # np insert
        if ascending == "self.HOD":
            sortArray = np.argwhere(matrix.argsort()[:,::-1]==(period-1)) + 1
        elif ascending == "self.LOD":
            sortArray = np.argwhere(matrix.argsort()==(period-1)) + 1
        
        return np.insert(sortArray.T[-1].astype(float), 0, [period]*(period-1))

    def TrendValue(self):
        biasValue = MAX(self.CLOSE, MAX(self.microSma, MAX(self.miniSma, MAX(self.shortSma, MAX(self.midSma, MAX(self.longSma, self.hugeSma)))))) - MIN(self.CLOSE, MIN(self.microSma, MIN(self.miniSma, MIN(self.shortSma, MIN(self.midSma, MIN(self.longSma, self.hugeSma))))))
        almostBiasValue = MAX(self.CLOSE, MAX(self.microSma, MAX(self.miniSma, MAX(self.shortSma, MAX(self.midSma, self.longSma))))) - MIN(self.CLOSE, MIN(self.microSma, MIN(self.miniSma, MIN(self.shortSma, MIN(self.midSma, self.longSma)))))


        stdShort = ta.STDDEV(self.CLOSE, timeperiod=20, nbdev=1)/self.atrShort
        shortBias = (MAX(MAX(MAX(MAX(MA(self.CLOSE,5), MA(self.CLOSE,10)),self.shortSma),self.CLOSE),MA(self.CLOSE,34)) - MIN(MIN(MIN(MIN(MA(self.CLOSE,5), MA(self.CLOSE,10)),self.shortSma),self.CLOSE),MA(self.CLOSE,34)))/self.atrShort
        closeDensityState = (stdShort<1) & (shortBias<1.5)
        closeDensity = closeDensityState | (BARSLAST(closeDensityState)<=BARSLAST(self.CLOSE<REF(self.CLOSE,1)))

        denseSma = (biasValue < self.atrShort) | (biasValue < self.CLOSE*0.05) | ((self.longSma > self.hugeSma) & ((almostBiasValue<self.atrShort) | (almostBiasValue<self.CLOSE*0.05)))
        denseSmaLoose = (~(denseSma)) & (biasValue < self.atrShort * 2)
        almostDenseSma = ((~(denseSma)) & (almostBiasValue < self.atrShort * 1.5)) | (((HHV(self.shortSma,20) - LLV(self.shortSma,20))<self.atrShort) & (self.shortSlope > -0.5))
        longRange = (~(denseSma)) & (self.midSma>=self.longSma*1.01) & (HHV(self.midSma,10) < self.midSma*1.01) & (self.longSma >=self.hugeSma*1.01) & (self.hugeSlope > 0) & (self.shortSma>=self.longSma*1.01)
        almostLongRange = (~(longRange)) & (~(almostDenseSma)) & (self.shortSma>=self.longSma*1.01) & (self.shortSma>= self.hugeSma*1.01) & (self.shortSma>=self.midSma*1.01)
        shortRange = (~(denseSma)) & (~(closeDensity)) & (self.longSma>=self.midSma*1.01) & (self.hugeSma>=self.longSma*1.01)  & (self.hugeSlope < 0) & (self.longSma>=self.shortSma*1.01)
        almostShortRange = (~(shortRange)) & (~(almostDenseSma)) & (self.longSma>=self.shortSma*1.01) & (self.hugeSma>=self.shortSma*1.01) & (self.midSma>=self.shortSma*1.01)
        noObviousTrend = (~(denseSma)) & (~(almostDenseSma)) & (~(longRange)) & (~(almostLongRange)) & (~(shortRange)) & (~(almostShortRange))


        self.trendValue = 0
        self.trendValue=IF(denseSma | (BARSLAST(denseSma) <= BARSLAST(self.CLOSE < REF(self.CLOSE,1))),
                    1,
                    IF(longRange, 
                        2,
                        IF(closeDensity,
                            0.5,
                            IF(shortRange, 
                            -1,
                            IF(almostDenseSma | denseSmaLoose | (BARSLAST(denseSma) <= BARSLAST(self.CLOSE < REF(self.CLOSE,1)) & ((~(almostDenseSma)) | (~(denseSma)))),
                                0.5,
                                IF(almostLongRange, 
                                    1.5,
                                    IF(almostShortRange, 
                                        -0.5,
                                        0
        )))))))


    def VolIndicate(self):
        # 空头下的大量大波动
        bigVolumeWave = (self.bigWave & 
                        IF(self.trendValue<0,
                            (self.superShortBigVolume>0) | (self.hugeVolume>0) | (self.skyVolume>0),
                            IF(self.trendValue==0,
                            self.shortBigVolume>0,
                            self.bigVolume>0))) | \
                        ((self.hugeVolume>0) & (self.skyVolume>0) & (self.smallEntity < 0) & (self.smallWave<0))
        self.shortBigVolumeWave = bigVolumeWave & (self.CLOSE < self.shortSma) & (self.LOW - LLV(self.LOW,15) < self.atrShort) & IF(self.CLOSE<self.OPEN, self.LOD(self.CLOSE,3)==1,self.bigEntity)
        self.aaa = None
        # shortBigVolumeWave的最低值
        extraMiniSlopeNegStrict=IF(self.LOD(self.miniSlope, long) <= 2, self.miniSlope, 0)
        mulLowDiff = IF(extraMiniSlopeNegStrict<0, 3, 1.5)
        shortBigVolumeWaveLowest=IF(((HHV(self.HIGH,BARSLAST(self.shortBigVolumeWave)[-1]+1) < REF(self.LOW, BARSLAST(self.shortBigVolumeWave)[-1]) + 3*self.atrShort) | (BARSLAST(self.shortBigVolumeWave) <  BARSLAST(self.CLOSE > self.midSma))) & (LLV(self.LOW,BARSLAST(self.shortBigVolumeWave)[-1]+1) > REF(self.LOW, BARSLAST(self.shortBigVolumeWave)[-1]) - mulLowDiff*self.atrShort),
                                    REF(self.LOW, BARSLAST(self.shortBigVolumeWave)[-1]+1),
                                    0)
            
        # shortBigVolumeWave后的最低值
        barlastCount = BARSLAST(self.shortBigVolumeWave & (self.LOW==shortBigVolumeWaveLowest))
        afterShortBigVolumeWaveLowest=LLV(self.LOW,BARSLAST(self.shortBigVolumeWave & (self.LOW==shortBigVolumeWaveLowest))[-1]+1)
        self.shortBigVolumeNoBreak=IF(shortBigVolumeWaveLowest>0,0.5,0)


        # 多头下的大量大波动
        bigVolumeWaveUp = (self.bigWave & (((self.superShortBigVolume>0) & (self.lowDiff>2.0)) | (self.hugeVolume>0) | (self.skyVolume>0))) | ((self.hugeVolume>0) & (self.skyVolume>0) & (self.smallEntity < 0) & (self.smallWave<0))
        self.shortBigVolumeWaveUp = bigVolumeWaveUp & \
                                (self.CLOSE > self.shortSma) & \
                                (HHV(self.HIGH,15)-self.HIGH < self.atrShort) & \
                                ((self.HOD(self.CLOSE,3)==1) | (self.HOD(self.HIGH,3)==1)) & \
                                ((self.HOD(self.CLOSE,60)==1) | (self.HOD(self.HIGH,60)==1)) & \
                                ((self.CLOSE - self.midSma > 3*self.atrShort) | (HHVBARS(self.CLOSE, 120)==0)) & \
                                IF(self.lowDiff<3, 
                                ((self.superShortBigVolume>0) & (self.superMidBigVolume>0)) | (self.hugeVolume>0) | (self.skyVolume>0), 
                                1)

        # shortBigVolumeWaveUp的最高值
        extraMiniSlopePosStrict=IF(self.HOD(self.miniSlope, huge) <= 2, 
                                self.miniSlope, 
                                0)
        mulHighDiff = IF(self.extraMiniSlopePosHighest>0, 
                        3, 
                        1.5)
        shortBigVolumeWaveHighest=IF((HHV(self.HIGH,BARSLAST(self.shortBigVolumeWaveUp)[-1]+1) < REF(self.HIGH, BARSLAST(self.shortBigVolumeWaveUp)[-1]) + mulHighDiff*self.atrShort) & \
                                    (LLV(self.HIGH,BARSLAST(self.shortBigVolumeWaveUp)[-1]+1) > REF(self.HIGH, BARSLAST(self.shortBigVolumeWaveUp)[-1]) - 3*self.atrShort),
                                    REF(self.HIGH, BARSLAST(self.shortBigVolumeWaveUp)[-1]),
                                    0)
        
        # shortBigVolumeWaveUp后的最高值
        barlastCountUp = BARSLAST(self.shortBigVolumeWaveUp & (self.LOW==shortBigVolumeWaveHighest))
        afterShortBigVolumeWaveUpHighest=HHV(self.HIGH,BARSLAST(self.shortBigVolumeWaveUp & (self.HIGH==shortBigVolumeWaveHighest))[-1])
        self.shortBigVolumeUpNoBreak=IF(shortBigVolumeWaveHighest>0,0.3,0)

    def ShortRange(self):

        shortRangeDurationState = (self.CLOSE < REF(self.CLOSE, 1)) | (self.CLOSE < self.shortSma)
        shortRangeDaysCount = COUNT(shortRangeDurationState,contiShortShortDays)
        self.shortRangeDurationDays = (COUNT(shortRangeDurationState,contiShortShortDays) >= 8) & (self.CLOSE < self.shortSma)

        longRangeDurationState = (self.CLOSE > REF(self.CLOSE, 1)) | (self.CLOSE > self.shortSma)
        longRangeDurationDays = (COUNT(longRangeDurationState,contiShortShortDays) >= 8) & (self.CLOSE > self.shortSma)

        # 通过方差来计算据均线密集
        stdRatio = STD(self.CLOSE,20)/self.shortSma
        stdValue = STD(self.CLOSE,20)
        stdDense = (stdValue<self.atrShort*0.66) & (ABS(self.CLOSE-self.shortSma)<self.atrShort/2)

        # 通过20日均线的浮动来计算均线密集
        shortSmaDiff = HHV(self.shortSma,20) - LLV(self.shortSma,20);
        shortSmaDense = (shortSmaDiff<self.atrShort) & (ABS(self.CLOSE-self.shortSma)<self.atrShort/2)
        return self.shortRangeDurationDays

    def EPoint(self):
        # self.trendValue=2 连续持续20天以上
        trendHighestContiState = COUNT(self.trendValue == 2, 20) == 20
        trendHighestWait = (BARSLAST(trendHighestContiState)[-1] < 40) & (self.trendValue <= 1)

        # 该指标引用其他已经定义的指标
        bigGains = (self.CLOSE - REF(self.CLOSE,1))/REF(self.CLOSE,1) > self.atrShort*3/self.CLOSE;
        jumper = MIN(self.CLOSE, self.OPEN) - REF(self.CLOSE,1) > self.atrShort

        # 空头排列突破入场
        # 0.5: 是缩量未进场   0.4:是超量未进场
        EPoint=IF(REF(self.shortRangeDurationDays,1) & (not(self.shortRangeDurationDays)) & (not(self.extraMiniSlopePosi)),
        IF(trendHighestWait, 0.7,
        IF((self.lowDiffMid>5) & ((self.extraMiniSlopeNegLowest>0) | (self.shortBigVolume==0)), 0.8,
        IF((self.CLOSE<self.OPEN) & (self.bigEntity),0.3,
        IF(self.skyVolume | self.hugeVolume, IF(self.lowDiff < 2, 1, 0.4),
        IF(self.HOD(MAX(self.CLOSE, self.OPEN),5)>1, 0.1,
        IF((self.CLOSE<(REF(self.OPEN,1))) | (self.microSlope < -0.1) | (self.VOL < self.volumeFloor), 0.2,
        IF(self.trendValue > 1, IF((self.shortBigVolumeUpNoBreak==0) & (((self.VOL > self.volumeFloor) & (self.lowDiff < 2.2)) | (self.bigVolume & (self.lowDiff < 3))), 1, 0.5),							#多头排列时候，如果明显缩量，就不能进场
        IF(REF(self.shortBigVolumeNoBreak & (self.lowDiff < 4) & (self.trendValue >=0), 1) > 0,1,
        IF(bigGains, 0.4,
        IF(self.trendValue == 0 , self.shortBigVolume & (self.midBigVolume | self.longBigVolume) & (self.lowDiff < 3),
        IF(self.trendValue < 0, IF((self.lowDiff < 2) & self.shortBigVolume, 1 , IF((self.lowDiff < 3) & self.superShortBigVolume & ((self.bigWave > 0) | (self.bigEntity > 0)), 0.6, 0)),
        IF(jumper,0.4,
        IF(jumper,0.4,
        IF((self.bigEntity | self.bigWave) & (self.lowDiff < 2) & (self.CLOSE> self.OPEN) & self.bigVolume, 1, 0)))
        )))
        )))
        )))
        )),0)

        # 入场时前5天内平均值和入场当天差值百分比
        fourSma = MA(self.CLOSE, 4);
        avgLowDiffRadio = (self.CLOSE - REF(fourSma, 1))/self.CLOSE
        _avgLowDiffRadio = IF(EPoint>0, avgLowDiffRadio, 0)

        # 空头排列Second入场
        EPointSecondDur= IF(IF(self.bigWave, not(self.smallEntity), 1) & IF((self.CLOSE > self.OPEN) | (self.CLOSE > REF(self.CLOSE,1)), 1,(self.CLOSE>self.shortSma) & self.smallShortVolume),1,0)
        EPointSecond=IF((BARSLAST(EPoint=0.5) < 5) & (BARSLAST(EPoint=0.5) <= BARSLAST(EPointSecondDur=0)) & (EPoint==0), self.VOL>self.volumeFloor,0)



        # 放量大波动且斜率极值下反转入场,此入场点后续若没有明显突破，则马上离场，笑脸
        extraLowState = ((REF(self.shortBigVolumeNoBreak,1)>0) & (REF(self.extraMiniSlopeNeg, 1)<0)) | ((self.CLOSE>self.OPEN) & self.shortBigVolumeWave) & LLVBARS(self.CLOSE,60)<=3 ;
        # 放量进
        RPoint=IF(extraLowState & (self.shortSma < self.midSma) & (self.CLOSE > REF(self.CLOSE,1)) & (self.CLOSE > REF(self.OPEN,1)) & self.superShortBigVolume & self.bigEntity & (self.trendValue <= 0), 1, 0)

        RPoint=IF(RPoint, RPoint, (LLVBARS(self.CLOSE,120)<=3) & (self.VOL>self.volumeFloor) & REF(self.bigEntity, 2) & REF(self.bigWave, 2) & (REF(self.CLOSE, 2) <REF(self.OPEN, 2)) & (self.shortSma < self.midSma) & self.bigEntity & self.bigWave & (self.CLOSE > self.OPEN) & (self.LOD(MIN(self.CLOSE, self.OPEN),3)==1) & (self.HOD(MAX(self.CLOSE, self.OPEN),3)==1) & (LLV(MIN(self.CLOSE, self.OPEN),60)==LLV(MIN(self.CLOSE, self.OPEN),3)))
        RPoint=IF(RPoint,RPoint, (extraLowState | REF(extraLowState,1)) & (REF(MIN(self.CLOSE,self.OPEN),1)==LLV(MIN(self.CLOSE,self.OPEN),60)) & (REF(self.extraMiniSlopeNegLowest,1)>0) & (self.shortSma < self.midSma) & (self.VOL>self.volumeFloor) & self.bigEntity & self.bigWave & (MAX(self.CLOSE,self.OPEN)>HHV(MAX(self.CLOSE,self.OPEN),5)-(self.atrShort/3)))

        # Epoint = 0.1 的入场条件 入场不是5天最高价
        # 上影线要短
        EPointHOD = ((COUNT(EPoint==0.1,8)>0) & (LLV(self.CLOSE,BARSLAST(EPoint==0.1)) > REF(MIN(self.CLOSE,self.OPEN)), BARSLAST(EPoint==0.1))-(self.atrShort/3)) & (self.HOD(MAX(self.CLOSE, self.OPEN),5)==1) & (self.CLOSE>self.OPEN) & (self.lowDiff < 2) & (self.VOL>self.volumeFloor) & (self.HIGH-self.CLOSE < (self.CLOSE-self.OPEN)/2)


        # Epoint = 0.2 的入场条件 入场时为满足一些条件 黄色圆点
        _lowDiff = IF(EPoint>0, self.lowDiff, 0)
        EPointB = (((EPoint==0.2) & (self.lowDiff<2.2)) | ((BARSLAST(EPoint==0.2)<10) & (EPoint!=0.2) & (self.lowDiff<3))) & (self.CLOSE > self.shortSma*1.01) & (self.CLOSE > self.OPEN) & (self.HOD(MAX(self.CLOSE, self.OPEN),5)==1) & ((self.bigEntity>0) | ((self.bigWave>0) & (self.smallEntity==0)))
        EPointBB = (COUNT(EPointB, 10) == 1) & EPointB

        # Epoint=0.4 红色三角形
        EPointHugeVol=IF((BARSLAST(EPoint==0.4) < 8) & (self.CLOSE > self.OPEN) & (BARSLAST(EPoint==0.4) > 0) & (BARSLAST(EPoint==0.4) < BARSLAST((self.skyVolume | self.hugeVolume) & ((self.bigWave & self.smallEntity) | ((not(self.smallEntity)) & self.CLOSE < self.OPEN)))) & (BARSLAST(EPoint=0.4) <= BARSLAST(((self.bigWave | self.bigEntity) & (self.CLOSE < self.OPEN))) | (self.CLOSE < REF(self.OPEN,BARSLAST(EPoint==0.4)))),
        IF(self.trendValue <= 0, self.shortBigVolume & (self.CLOSE > REF(self.CLOSE,1)), self.shortBigVolume), 0)
        EPointHugeVolL = (REF(BARSLAST(EPointHugeVol),1)>10) & EPointHugeVol

        # Entry = 0.6 的入场条件：空中加油
        launchDays = IF(COUNT(EPoint == 0.6, 21) > 0, BARSLAST(EPoint == 0.6), 99)
        launchLowest = IF(launchDays<21, IF(REF(self.lowDiff, launchDays) < 3, REF(LLV(MIN(self.CLOSE, self.OPEN), 15)-self.atrShort, launchDays), REF(self.OPEN, launchDays)), 9999) 

        EPointL = (launchDays>0) & (launchDays < 21) & (LLV(MIN(self.CLOSE,self.OPEN), launchDays) > REF(self.CLOSE, launchDays)) & (self.CLOSE > REF(self.CLOSE, 1)) & (self.CLOSE > self.OPEN) & (not(self.smallEntity) & (self.smallWave>0)) & (self.lowDiff < 3)


        # Entry = 0.7 长期trendValue=2后低于trendValue=1入场,红叉 BARSLAST(self.bigEntity & self.bigWave & self.VOL>self.volumeFloor & self.CLOSE < self.OPEN) > trendHighestLaunchDays
        trendHighestLaunchDays = IF(COUNT(EPoint == 0.7, 21) > 0, BARSLAST(EPoint == 0.7), 99)
        EPointT = (LLVBARS(MIN(self.CLOSE,self.OPEN),20) > trendHighestLaunchDays) & (BARSLAST(self.bigEntity & self.bigWave & (self.VOL>self.volumeFloor) & (self.CLOSE < self.OPEN)) > trendHighestLaunchDays) & (trendHighestLaunchDays > 0) & (trendHighestLaunchDays<21) & (self.CLOSE>HHV(self.CLOSE,21)-(self.atrShort/3)) & (self.VOL>self.volumeFloor) & (self.bigEntity > 0) & (self.bigWave > 0) & (self.CLOSE > self.OPEN) & (self.CLOSE > REF(self.CLOSE,1)) & (self.lowDiff<3)
        # 0.7当日均线密集入场
        EPointT = IF(EPointT, EPointT, (trendHighestLaunchDays == 0) & (self.HOD(self.CLOSE,5)==1) & (self.VOL>self.volumeFloor) & (self.lowDiff < 3) & (self.CLOSE > self.OPEN))
        EPointTT = (COUNT(EPointT,10)==1) & (EPointT>0)

        # Entry = 0.8 lowDiffMid过大



        # Entry 密集突破 self.trendValue=1时向上突破 红色圆框
        EPointD = (self.HOD(MAX(self.CLOSE, self.OPEN),5)==1) & (COUNT(self.bigVolume, 10)<3) & (COUNT(self.trendValue==1,10)>7) & (self.CLOSE>self.OPEN) & (self.CLOSE > self.shortSma) & (not(self.smallEntity)) & (not(self.smallWave)) & (((self.VOL>self.shortVolumeSma) & (self.lowDiff < 3)) | ((self.VOL>self.volumeFloor) & (self.lowDiff < 2)))

        # Entry 选股用
        Entry : (EPoint == 1) | (EPointHugeVol>0) | (EPointSecond > 0) | (RPoint > 0) | (EPointBB > 0) | (EPointL > 0) | (EPointD > 0) | (EPointTT>0)

        {止损: 错误入场信号}
        secondDown = (self.bigEntity>0 | (self.bigWave>0 & self.smallEntity=0)) & (self.VOL > self.volumeFloor | self.VOL > REF(self.VOL, 1)*0.8 ) & self.CLOSE < self.OPEN & self.CLOSE < MIN(REF(self.OPEN,1), REF(self.CLOSE,2));
        DRAWICON(REF(Entry,1)=1 & secondDown,0.5,5);

        threeDaysDown = BARSLAST(Entry=1) <= 3 & (self.bigEntity>0 | (self.bigWave>0 & self.smallEntity=0)) & self.VOL > self.volumeFloor & self.CLOSE < self.OPEN & self.CLOSE < REF(self.CLOSE,1) & REF(self.OPEN, BARSLAST(Entry=1)) > self.CLOSE;
        DRAWICON(threeDaysDown,0.6,5);


        {离场}
        exitMicroPrice = IF(self.smallEntity=0, self.CLOSE<self.microSma, self.CLOSE + (self.atrShort/3) <= self.microSma) & self.CLOSE < REF(self.CLOSE,1) & (REF(LLV(self.CLOSE, 3), 1) > self.CLOSE + (self.atrShort/3) | self.CLOSE < MIN(REF(self.OPEN,1), REF(self.CLOSE,1)) - (self.atrShort/3));
        exitMiniPrice = IF(self.smallEntity=0, self.CLOSE<self.miniSma, self.CLOSE + (self.atrShort/3) <= self.miniSma) & self.CLOSE < REF(self.CLOSE,1) & (REF(LLV(self.CLOSE, 3), 1) > self.CLOSE + (self.atrShort/3) | self.CLOSE < MIN(REF(self.OPEN,1), REF(self.CLOSE,1)) - (self.atrShort/3));

        {exit:放量大实体后跌破， 绿色圆点}
        {IF(self.trendValue=2, (self.shortBigVolumeUpNoBreak | self.shortBigVolume) & REF(MAX(self.CLOSE,self.OPEN),) BARSLAST(self.shortBigVolumeWaveUp)  )}


        volReversalState = self.shortBigVolumeUpNoBreak & exitMicroPrice & IF(BARSLAST(self.shortBigVolumeWaveUp) < 10, self.CLOSE < REF(MIN(self.OPEN, self.CLOSE), BARSLAST(self.shortBigVolumeWaveUp)) | (self.HOD(MAX(self.OPEN,self.CLOSE), 60)=1 & self.LOD(MIN(self.CLOSE,self.OPEN),3)=1) | (self.bigVolume & HHVBARS(self.CLOSE,120)<5),1),NODRAW;
        exitBigWasve = IF(volReversalState,IF(self.trendValue > 1.0,IF(self.shortBigVolume, 1, IF(HHVBARS(self.CLOSE,120)<5, self.bigVolume,self.VOL>self.volumeFloor & exitMiniPrice)), self.VOL>self.volumeFloor & self.CLOSE < REF(MAX(self.OPEN, self.CLOSE), BARSLAST(self.shortBigVolumeWaveUp))),0),NODRAW;
        {exitBigWasveS : exitBigWasve & (REF(BARSLAST(exitBigWasve), 1)>10 | REF(BARSLAST(exitBigWasve), 1) >= BARSLAST(Entry)-1);}
        exitBigWasveS = exitBigWasve & (REF(BARSLAST(exitBigWasve), 1)>10);
        DRAWICON(exitBigWasveS,0.6,11);


        {exit:长期多头条件下，跌破20日均线，highDiff>2，红色圆点}
        exitLongRangeBreak = REF(longRangeDurationDays,1) & self.highDiff>2 & NOT(longRangeDurationDays) & (self.VOL > self.volumeFloor | self.bigEntity | self.bigWave);
        DRAWICON(exitLongRangeBreak,0.58,10);


        {exit:大波动大实体收阴，前一天收盘创新高，当天大波动大实体收阴,黄色圆点}
        bigWaveBigEntityShadow = self.bigWave & self.bigEntity & self.CLOSE < self.OPEN;		{大量大实体收阴}
        engulfingPattern = self.CLOSE < self.OPEN & REF(self.CLOSE,1)> REF(self.OPEN,1) & BARSLASTCOUNT(self.bigEntity) > 1 & BARSLASTCOUNT(self.bigWave) > 1 & self.OPEN >= REF(self.CLOSE,1) & self.CLOSE <= REF(self.OPEN,1); {吞没形态}
        breakDown = self.CLOSE<self.OPEN & self.bigWave & self.bigEntity & REF(self.HOD(self.CLOSE,5),1)=1 & self.CLOSE=LLV(MIN(self.OPEN,self.CLOSE),5);	{5日跌破形态}
        breakDownFour = self.CLOSE<self.OPEN & self.bigWave & self.bigEntity & REF(self.HOD(self.CLOSE,5),1)=1 & self.CLOSE=LLV(MIN(self.OPEN,self.CLOSE),4);	{4日跌破形态}
        engulfingBreakdown = self.CLOSE<self.OPEN & self.bigWave & self.bigEntity & self.HOD(MAX(self.OPEN,self.CLOSE),5)=1 & self.CLOSE=LLV(MIN(self.OPEN,self.CLOSE),3); {吞没跌破形态}

        {1.短期放量，收盘是5日内最低，跌破10日均线}
        {2，volume>self.volumeFloor, 实体覆盖前两日实体，跌破10日均线}
        exitEngulfing = IF(self.shortBigVolume & exitMiniPrice, breakDown , IF(self.VOL>self.volumeFloor, engulfingBreakdown, 0));
        {3.前一天天量，当天天量，收盘低于前收}
        exitEngulfing = IF(exitEngulfing, exitEngulfing, bigWaveBigEntityShadow & REF(self.skyVolume | self.hugeVolume, 1) & (self.skyVolume | self.hugeVolume) & REF(self.CLOSE,1) > REF(self.OPEN,1) & self.CLOSE < self.OPEN & self.OPEN > REF(self.CLOSE,1) & self.CLOSE <REF(self.CLOSE,1));
        {4.昨日天量，连续天量，收盘低于前日实体最高值}
        exitEngulfing = IF(exitEngulfing, exitEngulfing, bigWaveBigEntityShadow & BARSLASTCOUNT(self.skyVolume | self.hugeVolume)>2 & self.CLOSE < MAX(REF(self.OPEN,1), REF(self.CLOSE,1)));
        {5.吞没形态 创250日新高 短期放量  斜率极值}
        exitEngulfing = IF(exitEngulfing, exitEngulfing, engulfingPattern & self.HOD(MAX(self.HIGH,self.CLOSE),250)=1 & self.extraMiniSlopePosHighest>0 & self.superShortBigVolume>0);
        {6. 250日最高量且斜率极值极高  大量大实体收阴 且价格低于前高}
        exitEngulfing = IF(exitEngulfing, exitEngulfing, self.HOD(self.VOL,250)=1 & self.extraMiniSlopePosHighest>0 & bigWaveBigEntityShadow & (self.skyVolume or self.hugeVolume) & self.CLOSE < REF(MAX(self.CLOSE,self.OPEN),1));
        {7. 前日250最高价且斜率极值极高  大量大实体收阴， 4日跌破形态  }
        exitEngulfing = IF(exitEngulfing, exitEngulfing, REF(self.HOD(MAX(self.CLOSE,self.OPEN),250),1)=1 & self.extraMiniSlopePosHighest>0 & bigWaveBigEntityShadow & breakDownFour);
        DRAWICON(exitEngulfing,0.2,12);
            
    
    




# if __name__ == '__main__':
#     import akshare as ak

#     stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="002466", period="daily", start_date="20210301", end_date='20230227', adjust="")
    
    
#     close = list(stock_zh_a_hist_df['收盘'])
#     open = list(stock_zh_a_hist_df['开盘'])
#     high = list(stock_zh_a_hist_df['最高'])
#     low = list(stock_zh_a_hist_df['最低'])
#     volume = list(stock_zh_a_hist_df['成交量'])
    
#     InitIndicate(close,open,low,high,volume)
#     a = VolIndicate(close,open,low,high,volume)
#     pass