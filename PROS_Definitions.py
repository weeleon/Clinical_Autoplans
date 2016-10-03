# DEFINE A SUPPLEMENTARY SET OF STRUCTURES TO EXTEND MASTER
#
# COLOR CHARTS :
#---- see http://www.rapidtables.com/web/color/RGB_Color.htm
#
#
# --- clinical tumour volume seminal vesicles
ctvSV = 'CTV-SV'
colourCtvSV = "230,149,134"
#
# --- planning tumour volume seminal vesicles
ptvSV = 'PTV-SV'
colourPtvSV = "112,102,232"
#
# --- combined tumour and seminal vesicles PTV
ptvTSV = 'PTV-TSV'
colourPtvTSV = "202,203,249"
#
# --- elective pelvic lymph nodes for whole-pelvis irradiation
ctvE = 'CTV-E'
colourCtvE = "255,81,81"
#
ptvE = 'PTV-E'
colourPtvE = "126,130,239"
#
# --- summated tumour PTVs
ptvTSVE = 'PTV-(T+SV+E)'
colourPtvTSVE = colourPtvE
#
# --- combined elective vesicles and lymph nodes
ptvSVE = 'PTV-(SV+E)'
colourPtvSVE = colourPtvTSV
#
# --- fiducial markers
fiducial1 = 'S1' #does not exist for salvage cases
marker1 = 'Mark1'
colourMarker1 = "0,255,255"
#
fiducial2 = 'S2' #does not exist for salvage cases
marker2 = 'Mark2'
colourMarker2 = "255,128,255"
#
fiducial3 = 'S3' #does not exist for salvage cases
marker3 = 'Mark3'
colourMarker3 = "0,255,0"
#
fiducial4 = 'S4' #may or may not exist for any prostate plan
marker4 = 'Mark4'
colourMarker4 = "255,255,0"
#
fiducial5 = 'S5' #may or may not exist for any prostate plan
marker5 = 'Mark5'
colourMarker5 = "0,0,255"
#
fiducial6 = 'S6' #may or may not exist for any prostate plan
marker6 = 'Mark6'
colourMarker6 = "128,0,255"
#
# --- rectum expansion/contraction help volume for therapists
hvRect = 'HV-Rectum'
colourHvRect = "red"
#
# --- target volume transitions for elective irradiation
transitionTSVtoE = 'PTV-E-(PTV-TSV+8mm)'
transitionTtoSVE = 'PTV-(SV+E)-(PTV-T+8mm)'
#
# --- wall structures for dose conformality shaping
wall5mmPtvT = 'Wall; PTV-T+5mm'
wall8mmPtvT = 'Wall; PTV-T+8mm'
wall5mmPtvTSV = 'Wall; PTV-TSV+5mm'
wall8mmPtvTSV = 'Wall; PTV-TSV+8mm'
wall5mmPtvE = 'Wall; PTV-E+5mm'
wall8mmPtvE = 'Wall; PTV-E+8mm'
#
# --- complementary "external" structures outside targets for dose shaping
complementExt5mmPtvT = 'Ext-(PTV-T+5mm)'
complementExt5mmPtvTSV = 'Ext-(PTV-TSV+5mm)'
complementExt5mmPtvE = 'Ext-(PTV-E+5mm)'
complementExt8mmPtvTSV = 'Ext-(PTV-TSV+8mm)'
complementExt8mmPtvE = 'Ext-(PTV-E+8mm)'
#
#
#
# not typically as standard for inverse planning in Raystation
#complementPtvEofTSV = 'PTV-E-(PTV-TSV)'
#complementBladderPtvT = 'OR; Blaere-(PTV-T+5mm)'
#complementBladderPtvTSV = 'OR; Blaere-(PTV-TSV+5mm)'
#complementBladderPtvE = 'OR; Blaere-(PTV-E+5mm)'
#complementRectumPtvT = 'OR; Rectum-(PTV-T+5mm)'
#complementRectumPtvTSV = 'OR; Rectum-(PTV-TSV+5mm)'
#complementRectumPtvE = 'OR; Rectum-(PTV-E+5mm)'
#complementBowelPtvTSV = 'OR; Tarm-(PTV-TSV+5mm)'
#complementBowelPtvE = 'OR; Tarm-(PTV-E+5mm)'
#
#
# DEFINE THE STANDARD COLLIMATOR ANGLE FOR VMAT ARCS IN PROSTATE
defaultProstCollAngle = 45
#
#
# DEFINE THE STANDARD CLINICAL TEMPLATES FOR PLANNING OBJECTIVES
defaultClinicalGoalsProstC = 'ProstC_Clinical_Goals_Template'
defaultClinicalGoalsProstA = 'ProstA_Clinical_Goals_Template'
defaultClinicalGoalsProstS = 'ProstS_Clinical_Goals_Template'
defaultClinicalGoalsProstBPr = 'ProstBPr_Clinical_Goals_Template'
defaultClinicalGoalsProstBBo = 'ProstBBo_Clinical_Goals_Template'
defaultClinicalGoalsProstB = 'ProstB_Clinical_Goals_Template'
defaultClinicalGoalsProstD = 'ProstD_Clinical_Goals_Template'
defaultClinicalGoalsProstE = 'ProstE_Clinical_Goals_Template'
#
#
#
# DEFINE THE STANDARD CLINICAL TEMPLATES FOR OPTIMIZATION FUNCTIONS
defaultOptimVmatProstC = 'ProstC_VMAT_1arc_Optimization'
defaultOptimVmatProstA = 'ProstA_VMAT_1arc_Optimization'
defaultOptimVmatProstS = 'ProstS_VMAT_1arc_Optimization'
defaultOptimVmatProstBBo = 'ProstBBo_VMAT_1arc_Optimization'
defaultOptimVmatProstBPr = 'ProstBPr_VMAT_1arc_Optimization'
defaultOptimVmatProstD = 'ProstD_VMAT_2arc_Optimization'
defaultOptimVmatProstE = 'ProstE_VMAT_2arc_Optimization'
#
#
#
#
# prostate autoplans require a special function to manually override density adjacent to fiducials
#
def OverrideFiducialsDensity(pm,exam,i):
# 19) creation of density over-rides in concentric rings around a fiducial
	#fiducial number 1
	try:
		coord = pm.StructureSets[exam.Name].PoiGeometries[fiducial1].Point
		# --- set a new empty roi at this coordinate position
		pm.CreateRoi(Name='Temp1', Color="Fuchsia", Type="Marker", TissueName=None, RoiMaterial=None)
		# --- draw a 3mm spherical roi around the nominated poi
		pm.RegionsOfInterest['Temp1'].CreateSphereGeometry( Radius=0.3, Examination=exam, Center={'x':coord.x, 'y':coord.y, 'z':coord.z} )
		# --- draw a 7mm-wide wall region around the temporary roi
		pm.CreateRoi(Name=marker1, Color=colourMarker1, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[marker1].SetWallExpression(SourceRoiName='Temp1', OutwardDistance=0.7, InwardDistance=0)
		pm.RegionsOfInterest[marker1].UpdateDerivedGeometry(Examination=exam)
		# --- reset the density override in this region to the newly created material (index from args)
		pm.RegionsOfInterest[marker1].SetRoiMaterial(Material = pm.Materials[i])
	except Exception:
		print 'Failed to generate Marker_1 override ROI. Continues...'
	#no further need for the temporary structure
	try:
		pm.RegionsOfInterest['Temp1'].DeleteRoi()
	except Exception:
		print 'Error cleaning up marker 1 source ROI. Continues...'
	#
	#fiducial number 2
	try:
		coord = pm.StructureSets[exam.Name].PoiGeometries[fiducial2].Point
		# --- set a new empty roi at this coordinate position
		pm.CreateRoi(Name='Temp2', Color="Fuchsia", Type="Marker", TissueName=None, RoiMaterial=None)
		# --- draw a 3mm spherical roi around the nominated poi
		pm.RegionsOfInterest['Temp2'].CreateSphereGeometry( Radius=0.3, Examination=exam, Center={'x':coord.x, 'y':coord.y, 'z':coord.z} )
		# --- draw a 7mm-wide wall region around the temporary roi
		pm.CreateRoi(Name=marker2, Color=colourMarker2, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[marker2].SetWallExpression(SourceRoiName='Temp2', OutwardDistance=0.7, InwardDistance=0)
		pm.RegionsOfInterest[marker2].UpdateDerivedGeometry(Examination=exam)
		# --- reset the density override in this region to the newly created material (index from args)
		pm.RegionsOfInterest[marker2].SetRoiMaterial(Material = pm.Materials[i])
	except Exception:
		print 'Failed to generate Marker_2 override ROI. Continues...'
	#no further need for the temporary structure
	try:
		pm.RegionsOfInterest['Temp2'].DeleteRoi()
	except Exception:
		print 'Error cleaning up marker 2 source ROI. Continues...'
	#
	#fiducial number 3
	try:
		coord = pm.StructureSets[exam.Name].PoiGeometries[fiducial3].Point
		# --- set a new empty roi at this coordinate position
		pm.CreateRoi(Name='Temp3', Color="Fuchsia", Type="Marker", TissueName=None, RoiMaterial=None)
		# --- draw a 3mm spherical roi around the nominated poi
		pm.RegionsOfInterest['Temp3'].CreateSphereGeometry( Radius=0.3, Examination=exam, Center={'x':coord.x, 'y':coord.y, 'z':coord.z} )
		# --- draw a 7mm-wide wall region around the temporary roi
		pm.CreateRoi(Name=marker3, Color=colourMarker3, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[marker3].SetWallExpression(SourceRoiName='Temp3', OutwardDistance=0.7, InwardDistance=0)
		pm.RegionsOfInterest[marker3].UpdateDerivedGeometry(Examination=exam)
		# --- reset the density override in this region to the newly created material (index from args)
		pm.RegionsOfInterest[marker3].SetRoiMaterial(Material = pm.Materials[i])
	except Exception:
		print 'Failed to generate Marker_3 override ROI. Continues...'
	#no further need for the temporary structure
	try:
		pm.RegionsOfInterest['Temp3'].DeleteRoi()
	except Exception:
		print 'Error cleaning up marker 3 source ROI. Continues...'
	#
	#fiducial number 4 - might not exist
	try:
		coord = pm.StructureSets[exam.Name].PoiGeometries[fiducial4].Point
		# --- set a new empty roi at this coordinate position
		pm.CreateRoi(Name='Temp4', Color="Fuchsia", Type="Marker", TissueName=None, RoiMaterial=None)
		# --- draw a 3mm spherical roi around the nominated poi
		pm.RegionsOfInterest['Temp4'].CreateSphereGeometry( Radius=0.3, Examination=exam, Center={'x':coord.x, 'y':coord.y, 'z':coord.z} )
		# --- draw a 7mm-wide wall region around the temporary roi
		pm.CreateRoi(Name=marker4, Color=colourMarker4, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[marker4].SetWallExpression(SourceRoiName='Temp4', OutwardDistance=0.7, InwardDistance=0)
		pm.RegionsOfInterest[marker4].UpdateDerivedGeometry(Examination=exam)
		# --- reset the density override in this region to the newly created material (index from args)
		pm.RegionsOfInterest[marker4].SetRoiMaterial(Material = pm.Materials[i])
	except Exception:
		print 'Failed to generate Marker_4 override ROI. Continues...'
	#no further need for the temporary structure
	try:
		pm.RegionsOfInterest['Temp4'].DeleteRoi()
	except Exception:
		print 'Error cleaning up marker 4 source ROI. Continues...'
	#
	#fiducial number 5 - might not exist
	try:
		coord = pm.StructureSets[exam.Name].PoiGeometries[fiducial5].Point
		# --- set a new empty roi at this coordinate position
		pm.CreateRoi(Name='Temp5', Color="Fuchsia", Type="Marker", TissueName=None, RoiMaterial=None)
		# --- draw a 3mm spherical roi around the nominated poi
		pm.RegionsOfInterest['Temp5'].CreateSphereGeometry( Radius=0.3, Examination=exam, Center={'x':coord.x, 'y':coord.y, 'z':coord.z} )
		# --- draw a 7mm-wide wall region around the temporary roi
		pm.CreateRoi(Name=marker5, Color=colourMarker5, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[marker5].SetWallExpression(SourceRoiName='Temp5', OutwardDistance=0.7, InwardDistance=0)
		pm.RegionsOfInterest[marker5].UpdateDerivedGeometry(Examination=exam)
		# --- reset the density override in this region to the newly created material (index from args)
		pm.RegionsOfInterest[marker5].SetRoiMaterial(Material = pm.Materials[i])
	except Exception:
		print 'Failed to generate Marker_5 override ROI. Continues...'
	#no further need for the temporary structure
	try:
		pm.RegionsOfInterest['Temp5'].DeleteRoi()
	except Exception:
		print 'Error cleaning up marker 5 source ROI. Continues...'
	#
	#fiducial number 6 - might not exist
	try:
		coord = pm.StructureSets[exam.Name].PoiGeometries[fiducial6].Point
		# --- set a new empty roi at this coordinate position
		pm.CreateRoi(Name='Temp6', Color="Fuchsia", Type="Marker", TissueName=None, RoiMaterial=None)
		# --- draw a 3mm spherical roi around the nominated poi
		pm.RegionsOfInterest['Temp6'].CreateSphereGeometry( Radius=0.3, Examination=exam, Center={'x':coord.x, 'y':coord.y, 'z':coord.z} )
		# --- draw a 7mm-wide wall region around the temporary roi
		pm.CreateRoi(Name=marker6, Color=colourMarker6, Type="Marker", TissueName=None, RoiMaterial=None)
		pm.RegionsOfInterest[marker6].SetWallExpression(SourceRoiName='Temp6', OutwardDistance=0.7, InwardDistance=0)
		pm.RegionsOfInterest[marker6].UpdateDerivedGeometry(Examination=exam)
		# --- reset the density override in this region to the newly created material (index from args)
		pm.RegionsOfInterest[marker6].SetRoiMaterial(Material = pm.Materials[i])
	except Exception:
		print 'Failed to generate Marker_6 override ROI. Continues...'
	#no further need for the temporary structure
	try:
		pm.RegionsOfInterest['Temp6'].DeleteRoi()
	except Exception:
		print 'Error cleaning up marker 6 source ROI. Continues...'
#procedure OverrideFiducialsDensity ends
#
#
#
# all prostate autoplans use the same default VMAT optimization settings
#
def SetVmatOptimizationParameters(op):
	try:
		# standard number of run iterations
		op.Algorithm.MaxNumberOfIterations = 40
		# standard optimality tolerance level
		op.Algorithm.OptimalityTolerance = 1E-05
		# set to compute intermediate and final dose
		op.DoseCalculation.ComputeFinalDose = 'True'
		op.DoseCalculation.ComputeIntermediateDose = 'True'
		# set number of iterations in preparation phase for DMPO
		op.DoseCalculation.IterationsInPreparationsPhase = 7
		# constraint arc segmentation for stable machine deliverability
		op.SegmentConversion.ArcConversionProperties.UseMaxLeafTravelDistancePerDegree = 'True'
		op.SegmentConversion.ArcConversionProperties.MaxLeafTravelDistancePerDegree = 0.40
	except Exception:
		raise Exception('Error - could not set optimization parameters by script.')
#
#
#
#


