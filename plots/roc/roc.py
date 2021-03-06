# Standard imports
import ROOT
import array
import os
import math
from ROOT import gStyle

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',           default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',              action='store_true',                help='Run only on a small subset of the data?', )
argParser.add_argument('--medium',             action='store_true',                help='Run only on a medium subset of the data?', )
argParser.add_argument('--plot_directory',     action='store',           default='deepLepton')
argParser.add_argument('--ptMin',              action='store',      type=int,     default=25)
argParser.add_argument('--ptMax',              action='store',      type=int,     default=0)
argParser.add_argument('--flat',               action='store_true',                 help='Run on flat ntuple data?', )
argParser.add_argument('--flatSample',         action='store',           default='TTJets_Muons_balanced_pt5toInf_2016')
argParser.add_argument('--testFile',           action='store_true',                 help='Run on testFile for full events data?', )

argParser.add_argument('--year',               action='store', type=int, choices=[2016,2017],   default=2016,   help="Which year?")
argParser.add_argument('--flavour',            action='store', type=str, choices=['ele','muo'], default='muo',  help="Which Flavour?")
argParser.add_argument('--testData',           action='store_true',   help="plot test or train data?")
argParser.add_argument('--lumi_weight',        action='store_true',   help="apply lumi weight?")
argParser.add_argument('--wp',                 action='store_true',   help="add WP of standard cut selection")
argParser.add_argument('--fairComp',           action='store_true',   help="fair comparison between analysis and DL")
#argParser.add_argument('--selection',          action='store',      default='dilepOS-njet3p-btag1p-onZ')
args = argParser.parse_args()

# DeepLepton
from DeepLepton.Tools.user import plot_directory

# Logger
import DeepLepton.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

#RootTools
from RootTools.core.standard import *

event_selection = "(1)"

#signal and background sample

if args.flat:
    from DeepLepton.samples.flat_training_samples import *

    nMax = 1 if args.small else -1
    
    flat_sampleInfo = vars()[args.flatSample]
    flat_files, predict_files = get_flat_files( flat_sampleInfo['flat_directory'], flat_sampleInfo['predict_directory' if args.testData else 'predict_directory_trainData'])
    flat_sample = get_flat_sample( flat_sampleInfo['training_name'], flat_sampleInfo['sample_name'], flat_files, predict_files )

    sig_sample = flat_sample
    bkg_sample = flat_sample

    training_name = flat_sample.name
    sample_name   = flat_sample.texName

else:
    #data_directory = "/afs/hephy.at/data/rschoefbeck02/cmgTuples/"
    data_directory = "/afs/hephy.at/data/gmoertl01/cmgTuples/"
    #postProcessing_directory = "deepLepton_v1/inclusive"
    postProcessing_directory = "deepLepton_v4/singlelep"
    from DeepLepton.samples.cmgTuples_deepLepton_Summer16_mAODv2_postProcessed import *

    if args.testFile:
        sig_sample = testFile
        bkg_sample = testFile
        training_name = 'TTs_Muons_20181017'
        sample_name   = 'testFile'
    else:
        sig_sample = TTJets_DiLepton
        bkg_sample = TTJets_SingleLepton
        training_name = 'TTs_Muons_20181017'
        sample_name   = 'TTs_Muons'

        if args.small or args.medium:
            TTJets_DiLepton.reduceFiles( to = 1 if args.small else 50 )
            TTJets_SingleLepton.reduceFiles( to = 1 if args.small else 50 )
            #DY.reduceFiles( to = 1 )
            #QCD.reduceFiles( to = 1 )

# truth categories
prompt_selection    = "(abs(lep_mcMatchId)==6||abs(lep_mcMatchId)==23||abs(lep_mcMatchId)==24||abs(lep_mcMatchId)==25||abs(lep_mcMatchId)==37)"
nonPrompt_selection = "(!(abs(lep_mcMatchId)==6||abs(lep_mcMatchId)==23||abs(lep_mcMatchId)==24||abs(lep_mcMatchId)==25||abs(lep_mcMatchId)==37))&&(abs(lep_mcMatchAny)==4||abs(lep_mcMatchAny)==5)"
fake_selection      = "(!(abs(lep_mcMatchId)==6||abs(lep_mcMatchId)==23||abs(lep_mcMatchId)==24||abs(lep_mcMatchId)==25||abs(lep_mcMatchId)==37))&&(!(abs(lep_mcMatchAny)==4||abs(lep_mcMatchAny)==5))"

if args.flavour == 'muo': 
    # lepton preselection
    loose_id = "abs(lep_pdgId)==13&&lep_pt>5&&abs(lep_eta)<2.4&&lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dxy)<0.05&&abs(lep_dz)<0.1&&lep_pfMuonId&&lep_mediumMuonId"
elif args.flavour == 'ele':
    loose_id = "abs(lep_pdgId)==11&&lep_pt>7&&abs(lep_eta)<2.5&&lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dxy)<0.05&&abs(lep_dz)<0.1&&lep_lostHits<=1"

