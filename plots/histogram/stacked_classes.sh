#!/bin/sh

#testData
python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 0   --varSelection simpleClasses --flatSample TTs_Muons_simpleClasses_2016 --testData 
python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 25  --varSelection simpleClasses --flatSample TTs_Muons_simpleClasses_2016 --testData 
python -i stacked_classes.py --flat --looseId --ptMin 25 --ptMax 0   --varSelection simpleClasses --flatSample TTs_Muons_simpleClasses_2016 --testData 

#trainData
python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 0   --varSelection simpleClasses --flatSample TTs_Muons_simpleClasses_2016
python -i stacked_classes.py --flat --looseId --ptMin 10 --ptMax 25  --varSelection simpleClasses --flatSample TTs_Muons_simpleClasses_2016
python -i stacked_classes.py --flat --looseId --ptMin 25 --ptMax 0   --varSelection simpleClasses --flatSample TTs_Muons_simpleClasses_2016

#python -i stacked_classes.py --flat --ptMin 5  --ptMax 0   --flatSample TTs_Muons_simpleClasses_2016
#python -i stacked_classes.py --flat --ptMin 10 --ptMax 0   --flatSample TTs_Muons_simpleClasses_2016
#python -i stacked_classes.py --flat --ptMin 10 --ptMax 25  --flatSample TTs_Muons_simpleClasses_2016
#python -i stacked_classes.py --flat --ptMin 25 --ptMax 0   --flatSample TTs_Muons_simpleClasses_2016
