
# DEFINE THE CT DENSITY TABLE NAME
densityConversionTable = 'CTAWP65673:120kV'
oncentraConversionTable = 'OEB CT Table'


# DEFINE AN EXTERNAL CONTOUR THRESHOLD LEVEL FOR AUTOSEGMENTATION
externalContourThreshold = -150
factoryContourThreshold = -250


# DEFINE A MANDATORY SET OF INITIAL STRUCTURES
# ------ PLAN NEEDS TO HAVE THESE STRUCTURES DEFINED BEFORE EXECUTING THE AUTOPLAN SCRIPT
ctvT = 'CTV-T' #there must be one CTV-T
itvT = 'ITV-T' #there must be one ITV-T
ctvE = 'CTV-E' #there must be one CTV-E even if it has zero volume
itvE = 'ITV-E' #there must be one CTV-E even if it has zero volume
bladder = 'OR; Blaere'
bowel = 'OR; Tarm'
sacrum = 'OR; Os sacrum'
pelvicCouchModel = 'ContesseCouch-Pelvine'


# DEFINE A STANDARD SET OF ANATOMICAL STRUCTURE NAMES
external = 'External'
femHeadLeft = 'OR; Cap fem sin'
femHeadRight = 'OR; Cap fem dex'
ptvT = 'PTV-T'
ptvP = 'PTV-P'
ptvE = 'PTV-E'
testes = 'OR; Testis' #may or may not exist
penileBulb = 'OR; Bulbus penis' #may or may not exist
vagina = 'OR; Vagina' #may or may not exist
ctvP = 'CTV-P' #may or may not exist
itvP = 'ITV-P' #may or may not exist


# DEFINE A STANDARD SET OF STRUCTURE COLOURS
# colour codes imported from Oncentra
#---- see for example colour charts at http://www.rapidtables.com/web/color/RGB_Color.htm
colourExternal = "255,173,91"
colourCtvT = "255,128,128"
colourCtvP = "230,149,134"
colourCtvE = "255,81,81"
colourItv = "0,0,220"
colourPtvT = "202,203,249"
colourPtvP = "112,102,232"
colourPtvE = "126,130,239"
colourBladder = "0,172,128"
colourBulbusPenis = "128,255,128"
colourCaputFemori = "0,66,0"
colourBowel = "0,176,0"
colourTestes = "24,192,128"
colourVagina = "128,0,128"

colourComplementExternal = "192,192,192"
colourWallStructures = "0,200,255"


# DEFINE A SET OF PLANNING HELP STRUCTURES
wall5mmPtvT = 'Wall; PTV-T+5mm'
wall8mmPtvT = 'Wall; PTV-T+8mm'
wall5mmPtvTSV = 'Wall; PTV-TSV+5mm'
wall8mmPtvTSV = 'Wall; PTV-TSV+8mm'
wall5mmPtvE = 'Wall; PTV-E+5mm'
wall8mmPtvE = 'Wall; PTV-E+8mm'

transitionTPtoE = 'PTV-E-(PTV-T+5mm)'

complementExt5mmPtvT = 'Ext-(PTV-T+5mm)'
complementExt5mmPtvTSV = 'Ext-(PTV-TSV+5mm)'
complementExt5mmPtvE = 'Ext-(PTV-E+5mm)'
complementExt8mmPtvTSV = 'Ext-(PTV-TSV+8mm)'
complementExt8mmPtvE = 'Ext-(PTV-E+8mm)'


# DEFINE THE STANDARD PLANNING AND PRESCRIPTION PARAMETERS
defaultLinac = 'ElektaAgility_v1' #standard linac beam model for dose planning
defaultDoseGrid = 0.25 #isotropic dose grid dimension
defaultPhotonEn = 6 #standard photon beam modality in units of MV


# DEFINE THE STANDARD TEMPLATES AND OPTIMIZATION FUNCTIONS
defaultClinicalGoalsRect62 = 'Recti_62Gy_Clinical_Goals_Template'
# 
defaultOptimVmatRect62 = 'Recti_62Gy_VMAT_2arc_Optimization'



# IMPORTANT - MODIFY WITH CAUTION - STANDARD PROCEDURES FOR AUTOPLANNING WORKFLOW
# ===============================================================================

