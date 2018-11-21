# Standard imports
import ROOT
import os

# RootTools
from RootTools.core.standard import *

#Get flat ntuple files + prediction files
def get_flat_files( flat_directory, predict_directory, maxN = -1 ):

    #get predict files
    predict_files = os.listdir(predict_directory)
    #remove DeepJet log file
    if 'tree_association.txt' in predict_files:
        predict_files.remove('tree_association.txt')       

    #get only maxN files
    if len(predict_files)>maxN and maxN>0:
        del predict_files[maxN:]

    #get flat files
    flat_files = predict_files
    flat_files = [file_name.replace('_predict.root', '.root') for file_name in flat_files]

    #append directory to file names
    flat_files    = [file_name.replace(file_name, os.path.join(flat_directory,    file_name)) for file_name in flat_files   ]
    predict_files = [file_name.replace(file_name, os.path.join(predict_directory, file_name)) for file_name in predict_files]

    return flat_files, predict_files

def get_flat_sample( training_name, sample_name, flat_files, predict_files):

    postfix = '_predict'
    flat_sample         = Sample.fromFiles( training_name,         texName = sample_name,            files = flat_files,    treeName='tree' ) 
    flat_sample_predict = Sample.fromFiles( training_name+postfix, texName = sample_name+postfix,    files = predict_files, treeName='tree' ) 
    flat_sample.addFriend( flat_sample_predict, 'tree' )

    return flat_sample

def get_flat_variables(noTraining):

    flat_variables = [
    "run/I",
    "lumi/I",
    "evt/l",
    "lep_trackerHits/I",
    #Training Variables
    "lep_pt/F",
    "lep_eta/F",
    "lep_phi/F",
    "lep_rho/F",
    "lep_innerTrackChi2/F",

    "lep_relIso03/F",
    "lep_relIso04/F",
    "lep_miniRelIso/F",
    "lep_chargedHadRelIso03/F",
    "lep_chargedHadRelIso04/F",
    "lep_miniRelIsoNeutral/F",
    "lep_miniRelIsoCharged/F",

    "lep_lostHits/I", #lost inner hits
    "lep_innerTrackValidHitFraction/F",
    "lep_trackerLayers/I",
    "lep_pixelLayers/I",
    "lep_trackerHits/I",
    "lep_lostOuterHits/I",
    "lep_jetBTagCSV/F",
    "lep_jetBTagDeepCSV/F",
    "lep_jetBTagDeepCSVCvsB/F",
    "lep_jetBTagDeepCSVCvsL/F",

    "lep_jetDR/F",
    "lep_dxy/F",
    "lep_dz/F",
    "lep_edxy/F",
    "lep_edz/F",
    "lep_ip3d/F",
    "lep_sip3d/F",
    "lep_EffectiveArea03/F",
    "lep_jetPtRatiov1/F",
    "lep_jetPtRatiov2/F",
    "lep_jetPtRelv1/F",
    "lep_jetPtRelv2/F",
    "lep_ptErrTk/F",

    "npfCand_neutral/I",
    "npfCand_charged/I",
    "npfCand_photon/I",
    "npfCand_electron/I",
    "npfCand_muon/I",

    "pfCand_neutral[pt_ptRelSorted/F]",
    "pfCand_charged[pt_ptRelSorted/F]",
    "pfCand_photon[pt_ptRelSorted/F]",
    "pfCand_electron[pt_ptRelSorted/F]",
    "pfCand_muon[pt_ptRelSorted/F]",

    #Electron specific
    "lep_etaSc/F",
    "lep_sigmaIEtaIEta/F",
    "lep_full5x5_sigmaIetaIeta/F",
    "lep_dEtaInSeed/F",
    "lep_dPhiScTrkIn/F",
    "lep_dEtaScTrkIn/F",
    "lep_eInvMinusPInv/F",
    "lep_convVeto/I",
    "lep_hadronicOverEm/F",
    "lep_r9/F",
    "lep_mvaIdFall17noIso/F",
    "lep_mvaIdSpring16/F",
    #Muon specific
    "lep_segmentCompatibility/F",
    "lep_muonInnerTrkRelErr/F",
    "lep_isGlobalMuon/I",
    "lep_chi2LocalPosition/F",
    "lep_chi2LocalMomentum/F",
    "lep_globalTrackChi2/F",
    "lep_glbTrackProbability/F",
    "lep_caloCompatibility/F",
    "lep_trkKink/F",
    #other Variables
    "lep_pdgId/I",
    "lep_mcMatchPdgId/I",
    "lep_mcMatchId/I",
    "lep_mcMatchAny/I",
    "lep_mediumMuonId/I",
    "lep_pfMuonId/I",
    "lep_isPromptId_Training/I",
    "lep_isNonPromptId_Training/I",
    "lep_isFakeId_Training/I",
    "lep_mvaTTH/F",
    "lep_mvaTTV/F",
    "nTrueInt/F",
    "lumi_scaleFactor1fb/F",
    ]

    if not noTraining:
        flat_variables.append("prob_lep_isPromptId_Training/F")
        flat_variables.append("prob_lep_isNonPromptId_Training/F")
        flat_variables.append("prob_lep_isFakeId_Training/F")

    return flat_variables



#flat samples

#unmixed samples
DYvsQCD_Muons_balanced_2016 = {
#'training_name'     : 'DYvsQCD_Muons_balanced_20181108',
#'sample_name'       : 'DYvsQCD_Muons_2016',
#'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/DYvsQCD',
#'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018110801/DYvsQCD_balancedMuonEvaluationTestData',
'training_name'     : 'DYvsQCD_Muons_balanced_20181113',
'training_date'     : '2018111302',
'sample_name'       : 'DYvsQCD_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v5/step3/2016/muo/pt_15_-1/DYvsQCD',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111302/DYvsQCD_balancedMuonEvaluationTestData',
}

