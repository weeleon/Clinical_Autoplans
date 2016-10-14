# set script environment
import math
from connect import *
import time
import sys
clr.AddReference("PresentationFramework")
from System.Windows import *

# set master definitions
from MASTER_Definitions import *

# set prostate-specific definitions
from RECTI_Definitions import *

# Define null filter
filter = {}

# Get handle to current patient database
patient_db = get_current('PatientDB')

# Define current patient, current case and current examination handles
patient = get_current('Patient')
examination = get_current('Examination')
case = get_current('Case')

# Define standard prescription level
defaultPrescDose = 6020 #the absolute prescribed dose in cGy
defaultFractions = 28 #standard number of fractions

# Define major handles
pm = case.PatientModel
rois = pm.StructureSets[examination.Name]
examinationName = examination.Name

#
#
#
#
#

#### ANAL CANCER PROTOCOL FOR T1 STAGE ONLY
#### 60.2Gy/28F Normo-fractionated prescribed to PTV-(T)
#### Implemented as a single arc VMAT solution

#
#
#
#
#

# --- the plan shall NOT be made without the following required Rois
RequiredRois = [ctvT, itvT, bladder, bowel, sacrum, pelvicCouchModel]

# --- the following ROIs may or may not exist, but if they do exist they must have finite volume
VariableRois = [testes, penileBulb, vagina]

# --- the script shall REGENERATE each of the following Rois each time therefore if they already exist, delete first
ScriptedRois = [external, femHeadLeft, femHeadRight, ptvT, wall5mmPtvT, complementExt5mmPtvT]

#the following structures are excluded from DICOM export to the linear acc to help the nurses
ExcludedRois = [wall5mmPtvT, complementExt5mmPtvT]

#the following ROIs are generated as intermediate processes, and should be removed before running the script
TemporaryRois = ['temp_ext', 'supports', 'temp_wall']

#
#
#
#---------- auto-generate a unique plan name if the desired name already exists
planName = 'AniT1_60_28'
planName = UniquePlanName(planName, case)
#
beamSetPrimaryName = planName #prepares a single CC arc VMAT for the primary field
beamArcPrimaryName = 'A1'
examinationName = examination.Name



# Define the workflow for the autoplan step
# 1. Confirm that all mandatory structures exist and have non-zero volumes
# 2. Assign correct CT to Density Table
# 3. (Not applicable) Density overrides
# 4. Grow all required volumes and conformity structures
# 5. Create new plan with unique name
# 6. Create first beam set
# 7. Set default dose grid
# 8. Load beam(s) list
# 9. Load clinical goals list
# 10. Load cost functions list
# 11. Load optimization settings
# 12. Optimization first-run
# 13. Compute full dose



# 1. Check structure set and user has set a localization point
#
# - confirm that the required rois for autoplanning have been drawn
minVolume = 1 #at least 1cc otherwise the ROI does not make sense or might be empty
for r in RequiredRois:
	try :
		v = rois.RoiGeometries[r].GetRoiVolume()
		if v < minVolume :
			raise Exception('The volume of '+r+' seems smaller than required ('+minVolume+'cc).')
	except Exception :
		raise Exception('Please check structure set : '+r+' does not exist.')
#
numEmpty = 0
for rg in rois.RoiGeometries:
	for v in VariableRois:
		if (rg.OfRoi.Name == v):
			if ( rg.HasContours() ):
				print 'Structure '+v+' exists and has contours.'
			else:
				numEmpty = numEmpty + 1
if (numEmpty > 0):
	raise Exception('Some optional structures are currently defined, that have no contours!')
#
for sr in ScriptedRois:
	try:
		pm.RegionsOfInterest[sr].DeleteRoi()
		print 'Deleted - scripting will be used to generate fresh '+sr+'.'
	except Exception:
		print 'Scripting will be used to generate '+sr+'.'
#
for sr in TemporaryRois:
	try:
		pm.RegionsOfInterest[sr].DeleteRoi()
		print 'Deleted - scripting will be used to generate fresh '+sr+'.'
	except Exception:
		print 'Scripting will be used to generate '+sr+'.'
#
numLP = 0
for lp in pm.PointsOfInterest:
	if (lp.Type == 'LocalizationPoint'):
		numLP = numLP + 1
if (numLP < 1):
	raise Exception('No localization point defined - please define using POI Tools.')


