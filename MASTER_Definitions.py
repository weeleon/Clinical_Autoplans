# THIS IS THE MASTER DEFINITIONS FILE THAT SETS
# THE DEFAULT CONDITION FOR **ALL** AUTOPLANS
# IRRESPECTIVE OF GUI CLINICAL SETTINGS, RAYSTATION UNITS ARE ALWAYS **CGS**
# ie dose always in cGy, time always in seconds, distance always in cm
#
#
# For site-specific definitions look at the appropriate sub-definitions file
#
# For functions that are specific only to a single particular autoplan, look in the script
#
#
#
# ------- MASTER DEFINITIONS BEGIN
#
#
# DEFINE THE CT DENSITY TABLE NAME
densityConversionTable = 'CTAWP65673:120kV'
oncentraConversionTable = 'OEB CT Table'
#
#
# DEFINE AN EXTERNAL CONTOUR THRESHOLD LEVEL FOR SKIN AUTOSEGMENTATION
externalContourThreshold = -150
factoryContourThreshold = -250
#
#
# DEFINE THE STANDARD PLANNING AND PRESCRIPTION PARAMETERS
defaultLinac = 'ElektaAgility_v1' #standard linac beam model for dose planning
defaultDoseGrid = 0.25 #isotropic dose grid dimension in units of cm
defaultPhotonEn = 6 #standard photon beam modality in units of MV
defaultVmatGantryStart = 179.9
defaultVmatGantryStop = 180.1
defaultVmatGantryDir = 'CounterClockwise'
defaultTreatmentCouchAngle = 0.0
#
#
#
# GLOBAL DEFINITIONS OF ORGANS AT RISK
#
# COLOR CHARTS :
#---- see http://www.rapidtables.com/web/color/RGB_Color.htm
#
# --- Anal canal
analCanal = 'OR; Anal Canal'
colourAnalCanal = "0,204,0"
#
# --- Bladder
bladder = 'OR; Blaere'
colourBladder = "0,172,128"
#
# --- bowels
bowel = 'OR; Tarm'
colourBowel = "0,176,0"
#
# --- skin (external)
external = 'External'
colourExternal = "255,173,91"
#
# --- femoral heads
femHeadLeft = 'OR; Cap fem sin'
femHeadRight = 'OR; Cap fem dex'
colourCaputFemori = "0,66,0"
#
# --- Penile bulb
penileBulb = 'OR; Bulbus penis'
colourBulbusPenis = "128,255,128"
#
# --- rectum
rectum = 'OR; Rectum'
colourRectum = "0,102,51"
#
# --- os sacrum
sacrum = 'OR; Os sacrum'
colourOsSacrum = "0,66,0"
#
# --- testes
testes = 'OR; Testis'
colourTestes = "24,192,128"
#
# --- carbon fibre couch model
pelvicCouchModel = 'ContesseCouch-Pelvine'
#
# --- help structures
colourComplementExternal = "192,192,192"
colourWallStructures = "0,200,255"
#
# --- clinical tumour volume
ctvT = 'CTV-T'
colourCtvT = "255,128,128"
#
# --- planning tumour volume
ptvT = 'PTV-T'
colourPtvT = "202,203,249"
#
#
#
# IMPORTANT - MODIFY WITH CAUTION - STANDARD FUNCTIONS FOR MASTER AUTOPLANNING WORKFLOW
# ===============================================================================
#
# Utility function to retrieve a unique plan name in a given case
# Raystation standard
def UniquePlanName(name, cas):
  for p in cas.TreatmentPlans:
    if name == p.Name:
      name = name + '_1'
      name = UniquePlanName(name, cas)
  return name
#
#
# Utility function that loads a plan and beam set into GUI
# Raystation standard
def LoadPlanAndBeamSet(patient, plan, beamset):
  # load plan
  planFilter = {"Name":plan.Name}
  planInfos = patient.QueryPlanInfo(Filter = planFilter)
  if len(planInfos) != 1:
    raise Exception('Failed plan query (nr of plan infos = {0})'.format(len(planInfos)))
  patient.LoadPlan(PlanInfo = {"Name": "^" + plan.Name + "$"})
  # load beam set  
  beamsetInfos = plan.QueryBeamSetInfo(Filter = {"Name":beamset.DicomPlanLabel})
  if len(beamsetInfos) != 1:
    raise Exception('Failed beam set query (nr of beam set infos = {0})'.format(len(beamsetInfos)))
  plan.LoadBeamSet(BeamSetInfo = beamsetInfos[0])
  # end LoadPlanAndBeamSet
