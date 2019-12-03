#!/bin/sh

#python -i analysisPlots.py  --signal SMS --small
#python -i analysisPlots.py  --noData
python -i analysisPlots.py --region high_DY
python -i analysisPlots.py --region low_sig --signal SMS
python -i analysisPlots.py --region med_sig --signal SMS
python -i analysisPlots.py --region high_sig --signal SMS

python -i analysisPlots.py --region low_sig --signal SMS --noData 
python -i analysisPlots.py --region med_sig --signal SMS --noData
python -i analysisPlots.py --region high_sig --signal SMS --noData