# 2. Assign CT Density Table
# OVERWRITE current simulation modality to the REQUIRED density table name
try:
	examination.EquipmentInfo.SetImagingSystemReference(ImagingSystemName = densityConversionTable)
except Exception:
	print 'Failed to find matching name in list of commissioned CT scanners'


# 3. (Not applicable) Density overrides


# 4. Grow all required structures from the initial set
# --------- EXTERNAL will be set using threshold contour generate at the user-defined intensity value
pm.CreateRoi(Name='temp_ext', Color="Orange", Type="External", TissueName=None, RoiMaterial=None)
pm.RegionsOfInterest['temp_ext'].CreateExternalGeometry(Examination=examination, ThresholdLevel=externalContourThreshold)
#
#the above temporary external typically includes bit of sim couch therefore the true
#External needs to be generated from the temp external
pm.CreateRoi(Name=external, Color="Orange", Type="Organ", TissueName=None, RoiMaterial=None)
pm.RegionsOfInterest[external].SetAlgebraExpression(
		ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['temp_ext'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
		ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [pelvicCouchModel], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
		ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
pm.RegionsOfInterest[external].UpdateDerivedGeometry(Examination=examination)
pm.RegionsOfInterest[external].SetAsExternal()
#
#then remove the temporary external
pm.RegionsOfInterest['temp_ext'].DeleteRoi()
#
#and simplify straggly bits of the remaining true External
rois.SimplifyContours(RoiNames=[external], RemoveHoles3D='False', RemoveSmallContours='True', AreaThreshold=10, ReduceMaxNumberOfPointsInContours='False', MaxNumberOfPoints=None, CreateCopyOfRoi='False')
#
# ---------- FEMORALS HEADS will be approximated using built-in MALE PELVIS Model Based Segmentation
#get_current("ActionVisibility:Internal") # needed due to that MBS actions not visible in evaluation version.
pm.MBSAutoInitializer(MbsRois=[
	{ 'CaseType': "PelvicMale", 'ModelName': "FemoralHead (Left)", 'RoiName': femHeadLeft, 'RoiColor': colourCaputFemori }, 
	{ 'CaseType': "PelvicMale", 'ModelName': "FemoralHead (Right)", 'RoiName': femHeadRight, 'RoiColor': colourCaputFemori }],
	CreateNewRois=True, Examination=examination, UseAtlasBasedInitialization=True)
pm.AdaptMbsMeshes(Examination=examination, RoiNames=[femHeadLeft, femHeadRight], CustomStatistics=None, CustomSettings=None)
#
# ---------- GROW ALL REQUIRED PTVs
#
# PTV-T is a 3mm iso expansion from ITV-T
#CreateIsotropicExpansionType(pm,exam,sourceRoi,targetRoi,targetColour,targetType,outMargin):
CreateIsotropicExpansionType(pm,examination,itvT,ptvT,colourPtvT,"PTV",0.3)
#
#
# ---------- GROW WALL STRUCTURES
#
# --- temporary wall structure which is a 5mm donut around PTV-T
#Create3DWallOrgan(pm,exam,sourceRoi,targetRoi,targetColour,inMargin,outMargin):
Create3DWallOrgan(pm,examination,ptvT,'temp_wall',colourWallStructures,0.0,0.5)
#
# --- clip the temporary donut to exactly the skin contour
#IsotropicExpansionClipSkinType(pm,exam,sourceRoi,sourceMargin,targetRoi,targetColour,targetType,skin,skinMargin):
IsotropicExpansionClipSkinType(pm,examination,'temp_wall',0.0,wall5mmPtvT,colourWallStructures,"Organ",external,0.0)
#
# --- now delete the temporary donut structure
try:
	pm.RegionsOfInterest['temp_wall'].DeleteRoi()
except Exception:
	print 'Failed to remove temp-wall. Continues ...'
#
# ---------- GROW COMPLEMENTARY EXTERNAL STRUCTURES
#MarginSubtractionType(pm,exam,targetRoi,targetColour,targetType,sourceA,marginA,sourceB,marginB):
MarginSubtractionType(pm,examination,complementExt5mmPtvT,colourComplementExternal,"Organ",external,0.0,ptvT,0.5)
#
#
#-------------- Exclude help rois used only for planning and optimization from dicom export
for e in ExcludedRois:
	try :
		rois.RoiGeometries[e].OfRoi.ExcludeFromExport = 'True'
	except Exception :
		raise Exception('Please check structure set : '+e+' cannot be excluded from DCM export.')
# ------------- ANATOMY PREPARATION COMPLETE
# --------- save the active plan
patient.Save()


#
# ------------- AUTO VMAT PLAN CREATION
#

# 5 - 7. Define unique plan, beamset and dosegrid
# --------- Setup a standard VMAT protocol plan
with CompositeAction('Adding plan with name {0} '.format(planName)):
    # add plan
    plan = case.AddNewPlan(PlanName=planName, Comment="Single-arc Ani VMAT ", ExaminationName=examinationName)
	# set standard dose grid size
    plan.SetDefaultDoseGrid(VoxelSize={'x':defaultDoseGrid, 'y':defaultDoseGrid, 'z':defaultDoseGrid})
	# set the dose grid size to cover
    # add only one beam set
    beamSetArc1 = plan.AddNewBeamSet(Name = beamSetPrimaryName, ExaminationName = examinationName,
		MachineName = defaultLinac, Modality = "Photons", TreatmentTechnique = "VMAT",
		PatientPosition = "HeadFirstSupine", NumberOfFractions = defaultFractions, CreateSetupBeams = False)


# Load the current plan and beamset into the system
LoadPlanAndBeamSet(case, plan, beamSetArc1)


# 8. Create beam list
with CompositeAction('Create arc beam'):
	# ----- no need to add prescription for dynamic delivery
	beamSetArc1.AddDosePrescriptionToRoi(RoiName = ptvT, PrescriptionType="DoseAtVolume", DoseVolume=99, DoseValue = 5719, RelativePrescriptionLevel = 1, AutoScaleDose='False')
	#
	# ----- set the plan isocenter to the centre of the reference ROI
	isocenter = pm.StructureSets[examinationName].RoiGeometries[ptvT].GetCenterOfRoi()
	isodata = beamSetArc1.CreateDefaultIsocenterData(Position={'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
	beamSetArc1.CreateArcBeam(Name=beamArcPrimaryName, Description=beamArcPrimaryName, Energy=defaultPhotonEn, CouchAngle=defaultTreatmentCouchAngle, GantryAngle=defaultVmatGantryStart, ArcStopGantryAngle=defaultVmatGantryStop, ArcRotationDirection=defaultVmatGantryDir, CollimatorAngle = defaultRectiCollAngle, IsocenterData = isodata)
#
patient.Save()


# 9. Set a predefined template directly from the clinical database for v.5.0.2
plan.TreatmentCourse.EvaluationSetup.ApplyClinicalGoalTemplate(Template=patient_db.TemplateTreatmentOptimizations[defaultClinicalGoalsRect60])


# 10. import optimization functions from a predefined template
plan.PlanOptimizations[0].ApplyOptimizationTemplate(Template=patient_db.TemplateTreatmentOptimizations[defaultOptimVmatRect60])


# 11. set opt parameters and run first optimization for the VMAT plan
optimPara = plan.PlanOptimizations[0].OptimizationParameters #shorter handle
SetVmatOptimizationParameters(optimPara)


# 12. Execute optimization with warmstarts and final dose (as set above in opt settings)
for w in range(2):
	plan.PlanOptimizations[0].RunOptimization()	


# 13. compute final dose not necessary due to optimization setting
#beamSetArc1.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="CCDose", ForceRecompute=False)


bNum = 1
# set beam number(s)
for b in beamSetArc1.Beams :
	b.Number = bNum
	bNum = bNum + 1

# Save VMAT auto-plan result
patient.Save()


# NOT ACTIVATED :
# ------------- AUTO IMRT FALLBACK PLAN CREATION
# 
# 5 - 7. Define unique plan, beamset and dosegrid
# ---------- redefine the plan name parameter
# planName = 'Ani60_28_fb'
# planName = UniquePlanName(planName, case)
# 
# beamSetPrimaryName = planName #prepares a standard 8-fld StepNShoot IMRT
# examinationName = examination.Name
# 
# --------- Setup a standard IMRT protocol plan
# with CompositeAction('Adding plan with name {0} '.format(planName)):
#     add plan
#     plan = case.AddNewPlan(PlanName=planName, Comment="8-fld SMLC Ani IMRT ", ExaminationName=examinationName)
# 	set standard dose grid size
#     plan.SetDefaultDoseGrid(VoxelSize={'x':defaultDoseGrid, 'y':defaultDoseGrid, 'z':defaultDoseGrid})
# 	set the dose grid size to cover
#     add only one beam set
#     beamSetImrt = plan.AddNewBeamSet(Name = beamSetPrimaryName, ExaminationName = examinationName,
# 		MachineName = defaultLinac, Modality = "Photons", TreatmentTechnique = "SMLC",
# 		PatientPosition = "HeadFirstSupine", NumberOfFractions = defaultFractions, CreateSetupBeams = False)
# 
# 
# Load the current plan and beamset into the system
# LoadPlanAndBeamSet(case, plan, beamSetImrt)
# 
# 	
# 8. Create beam list
# with CompositeAction('Create StepNShoot beams'):
# 	----- no need to add prescription for dynamic delivery
# 	beamSetImrt.AddDosePrescriptionToRoi(RoiName = ptvT, PrescriptionType="DoseAtVolume", DoseVolume=99, DoseValue = 5719, RelativePrescriptionLevel = 1, AutoScaleDose='False')
# 	
# 	----- set the plan isocenter to the centre of the reference ROI
# 	isocenter = pm.StructureSets[examinationName].RoiGeometries[ptvE].GetCenterOfRoi()
# 	isodata = beamSetImrt.CreateDefaultIsocenterData(Position={'x':isocenter.x, 'y':isocenter.y, 'z':isocenter.z})
# 	add 7 static IMRT fields around the ROI-based isocenter
# 	beamSetImrt.CreatePhotonBeam(Name = 'G180A', Description = 'G180A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 180, CollimatorAngle = 0, IsocenterData = isodata)
# 	beamSetImrt.CreatePhotonBeam(Name = 'G140A', Description = 'G140A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 140, CollimatorAngle = 15, IsocenterData = isodata)
# 	beamSetImrt.CreatePhotonBeam(Name = 'G085A', Description = 'G085A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 85, CollimatorAngle = 345, IsocenterData = isodata)
# 	beamSetImrt.CreatePhotonBeam(Name = 'G030A', Description = 'G030A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 30, CollimatorAngle = 45, IsocenterData = isodata)
# 	beamSetImrt.CreatePhotonBeam(Name = 'G220A', Description = 'G220A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 220, CollimatorAngle = 345, IsocenterData = isodata)
# 	beamSetImrt.CreatePhotonBeam(Name = 'G275A', Description = 'G275A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 275, CollimatorAngle = 15, IsocenterData = isodata)
# 	beamSetImrt.CreatePhotonBeam(Name = 'G330A', Description = 'G330A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 330, CollimatorAngle = 315, IsocenterData = isodata)
# 	beamSetImrt.CreatePhotonBeam(Name = 'G000A', Description = 'G000A', Energy=defaultPhotonEn, CouchAngle = 0, GantryAngle = 0, CollimatorAngle = 0, IsocenterData = isodata)
# 
# 
# patient.Save()
# 
# 
# 9. Set a predefined template directly from the clinical database for v.5.0.2
# plan.TreatmentCourse.EvaluationSetup.ApplyClinicalGoalTemplate(Template=patient_db.TemplateTreatmentOptimizations[defaultClinicalGoalsRect62])
# 
# 10. import optimization functions from a predefined template
# plan.PlanOptimizations[0].ApplyOptimizationTemplate(Template=patient_db.TemplateTreatmentOptimizations[defaultOptimVmatRect62])
# 
# 11. set opt parameters and run first optimization for the IMRT plan
# optimPara = plan.PlanOptimizations[0].OptimizationParameters #shorter handle
# SetImrtOptimizationParameters(optimPara)
# 
# 
# 12. Execute first run optimization with final dose (as set above in opt settings)
# plan.PlanOptimizations[0].RunOptimization()
# one more as warm start
# plan.PlanOptimizations[0].RunOptimization()
# 
# 13. compute final dose not necessary due to optimization setting
# beamSetImrt.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="CCDose", ForceRecompute=False)
# 
# set fallback beam number(s)
# bNum = 11
# for b in beamSetImrt.Beams :
# 	b.Number = bNum
# 	bNum = bNum + 1
# 
# 
# Save IMRT auto-plan result
# patient.Save()
# 
# 

#end of AUTOPLAN





