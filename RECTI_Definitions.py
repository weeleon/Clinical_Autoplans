# DEFINE A SUPPLEMENTARY SET OF STRUCTURES TO EXTEND MASTER
#
# COLOR CHARTS :
#---- see http://www.rapidtables.com/web/color/RGB_Color.htm
#
#
# --- integral tumour volume for primary target
itvT = 'ITV-T'
colourItvT = "0,0,220"
#
# --- clinical tumour volume involved nodes
ctvP = 'CTV-P'
colourCtvP = "230,149,134"
#
itvP = 'ITV-P'
colourItvP = "0,0,220"
#
ptvP = 'PTV-P'
colourPtvP = "112,102,232"
#
# --- elective pelvic lymph nodes
ctvE = 'CTV-E'
colourCtvE = "255,81,81"
#
itvE = 'ITV-E'
colourItvE = "0,0,220"
#
ptvE = 'PTV-E'
colourPtvE = "126,130,239"
#
#
# --- target volume transitions for elective irradiation
transitionTPtoE = 'PTV-E-(PTV-T+5mm)'
#
# --- wall structures for dose conformality shaping
wall5mmPtvT = 'Wall; PTV-T+5mm'
wall8mmPtvT = 'Wall; PTV-T+8mm'
wall5mmPtvE = 'Wall; PTV-E+5mm'
wall8mmPtvE = 'Wall; PTV-E+8mm'
#
# --- complementary "external" structures outside targets for dose shaping
complementExt5mmPtvT = 'Ext-(PTV-T+5mm)'
complementExt5mmPtvE = 'Ext-(PTV-E+5mm)'
#
#
# DEFINE THE STANDARD COLLIMATOR ANGLE FOR VMAT ARCS IN PROSTATE
defaultRectiCollAngle = 30
#
#
# DEFINE THE STANDARD CLINICAL TEMPLATES FOR PLANNING OBJECTIVES
defaultClinicalGoalsRect62 = 'Recti_62Gy_Clinical_Goals_Template'
defaultClinicalGoalsRect60 = 'Recti_60Gy_Clinical_Goals_Template'
defaultClinicalGoalsRect50 = 'Recti_50Gy_Clinical_Goals_Template'
defaultClinicalGoalsRect25 = 'Recti_25Gy_Clinical_Goals_Template'
# 
# 
# 
# DEFINE THE STANDARD CLINICAL TEMPLATES FOR OPTIMIZATION FUNCTIONS
defaultOptimVmatRect62 = 'Recti_62Gy_VMAT_2arc_Optimization'
defaultOptimVmatRect60 = 'Recti_60Gy_VMAT_2arc_Optimization'
defaultOptimVmatRect50 = 'Recti_50Gy_VMAT_2arc_Optimization'
defaultOptimVmatRect25 = 'Recti_25Gy_VMAT_2arc_Optimization'
#
#
#
# all recti autoplans use the same default VMAT optimization settings
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