def CreateMarginPtvT(pm,exam):
# 1) create 3 mm isotropic expansion of ITV-T
	#PTV-T
	try :
		pm.CreateRoi(Name=ptvT, Color=colourPtvT, Type="PTV", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[ptvT].SetMarginExpression(SourceRoiName=itvT, MarginSettings={ 'Type': "Expand", 'Superior': 0.3, 'Inferior': 0.3, 'Anterior': 0.3, 'Posterior': 0.3, 'Right': 0.3, 'Left': 0.3 })
		pm.RegionsOfInterest[ptvT].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create PTV-T. Continues...'
#procedure CreateMarginPtvT ends

def CreateMarginPtvP(pm,exam):
# 2) create 5 mm isotropic expansion of ITV-P but clip away 5mm from skin
	#PTV-P
	try :
		pm.CreateRoi(Name=ptvP, Color=colourPtvP, Type="PTV", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[ptvP].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [external], 'MarginSettings': { 'Type': "Contract", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [itvP], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
			ResultOperation="Intersection", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[ptvP].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create PTV-P. Continues...'
#procedure CreateMarginPtvP ends

def CreateMarginPtvE(pm,exam):
# 3) create 3 mm isotropic expansion of ITV-E but clip away 5mm from skin
	#PTV-E
	try :
		pm.CreateRoi(Name=ptvE, Color=colourPtvE, Type="PTV", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[ptvE].SetAlgebraExpression(
			ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [external], 'MarginSettings': { 'Type': "Contract", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
			ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [itvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.3, 'Inferior': 0.3, 'Anterior': 0.3, 'Posterior': 0.3, 'Right': 0.3, 'Left': 0.3 } },
			ResultOperation="Intersection", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[ptvE].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create PTV-E. Continues...'
#procedure CreateMarginPtvE ends

def CreateTransitionTPtoE(pm,exam,r):
# 4) transition zone between PTV-(T+P) and PTV-E
# if PTV-P exists, then the transition structure PTV-E-(PTV-T+5mm) will contain
# the union of PTV-T and PTV-P .... else, the transition structure will only contain PTV-T
	#PTV-E-(PTV-T+5mm)
	try :
		pm.CreateRoi(Name=transitionTPtoE, Color=colourPtvE, Type="PTV", TissueName=None, RoiMaterial=None)
		try:
			r.RoiGeometries[ptvP].GetRoiVolume() #only works if PTV-P exists
			pm.RegionsOfInterest[transitionTPtoE].SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvT,ptvP], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		except Exception:
			pm.RegionsOfInterest[transitionTPtoE].SetAlgebraExpression(
				ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [ptvE], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
				ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [ptvT], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } },
				ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
		pm.RegionsOfInterest[transitionTPtoE].UpdateDerivedGeometry(Examination=exam)
	except Exception:
		print 'Failed to create PTV-E-(PTV-T+5mm). Continues...'
#procedure CreateTransitionTPtoE ends





# Utility function to locate the index position of 'matl' in the materials list 'mlist'
def IndexOfMaterial(mlist,matl):
	mindex = -1 # if the material is not found in the list then it return a negative value
	mi = 0
	for m in mlist:
		if m.Name == matl:
			mindex = mi
		mi = mi + 1
	return mindex


# Utility function to retrieve a unique plan name in a given case
def UniquePlanName(name, cas):
  for p in cas.TreatmentPlans:
    if name == p.Name:
      name = name + '_1'
      name = UniquePlanName(name, cas)
  return name


# Utility function that loads a plan and beam set into GUI
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




#CreateComplementBladderPtvT(patient.PatientModel,examination) #all prostate types
#CreateComplementRectumPtvT(patient.PatientModel,examination) #all prostate types
#CreateWallPtvT(patient.PatientModel,examination) #all prostate types
#CreateComplementExternalPtvT(patient.PatientModel,examination) #all prostate types

#CreateComplementBladderPtvTSV(patient.PatientModel,examination) #all prostate types except Type A
#CreateComplementRectumPtvTSV(patient.PatientModel,examination) #all prostate types except Type A
#CreateWallPtvTSV(patient.PatientModel,examination) #all prostate types except Type A
#CreateComplementExternalPtvTSV(patient.PatientModel,examination) #all prostate types except Type A

#CreateMarginPtvE(patient.PatientModel,examination) #only for Type N+
#CreateTransitionPtvTsvPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementPtvTsvPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementBladderPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementRectumPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementBowelPtvTSV(patient.PatientModel,examination) #only for Type N+
#CreateComplementBowelPtvE(patient.PatientModel,examination) #only for Type N+
#CreateWallPtvE(patient.PatientModel,examination) #only for Type N+
#CreateComplementExternalPtvE(patient.PatientModel,examination) #only for Type N+