if args.fairComp:
    if args.flavour == 'muo':
        # lepton preselection
        loose_id = "abs(lep_pdgId)==13&&lep_pt>5&&abs(lep_eta)<2.4"
    elif args.flavour == 'ele':
        loose_id = "abs(lep_pdgId)==11&&lep_pt>5&&abs(lep_eta)<2.5"


#loose_id = "abs(lep_pdgId)==13&&lep_miniRelIso<0.5"
#prep for ele:
# in barrel: loose_id = "abs(lep_pdgId)==11&&lep_pt>5&&abs(lep_eta)<2.4&&lep_miniRelIso<0.4&&lep_sip3d<8&&abs(lep_dxy)<0.05&&abs(lep_dz)<0.1
#&&lep_sigmaIEtaIEta<0.0112&&abs(lep_dEtaInSeed)<0.00377&&lep_hadronicOverEm<#???#&&lep_eInvMinusPInv<0.193&&lep_lostHits<=1&&lep_convVeto==1"
# loose_id = "abs(lep_etaSc)<=1.479"

# pt selection
kinematic_selection      = "lep_pt>{ptMin}".format(ptMin = args.ptMin) if args.ptMax==0 else "lep_pt>{ptMin}&&lep_pt<={ptMax}".format(ptMin = args.ptMin, ptMax = args.ptMax)
kinematic_selection_name = 'pt > '+str(args.ptMin)+' GeV' if args.ptMax==0 else str(args.ptMin)+' GeV < pt < '+str(args.ptMax)+' GeV'

# filter LepOther with nan prediction
filter_LepOther = 'prob_lep_isPromptId_Training<999' if args.flat else 'lep_deepLepton_prompt<999'

#relative lumi weight
if args.flat:
    weightString = 'lumi_scaleFactor1fb' if args.lumi_weight else '1'
else:
    weightString = '1'

# lepton Ids
deepLepton = {"name":"DeepLepton", "var":"prob_lep_isPromptId_Training" if args.flat else "lep_deepLepton_prompt",      "color":ROOT.kGreen+2, "thresholds":[ i/100000. for i in range(0,100000)]}
mvaTTV     = {"name":"TTV",        "var":"lep_mvaTTV",                                                                  "color":ROOT.kGray+1,  "thresholds":[ i/1000. for i in range(-1000,1001)]}
mvaTTH     = {"name":"TTH",        "var":"lep_mvaTTH",                                                                  "color":ROOT.kGray,    "thresholds":[ i/1000. for i in range(-1000,1001)]}

lepton_ids = [
#    mvaTTH, 
#    mvaTTV,
    deepLepton,
]

# get signal efficiency
for lepton_id in lepton_ids:
    logger.info( "At id %s", lepton_id["name"] )
    selectionString = "&&".join( [ kinematic_selection, loose_id,  prompt_selection, filter_LepOther ] )
    print selectionString
    ref                    = sig_sample.getYieldFromDraw( selectionString = selectionString, weightString = weightString) 
    lepton_id["sig_h_eff"] = sig_sample.get1DHistoFromDraw(     lepton_id["var"], lepton_id["thresholds"], selectionString = selectionString, weightString = weightString, binningIsExplicit = True )
    lepton_id["sig_h_eff"].Scale( 1./ref['val'])
    
    selectionString = "&&".join( [ kinematic_selection, loose_id,  "(!("+prompt_selection+"))", filter_LepOther ] )
    print selectionString
    ref                    = bkg_sample.getYieldFromDraw( selectionString = selectionString, weightString = weightString )
    lepton_id["bkg_h_eff"] = bkg_sample.get1DHistoFromDraw( lepton_id["var"], lepton_id["thresholds"], selectionString = selectionString, weightString = weightString, binningIsExplicit = True )
    lepton_id["bkg_h_eff"].Scale( 1./ref['val'])

#    e_S = 0.
#    e_B = 0
#    for i_b in reversed(range( 0, lepton_id["sig_h_eff"].GetNbinsX() + 1 )):
#        print i_b, lepton_id["sig_h_eff"].Integral(i_b, lepton_id["sig_h_eff"].GetNbinsX() + 1), lepton_id["bkg_h_eff"].Integral(i_b, lepton_id["bkg_h_eff"].GetNbinsX() + 1)
    lepton_id["sig_eff" ] = [ lepton_id["sig_h_eff"].Integral(i_b, lepton_id["sig_h_eff"].GetNbinsX() + 1) for i_b in range( 0, lepton_id["sig_h_eff"].GetNbinsX() + 1 )] 
    lepton_id["bkg_eff" ] = [ lepton_id["bkg_h_eff"].Integral(i_b, lepton_id["bkg_h_eff"].GetNbinsX() + 1) for i_b in range( 0, lepton_id["bkg_h_eff"].GetNbinsX() + 1 )] 

    lepton_id["roc"]      = ROOT.TGraph(len(lepton_id["bkg_eff" ]), array.array('d', lepton_id["bkg_eff" ]), array.array('d', lepton_id["sig_eff" ]))
    lepton_id["roc"].SetLineColor( lepton_id['color'] )


    #look at DL thresholds and signal efficiency and background rejection
    if lepton_id == deepLepton:
        for i in range(len(lepton_id["sig_h_eff"])):
            print("sig_eff: ", lepton_id["sig_eff"][i], "bkg_rej: ", lepton_id["bkg_eff"][i], "DL threshold: " ,lepton_id["thresholds"][i])


