# L1Ntuple for ZDC studies with 2023 data
# Hannah Bossi, <hannah.bossi@cern.ch>
# 9/17/2023
import FWCore.ParameterSet.Config as cms
import os
import sys

#from Configuration.Eras.Era_Run3_pp_on_PbPb_cff import Run3_pp_on_PbPb
from Configuration.Eras.Era_Run3_pp_on_PbPb_2023_cff import Run3_pp_on_PbPb_2023
process = cms.Process('RAW2DIGI', Run3_pp_on_PbPb_2023)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_DataMapper_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


from Configuration.AlCa.GlobalTag import GlobalTag
# use the prompt queue for now, will need to update when the full GT becomes available
process.GlobalTag = GlobalTag(process.GlobalTag, '150X_dataRun3_Prompt_Queue', '')

# needed to supress error from cmssw 14
process.add_(cms.Service("AdaptorConfig", native=cms.untracked.vstring("root")))

# To change the number of events, change this part
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/hidata/HIRun2024B/HIZeroBias0/RAW/v1/000/388/305/00000/71ce4979-f1fa-444a-a7a2-17246a3d8658.root'
    )
)



process.options = cms.untracked.PSet(
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Output definition
from Configuration.Applications.ConfigBuilder import MassReplaceInputTag

# Additional output definition

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.endjob_step = cms.EndPath(process.endOfProcess)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step, process.endjob_step)


from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)


# customisation of the process.

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseReEmul
from L1Trigger.Configuration.customiseReEmul import L1TReEmulFromRAW 

#call to customisation function L1TReEmulFromRAW imported from L1Trigger.Configuration.customiseReEmul
process = L1TReEmulFromRAW(process)

# Automatic addition of the customisation function from L1Trigger.L1TNtuples.customiseL1Ntuple
from L1Trigger.L1TNtuples.customiseL1Ntuple import L1NtupleRAWEMU 

#call to customisation function L1NtupleRAWEMU imported from L1Trigger.L1TNtuples.customiseL1Ntuple
process = L1NtupleRAWEMU(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseSettings
from L1Trigger.Configuration.customiseSettings import L1TSettingsToCaloParamsHI_2024_v0_1
process = L1TSettingsToCaloParamsHI_2024_v0_1(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseUtils
from L1Trigger.Configuration.customiseUtils import L1TGlobalMenuXML 

#call to customisation function L1TGlobalMenuXML imported from L1Trigger.Configuration.customiseUtils
process = L1TGlobalMenuXML(process)

# End of customisation functions


# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion


#########################
# ZDC RecHit Producer && Analyzer
#########################
# to prevent crash related to HcalSeverityLevelComputerRcd record
process.load("RecoLocalCalo.HcalRecAlgos.hcalRecAlgoESProd_cfi")
process.load('HeavyIonsAnalysis.ZDCAnalysis.ZDCAnalyzersPbPb_cff')
process.zdcreco_step = cms.Path(process.zdcrecoRun3)
process.zdcanalyzer_step = cms.Path(process.zdcanalyzer)
process.schedule.append(process.zdcreco_step)
process.schedule.append(process.zdcanalyzer_step)
#=======================================================================


# ======================================================================
# ======================== add in the emulator =========================
# unpacked etsums
process.l1UpgradeTree.sumZDCTag = cms.untracked.InputTag("gtStage2Digis","EtSumZDC") 
process.l1UpgradeTree.sumZDCToken = cms.untracked.InputTag("gtStage2Digis","EtSumZDC")

# l1 emulator sums
process.l1UpgradeEmuTree.sumZDCTag = cms.untracked.InputTag("etSumZdcProducer")
process.l1UpgradeEmuTree.sumZDCToken = cms.untracked.InputTag("etSumZdcProducer")

# do not change these settings
process.etSumZdcProducer = cms.EDProducer('L1TZDCProducer',
                                          hcalTPDigis = cms.InputTag("simHcalTriggerPrimitiveDigis"),
#                                          hcalTPDigis = cms.InputTag("hcalDigis"),
                                          bxFirst = cms.int32(-2),
                                          bxLast = cms.int32(3)
)

#Via Hannah, for the simHcal collection
process.simHcalTriggerPrimitiveDigis.inputLabel = cms.VInputTag("hcalDigis", "hcalDigis:ZDC")
process.simHcalTriggerPrimitiveDigis.inputUpgradeLabel = cms.VInputTag("hcalDigis", "hcalDigis:ZDC")


process.etSumZdc = cms.Path(process.etSumZdcProducer)
process.schedule.append(process.etSumZdc)
#======================================================================


#UNCOMMENT HERE TO WORK WITH THE LATEST GREATEST
MassReplaceInputTag(process, new="rawDataRepacker", old="rawDataCollector")