DYvsQCD_Muons_balancedSimple_2016 = {
'training_name'     : 'DYvsQCD_Muons_balancedSimple_20181108',
'sample_name'       : 'DYvsQCD_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/DYvsQCD',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018110802/DYvsQCD_balancedSimpleMuonEvaluationTestData',
}

TTJets_Muons_balanced_2016 = {
#'training_name'     : 'TTJets_Muons_balanced_20181108',
#'sample_name'       : 'TTJets_Muons_2016',
#'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/TTJets',
#'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018110803/TTJets_balancedMuonEvaluationTestData',
'training_name'     : 'TTJets_Muons_balanced_20181112',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/TTJets',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181112/TTJets_balancedMuonEvaluationTestData',
}

TTJets_Muons_balancedSimple_2016 = {
'training_name'     : 'TTJets_Muons_balancedSimple_20181108',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/TTJets',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018110804/TTJets_balancedSimpleMuonEvaluationTestData',
}

#mixed samples
DYvsQCD_on_TTJets_Muons_balanced_2016 = {
'training_name'     : 'TTJets_Muons_balanced_20181108',
'sample_name'       : 'DYvsQCD_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/DYvsQCD',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/predictions/muons/20181108/EvaluationTestData_DYvsQCD_on_model_TTJets_balanced_20181108',
}

DYvsQCD_on_TTJets_Muons_balancedSimple_2016 = {
'training_name'     : 'TTJets_Muons_balancedSimple_20181108',
'sample_name'       : 'DYvsQCD_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/DYvsQCD',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/predictions/muons/20181108/EvaluationTestData_DYvsQCD_on_model_TTJets_balancedSimple_20181108',
}

TTJets_on_DYvsQCD_Muons_balanced_2016 = {
'training_name'     : 'DYvsQCD_Muons_balanced_20181108',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/TTJets',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/predictions/muons/20181108/EvaluationTestData_TTJets_on_model_DYvsQCD_balanced_20181108',
}

TTJets_on_DYvsQCD_Muons_balancedSimple_2016 = {
'training_name'     : 'DYvsQCD_Muons_balancedSimple_20181108',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v4/step3/2016/muo/pt_15_-1/TTJets',
'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/predictions/muons/20181108/EvaluationTestData_TTJets_on_model_DYvsQCD_balancedSimple_20181108',
}

#TTJets pt related trainings
TTJets_Muons_balanced_pt5toInf_2016 = {
'training_name'     : 'TTJets_Muons_balanced_pt5toInf_20181114',
'training_date'     : '20181114-01',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTJets',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111401/TTJets_balancedPt5toInfMuonEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111401/TTJets_balancedPt5toInfMuonEvaluationTestDataIsTrainData',
#'training_name'     : 'TTJets_Muons_balanced_pt5toInf_20181115',
#'training_date'     : '20181115',
#'sample_name'       : 'TTJets_Muons_2016',
#'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTJets',
#'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181115/TTJets_balancedPt5toInfMuonEvaluationTestData',
#'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181115/TTJets_balancedPt5toInfMuonEvaluationTestDataIsTrainData',
}

TTJets_Muons_balanced_pt5to15_2016 = {
#'training_name'     : 'TTJets_Muons_balanced_pt5to15_20181113',
#'sample_name'       : 'TTJets_Muons_2016',
#'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v5/step3/2016/muo/pt_5_15/TTJets',
#'predict_directory' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181113/TTJets_balancedLowPtMuonEvaluationTestData',
'training_name'     : 'TTJets_Muons_balanced_pt5to15_20181114',
'training_date'     : '20181114-02',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'              : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_15/TTJets',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111402/TTJets_balancedPt5to15MuonEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111402/TTJets_balancedPt5to15MuonEvaluationTestDataIsTrainData',
}

TTJets_Muons_balanced_pt15to25_2016 = {
'training_name'     : 'TTJets_Muons_balanced_pt15to25_20181114',
'training_date'     : '20181114-03',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTJets',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111403/TTJets_balancedPt15to25MuonEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111403/TTJets_balancedPt15to25MuonEvaluationTestDataIsTrainData',
}

TTJets_Muons_balanced_pt25toInf_2016 = {
'training_name'     : 'TTJets_Muons_balanced_pt25toInf_20181114',
'training_date'     : '20181114-04',
'sample_name'       : 'TTJets_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_25_-1/TTJets',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111404/TTJets_balancedPt25toInfMuonEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/2018111404/TTJets_balancedPt25toInfMuonEvaluationTestDataIsTrainData',
}

#TTs pt related trainings
TTs_Muons_balanced_pt5toInf_2016 = {
'training_name'     : 'TTs_Muons_balanced_pt5toInf_20181117',
'training_date'     : '20181117',
'sample_name'       : 'TTs_Muons_2016',
'flat_directory'    : '/afs/hephy.at/data/gmoertl01/DeepLepton/skims/v6/step3/2016/muo/pt_5_-1/TTs',
'predict_directory'           : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181117/TTs_balanced_pt5toInf_MuonEvaluationTestData',
'predict_directory_trainData' : '/afs/hephy.at/data/gmoertl01/DeepLepton/trainings/muons/20181117/TTs_balanced_pt5toInf_MuonEvaluationTestDataIsTrainData',
}


#usage
#flat_sample = TTJets_Muons_balanced_pt25toInf_2016
#flat_files, predict_files = get_flat_files( flat_sample['flat_directory'], flat_sample['predict_directory'])
#flat_sample = get_flat_sample( flat_sample['training_name'], flat_sample['sample_name'], flat_files, predict_files )