gStyle.SetOptTitle(0)
c = ROOT.TCanvas()
option = "L"
same    ="A"
for lepton_id in lepton_ids:
    lepton_id["roc"].GetXaxis().SetTitle("background efficiency")
    lepton_id["roc"].GetYaxis().SetTitle("signal efficiency")
    lepton_id["roc"].GetXaxis().SetLimits(0.01, 1)
    lepton_id["roc"].GetHistogram().SetMaximum(1.01)
    lepton_id["roc"].GetHistogram().SetMinimum(0.60)
    lepton_id["roc"].SetLineWidth(2)
    lepton_id["roc"].SetFillStyle(0)
    lepton_id["roc"].SetFillColor(0)
    lepton_id["roc"].SetMarkerColor(lepton_id["color"])
    lepton_id["roc"].SetTitle(lepton_id["name"])
    lepton_id["roc"].Draw(option+same)
    same = "same"


if args.wp:
    analysis_selection = "lep_ip3d<0.01&&lep_sip3d<2&&lep_relIso03<0.5&&(lep_relIso03*lep_pt)<5" 
    
    P_selection     = "&&".join([prompt_selection, kinematic_selection, loose_id, filter_LepOther])
    TP_selection    = "&&".join([prompt_selection, kinematic_selection, loose_id, filter_LepOther, analysis_selection])
    N_selection     = "&&".join(["(!("+prompt_selection+"))", kinematic_selection, loose_id, filter_LepOther])
    FP_selection    = "&&".join(["(!("+prompt_selection+"))", kinematic_selection, loose_id, filter_LepOther, analysis_selection])
    
    P_yield = sig_sample.getYieldFromDraw( selectionString = P_selection, weightString = weightString)
    TP_yield = sig_sample.getYieldFromDraw( selectionString = TP_selection, weightString = weightString)
    N_yield = sig_sample.getYieldFromDraw( selectionString = N_selection, weightString = weightString)
    FP_yield = sig_sample.getYieldFromDraw( selectionString = FP_selection, weightString = weightString)
    
    TPR = TP_yield['val']/P_yield['val']
    FPR = FP_yield['val']/N_yield['val']
    
    n=1
    wp_x, wp_y = array.array( 'd' ), array.array( 'd' )
    wp_x.append(FPR)
    wp_y.append(TPR)
    wp = ROOT.TGraph( n, wp_x, wp_y )
    
    wp.GetXaxis().SetTitle("background efficiency")
    wp.GetYaxis().SetTitle("signal efficiency")
    wp.GetXaxis().SetLimits(0.01, 1)
    wp.GetHistogram().SetMaximum(1.01)
    wp.GetHistogram().SetMinimum(0.60)
    wp.SetFillStyle(0)
    wp.SetFillColor(0)
    wp.SetMarkerColor(46)
    wp.SetMarkerStyle( 20 )
    wp.SetTitle('Analysis-WP')
    wp.Draw('Psame')
    


header = [
            #{'text': ROOT.TPaveLabel(.00,0.96,.20,1.0,  "CMS preliminary",                                                                                                                   "nbNDC"), 'font': 30  },
            {'text': ROOT.TPaveLabel(.00,0.965,1.0,1.0,  "training reference: {trainData}  -  {ref}".format( trainData=flat_sampleInfo['train_data'], ref=flat_sampleInfo['training_name'] ), "nbNDC"), 'font': 130 },
            {'text': ROOT.TPaveLabel(.00,0.905,1.0,0.960, "{testData} {pt}, loose ID selection".format( testData=flat_sampleInfo['test_data'], pt=kinematic_selection_name ),                 "nbNDC"), 'font': 130 },
         ]

for line in header:
    line['text'].SetFillColor(gStyle.GetTitleFillColor())
    line['text'].SetTextFont(line['font'])
    line['text'].Draw()

#c.SetPoint(1, )

c.SetGrid()
c.SetLogx()
#c.BuildLegend(0.695,0.475,0.895,0.595)
c.BuildLegend(0.70,0.43,0.88,0.55)

if args.flat:
    directory = os.path.join(   plot_directory, "DeepLepton", 
                                flat_sampleInfo['sample_name'],
                                flat_sampleInfo['training_date'],
                                'TestData' if args.testData else 'TrainData',
                                'roc',
                            )
    if args.fairComp:
        directory = os.path.join(   plot_directory, "DeepLepton",
                                    flat_sampleInfo['sample_name'],
                                    flat_sampleInfo['training_date'],
                                    'TestData' if args.testData else 'TrainData',
                                    'roc',
                                    'fairComp',
                                )

        
else:
    directory = os.path.join( plot_directory, "DeepLepton", "full_events" ) 

if not os.path.exists(directory):
    os.makedirs(directory)
c.Print(os.path.join( directory, "roc_{kin}_{lumi}.png".format( plot_name = training_name, kin = kinematic_selection, lumi = 'lumi' if args.lumi_weight else 'noLumi' ) ))