#
#
# Utility function to locate the index position of 'matl' in the materials list 'mlist'
# used to search for presence and index of user-defined material overrides
def IndexOfMaterial(mlist,matl):
	mindex = -1 # if the material is not found in the list then it return a negative value
	mi = 0
	for m in mlist:
		if m.Name == matl:
			mindex = mi
		mi = mi + 1
	return mindex
#
#
#
#
def Create3DWallOrgan(pm,exam,sourceRoi,targetRoi,targetColour,inMargin,outMargin):
# generic function that creates a 3D donut structure from sourceRoi
# outputs results as targetRoi of default type Organ and set colour targetColour
# contract inwards with an isotropic 3D margin of inMargin >= 0
# and expand outwards with an isotropic 3D margin of outMargin >= 0
	try:
		pm.CreateRoi(Name=targetRoi, Color=targetColour, Type="Organ", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[targetRoi].SetWallExpression(SourceRoiName=sourceRoi, OutwardDistance=outMargin, InwardDistance=inMargin)
		pm.RegionsOfInterest[targetRoi].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to generate '+targetRoi+'. Continues...'
#procedure Create3DWallOrgan ends
#
#
def CreateIsotropicExpansionType(pm,exam,sourceRoi,targetRoi,targetColour,targetType,outMargin):
# generic function that creates a 3D isotropic expansion from sourceRoi
# saves the output as targetRoi of type targetType
# and assigns the colour targetColour to the resulting structure
# with the isotropic margin of outMargin >= 0
# e.g. CreateIsotropicExpansionType(pm,exam,ctvT,ptvT,colourPtvT,"PTV",1.0) creates a 1cm margin for PTV-T around CTV-T
	try :
		pm.CreateRoi(Name=targetRoi, Color=targetColour, Type=targetType, TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[targetRoi].SetMarginExpression(SourceRoiName=sourceRoi, MarginSettings={ 'Type': "Expand", 'Superior': outMargin, 'Inferior': outMargin, 'Anterior': outMargin, 'Posterior': outMargin, 'Right': outMargin, 'Left': outMargin })
		pm.RegionsOfInterest[targetRoi].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create '+targetRoi+'. Continues...'
#procedure CreateIsotropicExpansionType ends
#
#
def CreateAnisotropicExpansionType(pm,exam,sourceRoi,targetRoi,targetColour,targetType,sMargin,iMargin,aMargin,pMargin,rMargin,lMargin):
# generic function that creates a **nonuniform** 3D expansion from sourceRoi
# saves the output as targetRoi of type targetType
# and assigns the colour targetColour to the resulting structure
# with the isotropic margin of each of s,i,a,p,r and lMargin >= 0
# e.g. CreateAnisotropicExpansionType(pm,exam,ctvT,ptvT,colourPtvT,"PTV",1.0,1.0,0.7,0.7,0.7,0.7)
	try :
		pm.CreateRoi(Name=targetRoi, Color=targetColour, Type=targetType, TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[targetRoi].SetMarginExpression(SourceRoiName=sourceRoi, MarginSettings={ 'Type': "Expand", 'Superior': sMargin, 'Inferior': iMargin, 'Anterior': aMargin, 'Posterior': pMargin, 'Right': rMargin, 'Left': lMargin })
		pm.RegionsOfInterest[targetRoi].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create '+targetRoi+'. Continues...'
#procedure CreateAnisotropicExpansionType ends
#
#
def CreateSimpleUnionType(pm,exam,targetRoi,targetColour,targetType,sourceA,sourceB):
# generic function that creates a **simple** union of two sources
# saves the output as targetRoi of type targetType with no additional post-union processing
# and assigns the colour targetColour to the resulting structure
# e.g. CreateSimpleUnionType(pm,exam,ptvTSV,colourPtvTSV,"PTV",ptvT,ptvSV) creates a PTV-TSV
	try:
		pm.CreateRoi(Name=targetRoi, Color=targetColour, Type=targetType, TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[targetRoi].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [sourceA], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [sourceB], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[targetRoi].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create '+targetRoi+'. Continues ...'
#procedure CreateSimpleUnionType ends
#
#
def CreateSimpleSubtractionType(pm,exam,targetRoi,targetColour,targetType,sourceA,sourceB):
# generic function that creates a **simple** subtraction of two sources i.e. A minus B
# saves the output as targetRoi of type targetType with no additional post-subtraction processing
# and assigns the colour targetColour to the resulting structure
# e.g. CreateSimpleSubtractionType(pm,exam,complementBladderPtvT,colourBladder,"Organ",bladder,ptvT) creates OR; Blaere-(PTV-T)
	try:
		pm.CreateRoi(Name=targetRoi, Color=targetColour, Type=targetType, TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[targetRoi].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [sourceA], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [sourceB], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[targetRoi].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create '+targetRoi+'. Continues ...'
#procedure CreateSimpleSubtractionType ends
#
#
def CreateSimpleIntersectionType(pm,exam,targetRoi,targetColour,targetType,sourceA,sourceB):
# generic function that creates a **simple** intersection of two sources i.e. A intersect B
# saves the output as targetRoi of type targetType with no additional post-intersection processing
# and assigns the colour targetColour to the resulting structure
	try:
		pm.CreateRoi(Name=targetRoi, Color=targetColour, Type=targetType, TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[targetRoi].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [sourceA], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [sourceB], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
			ResultOperation="Intersection", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[targetRoi].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create '+targetRoi+'. Continues ...'
#procedure CreateSimpleIntersectionType ends
#
#
def MarginSubtractionType(pm,exam,targetRoi,targetColour,targetType,sourceA,marginA,sourceB,marginB):
# generic function that creates a **complementary structure with margin(s)** i.e. (A+marginA) - (B+marginB)
# saves the output as targetRoi of type targetType with no additional post-subtraction processing
# and assigns the colour targetColour to the resulting structure
# used for complementary help volumes such as Blaere-(PTV-T+5mm) etc etc
# or SIB transition targets eg PTV-E-(PTV-TSV+5mm) etc etc
	try:
		pm.CreateRoi(Name=targetRoi, Color=targetColour, Type=targetType, TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[targetRoi].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [sourceA], 'MarginSettings': { 'Type': "Expand", 'Superior': marginA, 'Inferior': marginA, 'Anterior': marginA, 'Posterior': marginA, 'Right': marginA, 'Left': marginA } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [sourceB], 'MarginSettings': { 'Type': "Expand", 'Superior': marginB, 'Inferior': marginB, 'Anterior': marginB, 'Posterior': marginB, 'Right': marginB, 'Left': marginB } },
			ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[targetRoi].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create '+targetRoi+'. Continues ...'
#procedure MarginSubtractionType ends
#
#
def IsotropicExpansionClipSkinType(pm,exam,sourceRoi,sourceMargin,targetRoi,targetColour,targetType,skin,skinMargin):
# generic function that creates a **complementary structure with margin(s)** i.e. (A+marginA) - (B+marginB)
# saves the output as targetRoi of type targetType with no additional post-subtraction processing
# and assigns the colour targetColour to the resulting structure
# used for complementary help volumes such as Blaere-(PTV-T+5mm) etc etc
# or SIB transition targets eg PTV-E-(PTV-TSV+5mm) etc etc
	try :
		pm.CreateRoi(Name=targetRoi, Color=targetColour, Type=targetType, TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[targetRoi].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [skin], 'MarginSettings': { 'Type': "Contract", 'Superior': skinMargin, 'Inferior': skinMargin, 'Anterior': skinMargin, 'Posterior': skinMargin, 'Right': skinMargin, 'Left': skinMargin } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [sourceRoi], 'MarginSettings': { 'Type': "Expand", 'Superior': sourceMargin, 'Inferior': sourceMargin, 'Anterior': sourceMargin, 'Posterior': sourceMargin, 'Right': sourceMargin, 'Left': sourceMargin } },
			ResultOperation="Intersection", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[targetRoi].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create '+targetRoi+'. Continues ...'
#procedure IsotropicExpansionClipSkinType ends
















