from enum import Enum

from src.models.executable import Executable
from src.models.input import Input, InputClass, InputRange

from src.models.rr_enums import Program, Dat

class SystemState(Enum):
    COOLING = "1"
    HEATPUMP_COOLING = "0"
    HEATPUMP_HEATING = "-1"

class ASYS(Executable):
    def __init__(self):

        required_dats = [Dat.COIL, Dat.COIL1, Dat.COMP, Dat.COMPL, Dat.REF, Dat.REVALV]

        input_sequence = [[C(), TAE(), TWB(), EDB(), EWB(), FIRSTSUB(), LASTSUB(), INC(), ASC(), CD(), DSUP(), LS(), P(), SUBROWS(), RHROWS()],
                              [NP(), NL(), NE(), NC()],
                              [CNO(), EP(), CFW(), EFW(), K(), MC(), DC(), NM(), ME(), W(), OZ(), UM(), M()],
                              [],
                              [EVAP_N(), EVAP_FPI(), EVAP_ROWS(), EVAP_FH(), EVAP_FL(), EVAP_CFM(), EVAP_CKT1(), EVAP_CKT2(), EVAP_NT1(), EVAP_NT2(), EVAP_FLO(), EVAP_FIN(), EVAP_MTL(), EVAP_TW(), EVAP_TT(), EVAP_HDR(), EVAP_CON(), EVAP_SPHT(), EVAP_CF(), EVAP_EFW(), EVAP_TAE(), EVAP_TWB()],
                              [COND_N(), COND_FPI(), COND_ROWS(), COND_FH(), COND_FL(), COND_CFM(), COND_CKT1(), COND_CKT2(), COND_NT1(), COND_NT2(), COND_FLO(), COND_FIN(), COND_MTL(), COND_TW(), COND_TT(), COND_HDR(), COND_CON(), COND_SPHT(), COND_CF()]]
        for input in self.input_sequence[4]:
            input._code = "EVAP_" + input._code
        for input in self.input_sequence[4]:
            input._code = "COND_" + input._code

        result_mapping = {
            "QT/TQR": 57,
            "QS/QOA": 58,
            "QTR": 59,
            "EPD": 60,
            "EHDR PD": 61,
            "EWG": 62,
            ## FIXME missing many results!!!
            "UM": 140,
            "LBH20": 145,
        }

        super().__init__(
            program=Program.ASYS,
            result_mapping = result_mapping,
            input_sequence = input_sequence,
            required_dats = required_dats
        )

class ASYS_DX(ASYS):
    def __init__(self):
        super().__init__()
        self.input_sequence[3] = [SD1A(), SLENO(), SLENI(), SSV(), DD1A(), DLEN(), LD(), LL(), FD(), LSV(), ACCU(), ELE(), ELC(), QFD()]
        self.inputs["C"].options = ["1"]

class ASYS_HP(ASYS):
    def __init__(self):
        super().__init__()
        self.input_sequence[3] = [DD(), DL(), VD1(), VL1(), VL2O(), VL2I(), VL3(), VD4(), VL4(), SL1(), SD2(), SL2(), LD(), LL(), FD(), SSV(), LSV(), NREV(), LF(), MF(), ACCU(), CL(), VD2(), QFD()]
        self.inputs["C"].options = ["-1", "0"]

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LINE 1 INPUTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class C(InputClass):
    def __init__(self):
        super().__init__(
            code="C",
            data_type=str,
            description="1 for cooling system; 0 for heat pump cooling; -1 for heat pump heating",
            )
        
class TAE(InputRange):
    def __init__(self):
        super().__init__(
            code="TAE",
            data_type=float,
            description="Air Dry Bulb Temperature Entering Coil, F",
            )

class TWB(InputRange):
    def __init__(self):
        super().__init__(
            code="TWB",
            data_type=float,
            description="Air Wet Bulb Temperature Entering Coil, F",
            )

class EDB(InputRange):
    def __init__(self):
        super().__init__(
            code="EDB",
            data_type=float,
            description="Air Dry Bulb Temperature Leaving Coil, F",
            )

class EWB(InputRange):
    def __init__(self):
        super().__init__(
            code="EWB",
            data_type=float,
            description="Air Wet Bulb Temperature Leaving Coil, F",
            )

class ISO(InputClass):
    def __init__(self):
        super().__init__(
            code="ISO",
            data_type=str,
            description="0 if compressor in air stream, 1 if isolated, -1 if insulated jacket",
            options=["0", "1", "-1"],
            )

class FIRSTSUB(InputRange):
    def __init__(self):
        super().__init__(
            code="FIRSTSUB",
            data_type=int,
            description="First subcooling temperature in degrees Fahrenheit"
            )

class LASTSUB(InputRange):
    def __init__(self):
        super().__init__(
            code="LASTSUB",
            data_type=int,
            description="Last subcooling temperature in degrees Fahrenheit"
            )

class INC(InputRange):
    def __init__(self):
        super().__init__(
            code="INC",
            data_type=float,
            description="Increments between subcooling levels in °F",
            min_value = 0.1,
            is_required=True)

class ASC(InputRange):
    def __init__(self):
        super().__init__(
            code="ASC",
            data_type=float,
            description="Additional liquid subcooling, degrees F from external source "
            )

class CD(InputRange):
    def __init__(self):
        super().__init__(
            code="CD",
            data_type=int,
            description="Degradation factor (enter when SEER wanted)"
            )

class DSUP(InputRange):
    def __init__(self):
        super().__init__(
            code="DSUP",
            data_type=float,
            description=" Enter degress F (or MAX) hot gas desuperheating from external source"
        )

class LS(InputRange):
    def __init__(self):
        super().__init__(
            code="LS",
            data_type=float,
            description="Additional liquid subcooling, degrees F, from suction line heat exchange"
            )

from src.models.aevap import P ## FIXME P

class SUBROWS(InputRange):
    def __init__(self):
        super().__init__(
            code="SUBROWS",
            data_type=int,
            description=" Enter number of subcooler coil rows (enter minus (-)rows if microchannel)"
        )

class RHROWS(InputClass):
    def __init__(self):
        super().__init__(
            code="RHROWS",
            data_type=int,
            options=[191, 193, 224, 225, 273, 395, 445, 615, 1020, 1139, 1208, 1227, 1878],
            description="Enter model number of reheat coil (191, 193, 224, 225, 273, 395, 445, 615, 1020, 1139, 1208, 1227 or 1878)"
        )

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LINE 2 INPUTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NP(InputClass):
    def __init__(self):
        super().__init__(
            code="NP",
            data_type=int,
            description="OBSOLETE: New compressor, Enter 1 if a new element is to replace an old one; -1 if the element is to remain the same",
            options=[1]
            )

class NL(InputClass):
    def __init__(self):
        super().__init__(
            code="NL",
            data_type=int,
            description="OBSOLETE: New refrigerant lines, Enter 1 if a new element is to replace an old one; -1 if the element is to remain the same",
            options=[1]
            )


class NE(InputRange):
    def __init__(self):
        super().__init__(
            code="NE",
            data_type=int,
            description="New evaporator, if multi-split, enter number of evaporators; -1 if the element is to remain the same",
            min_value=1
        )

class NC(InputClass):
    def __init__(self):
        super().__init__(
            code="NC",
            data_type=int,
            description="OBSOLETE: New condenser, Enter 1 if a new element is to replace an old one; -1 if the element is to remain the same",
            options=[1]
        )

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LINE 3 INPUTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CNO(InputRange):
    def __init__(self):
        super().__init__(
            code="CNO",
            data_type=int,
            description="Compressor code number"
            )

class EP(InputRange):
    def __init__(self):
        super().__init__(
            code="EP",
            data_type=int,
            description="Electrical power, enter 1 for single phase 60 cycle; enter 2 for three phase 60 cycle; enter 3 for single phase 50 cycle; enter 4 for three phase 50 cycle; enter RPM for an open compressor",
            min_value=1
        )

class CFW(InputRange):
    def __init__(self):
        super().__init__(
            code="CFW",
            data_type=float,
            description="Condenser fan watts or outdoor coil if heat pump, enter (-) watts if draw thru air flow, enter watts in blow thru, multi-split enter totals all zones"
            )

class EFW(InputRange):
    def __init__(self):
        super().__init__(
            code="EFW",
            data_type=float,
            description="Evaporator fan watts or indoor coil if heat pump, enter (-) watts if draw thru air flow, enter watts in blow thru, multi-split enter totals all zones"
        )

class K(InputClass):
    def __init__(self):
        super().__init__(
            code="K",
            data_type=float,
            description=" System configuration code (See Page SK for schedule)"
        )

class MC(InputRange):
    def __init__(self):
        super().__init__(
            code="MC",
            data_type=float,
            description="Compressor nominal BTUH multiplier",
            min_value=0.0001
        )

class MW(InputRange):
    def __init__(self):
        super().__init__(
            code="MW",
            data_type=float,
            description="Compressor nominal watts multiplier",
            min_value=0.0001
            )

class DC(InputClass):
    def __init__(self):
        super().__init__(
            code="DC",
            data_type=int,
            description="1 for dry condenser pan but condensate re-evaporated, 0 for all others",
            options=[0, 1]
        )

class NM(InputClass):
    def __init__(self):
        description = "Enter 1C for a single motor located in the condenser air "   
        description += "driving both evaporator and condenser fans; "
        description += "enter 1E when the single motor is located in the evaporator air; " 
        description += "otherwise enter 2"
        super().__init__(
            code="NM",
            data_type=str,
            description=description,
            options = ["1C", "1E", "2"]
            )

class ME(InputRange):
    def __init__(self):
        description = "Evaporator motor efficiency; when NM = 2 enter 1 when motor in air "
        description += "stream, or motor efficiency as a decimal when not in air stream; "
        description += "when NM = 1C or 1E  enter motor efficiency as a decimal; "
        description += "enter 0 if gross QT and QS are desired"
        super().__init__(
            code="ME",
            data_type=float,
            description=description,
            min_value=0,
            max_value=1
            )

class W(InputRange):
    def __init__(self):
        super().__init__(
            code="W",
            data_type=float,
            description="Miscellaneous watts, such as crakecase heater, control transofmer, etc.",
            min_value=0
        )

class OZ(InputRange):
    def __init__(self):
        super().__init__(
            code="OZ",
            data_type=float,
            description="Fluid ounces oil added beyond the compressor initial charge requirement",
            min_value=0
        )

from src.models.aevap import UM ## FIXME UM

class M(InputClass):
    def __init__(self):
        super().__init__(
            code="M",
            data_type=str,
            description = "Enter M for metric print-out or leave blank for English print-out",
            options = ["M", ""]
            )

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LINE 4 INPUTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class DD(InputRange):
    def __init__(self):
        super().__init__(
            code="DD",
            data_type=int,
            description="Discharge Line OD in 1/8th inches",
            min_value=1
        )

from aevap import DL ## FIXME DL

class VD1(InputRange):
    def __init__(self):
        super().__init__(
            code="VD1",
            data_type=int,
            description="Vapor Lines SL1, VL1, VL2, VL3 O.D. in 1/8 inches",
            min_value=1
            )

class VL1(InputRange):
    def __init__(self):
        super().__init__(
            code="VL1",
            data_type=float,
            description="Vapor Line 1 length (feet)",
            min_value=0
            )

class VL2O(InputRange):
    def __init__(self):
        super().__init__(
            code="VL2O",
            data_type=float,
            description="Vapor Line #2 Length (feet) outdoor (enter 10 ft. for ARI rating)",
            min_value=0
        )

class VL2I(InputRange):
    def __init__(self):
        super().__init__(
            code="VL2I",
            data_type=float,
            description="Vapor Line #2 Length (feet) indoor (enter 15 ft. for ARI rating)",
            min_value=0
        )

class VL3(InputRange):
    def __init__(self):
        super().__init__(
            code="VL3",
            data_type=float,
            description="Vapor Line #3 Length (feet)",
            min_value=0
        )

class VD4(InputRange):
    def __init__(self):
        super().__init__(
            code="VD4",
            data_type=int,
            description="Vapor Line #4 O.D. in 1/8 inches",
            min_value=1
        )

class VL4(InputRange):
    def __init__(self):
        super().__init__(
            code="VL4",
            data_type=float,
            description="Vapor Line #4 Length (feet)",
            min_value=0
        )

class SL1(InputRange):
    def __init__(self):
        super().__init__(
            code="SL1",
            data_type=float,
            description="Suction Line #1 Length (feet)",
            min_value=0
        )

class SD2(InputRange):
    def __init__(self):
        super().__init__(
            code="SD2",
            data_type=int,
            description="Suction Line #2 O.D. in 1/8 inches",
            min_value=1
        )

class SL2(InputRange):
    def __init__(self):
        super().__init__(
            code="SL2",
            data_type=float,
            description="Suction Line #2 Length (feet)",
            min_value=0
        )

class LD(InputRange):
    def __init__(self):
        super().__init__(
            code="LD",
            data_type=int,
            description="Liquid Line O.D. in 1/8 inches",
            min_value=1
        )

class LL(InputRange):
    def __init__(self):
        super().__init__(
            code="LL",
            data_type=float,
            description="Liquid Line Length (feet), if insulated enter (-) length"
        )

class FD(Input): ## FIXME This should be an InputClass. need to get the FD models to use as options
    def __init__(self):
        description= "filter-drier models from page S2-B1; enter 0 if none"
        super().__init__(
            code="FD",
            data_type=str,
            description=description
        )

class SSV(InputRange):
    def __init__(self):
        description= "Suction Service Valve; enter 1 or 0 if none; "
        description += "or Aeroquip model size, i.e. 10, etc."
        super().__init__(
            code="SSV",
            data_type=str,
            description=description,
            min_value=0
            )

class LSV(InputRange):
    def __init__(self):
        description= "Liquid Service Valve; enter 1 or 0 if none; "
        description += "or Aeroquip model size, i.e. 6, etc."
        super().__init__(
            code="LSV",
            data_type=str,
            description=description,
            min_value=0
        )

class NREV(Input):
    def __init__(self):
        super().__init__(
            code="NREV",
            data_type=str,
            description="Reversing Valve (see schedule) Page NREV"
        )

class LF(InputRange):
    def __init__(self):
        super().__init__(
            code="LF",
            data_type=float,
            description="NREV leakage factor",
            min_value=0,
            max_value=1
        )

class MF(Input):
    def __init__(self):
        super().__init__(
            code="MF",
            data_type=str,
            description="Body/Seat/Connections Metals Factor (see Page NREV)"
        )

class ACCU(InputRange):
    def __init__(self):
        super().__init__(
            code="ACCU",
            data_type=int,
            description="Accumulator Connection size (0 if none, or connection O.D in 1/8 inches)",
            min_value=0
        )

class CL(InputClass):
    def __init__(self):
        super().__init__(
            code="CL",
            data_type=str,
            description="Compressor Location (0 for outdoor; 1 for indoor)",
            options=["0", "1"]
        )

class VD2(InputRange):
    def __init__(self):
        super().__init__(
            code="VD2",
            data_type=int,
            description="Vapor Line #2 O.D. in 1/8 inches if different than VD1",
            min_value=0
        )

class QFD(InputRange):
    def __init__(self):
        super().__init__(
            code="QFD",
            data_type=int,
            description="Quantity of filter-driers (if multiples installed in parallel)",
            min_value=0
        )

class SD1A(InputRange):
    def __init__(self):
        super().__init__(
            code="SD1A",
            data_type=int,
            description="Suction Line O.D. in 1/8 inches (thus 7 for 7/8 inches)",
            min_value=1
        )

class SLENO(InputRange):
    def __init__(self):
        super().__init__(
            code="SLENO",
            data_type=float,
            description="Suction Line Length (ft.) outdoor (enter 10 ft. for ARI rating)",
            min_value=0
        )

class SLENI(InputRange):
    def __init__(self):
        super().__init__(
            code="SLENI",
            data_type=float,
            description="Suction Line Length (ft.) indoor (enter 15 ft. for ARI rating)",
            min_value=0
        )

## SSV is defined in the HP section of Line 4

class DD1A(InputRange):
    def __init__(self):
        super().__init__(
            code="DD1A",
            data_type = float,
            description = "Discharge Line O.D. in 1/8'' (thus 2.5 for 5/6)",
            min_value=0
        )

class DLEN(InputRange):
    def __init__(self):
        super().__init__(
            code="DLEN",
            data_type = float,
            description = "Discharge Line Length (ft.)",
            min_value=0
        )        

# LD is defined in the HP section of Line 4

# LL is defined in the HP section of Line 4

# FD is defined in the HP section of Line 4

# LSV is defined in the HP section of Line 4

# ACCU is defined in the HP section of Line 4

class ELE(InputRange):
    def __init__(self):
        super().__init__(
            code="ELE",
            data_type=float,
            description="Elevation (ft.) compressor above evaporator, omit when compressor at or below evap level",
            min_value=0,
            is_required = False
        )

class ELC(InputRange):
    def __init__(self):
        super().__init__(
            code="ELC",
            data_type=float,
            description="Elevation (ft.) compressor above condenser, omit when compressor at or below cond level",
            min_value=0,
            is_required = False
        )

# QFD is defined in the HP section of Line 4.

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LINE 5 INPUTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.models.aevap import N as EVAP_N
from src.models.aevap import FPI as EVAP_FPI
from src.models.aevap import ROWS as EVAP_ROWS
from src.models.aevap import FH as EVAP_FH
from src.models.aevap import FL as EVAP_FL
from src.models.aevap import CFM as EVAP_CFM

class EVAP_CKT1(InputRange):
    def __init__(self):
        super().__init__(
            code = "CKT1",
            data_type = int,
            description = "Number of ckts. in first ckt.",
            min_value= 1
        )

class EVAP_CKT2(InputRange):
    def __init__(self):
        super().__init__(
            code = "CKT2",
            data_type = int,
            description = "Number of ckts. in second ckt.",
            min_value= 1
        )

class EVAP_NT1(InputRange):
    def __init__(self):
        super().__init__(
            code = "NT1",
            data_type = int,
            description = "Number of tubes in first ckt.",
            min_value= 1
        )

class EVAP_NT2(InputRange):
    def __init__(self):
        super().__init__(
            code = "NT2",
            data_type = int,
            description = "Number of tubes in second ckt.",
            min_value= 1
        )

from src.models.aevap import FLO as EVAP_FLO
from src.models.aevap import FIN as EVAP_FIN
from src.models.aevap import MTL as EVAP_MTL

class EVAP_TW(InputRange):
    def __init__(self):
        super().__init__(
            code="TW",
            data_type=int,
            description="Tube Wall in mils, thus 16, etc."
        )

class EVAP_TT(InputRange):
    def __init__(self):
        description = "Tube Treatment; enter Z for smooth; YB for Bosier City rifled; "
        description += "YH for Hitachi-HEX rifled; F for Fedders 5/16'' or 3/8'' OD "
        description += "aluminum grooved tubing (coils #29, 30, and 31 only); "
        description += "S3H for NFA high groove; S3L for NFA small groove; S3 for NFA NCP; "
        description += "W for Wolverine rifled; X for Outokumpu Plus-XA; "
        description += "A for Outokumpu Plus-A; L for Outokumpu Plus-XAL or Plus-XHL; "
        description += "H for Outokumpu rifled; V for Outokumpu Plus-X2V; "
        description += "U for Unilloy cross-hatched; B for Brazeway 5/16” or 3/8” grooved; "
        description += "SR for SAPA 7mm rifled; SG for SAPA 7mm or 3/8” grooved; "
        description += "I for IGT 5mm rifled"
        super().__init__(
            code="TT",
            data_type=int,
            description=description
        )

class EVAP_HDR(Input):
    def __init__(self):
        description = "Vapor Header O.D. in 1/8'', thus 7 for 7/8'', plus coil adapter tube " 
        description += "fabrication technique (S for sweged and inserted into drilled hole, "
        description += "or E for inserted into an extruded collar, thus 7S or 7E); "
        description += "for Elkhart 3/8'' O.D. extruded top outlet return bend enter .3; "
        description += "if no header enter 0"
        super().__init__(
            code="HDR",
            data_type = str,
            description = description
            )

    def _validate(self, value):
        if not super()._validate(value):
            return False
        if value in ["0", ".3"]:
            return True
        if value[-1] not in ["S", "E"]:
            return False
        try:
            val = int(value[:-1]) * 1
            return True
        except Exception:
            return False
        
from src.models.aevap import CON as EVAP_CON
from src.models.aevap import SPHT as EVAP_SPHT

class EVAP_CF(InputRange):
    def __init__(self):
        super().__init__(
            code = "CF",
            data_type = int,
            description = "Quantity of Capillary Tubes (if omitted, computer reads CKT2)",
            min_value=1,
            _is_required=False
        )

class EVAP_EFW(InputRange):
    def __init__(self):
        super().__init__(
            code = "EFW",
            data_type = int,
            description = "Multi-split evaporator fan watts (individual fan coil)",
            min_value=0,
            _is_required=False
        )
    
class EVAP_TAE(InputRange):
    def __init__(self):
        super().__init__(
            code = "TAE",
            data_type = int,
            description = "Multi-split evaporator air temperature, °F dry bulb (if different than line 1)",
            min_value=0,
            _is_required=False
        )
    
class EVAP_TWB(InputRange):
    def __init__(self):
        super().__init__(
            code = "TWB",
            data_type = int,
            description = "Multi-split evaporator air temperature, °F wet bulb (if different than line 1)",
            min_value=0,
            _is_required=False
        )

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LINE 6 INPUTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.models.acond import N as COND_N
from src.models.acond import FPI as COND_FPI
from src.models.acond import ROWS as COND_ROWS
from src.models.acond import FH as COND_FH
from src.models.acond import FL as COND_FL
from src.models.acond import CFM as COND_CFM
from src.models.acond import CKT1 as COND_CKT1
from src.models.acond import CKT2 as COND_CKT2
from src.models.acond import NT1 as COND_NT1
from src.models.acond import NT2 as COND_NT2

class COND_FLO(InputClass):
    def __init__(self):
        description = "Code for Circuiting arrangement (enter 0; If heat pump heating, "
        description += "enter 0 = cross; 1 = parallel; -1 = counter; "
        description += "2 = parallel except superheat in entering air row)"
        super().__init__(
            code = "FLO",
            data_type = str,
            description = description,
            options = [-1, 0, 1, 2]
        )

from src.models.acond import FIN as COND_FIN
from src.models.acond import MTL as COND_MTL

class COND_TW(InputRange):
    def __init__(self):
        super().__init__(
            code="TW",
            data_type=int,
            description="Tube Wall in mils, thus 16, etc."
        )

class COND_TT(Input):
    def __init__(self):
        description = "Tube Treatment; enter Z for smooth; YB for Bosier City rifled; "
        description += "YH for Hitachi-HEX rifled; F for Fedders 5/16'' or 3/8'' OD "
        description += "aluminum grooved tubing (coils #29, 30, and 31 only); "
        description += "S3H for NFA high groove; S3L for NFA small groove; S3 for NFA NCP; "
        description += "W for Wolverine rifled; X for Outokumpu Plus-XA; "
        description += "A for Outokumpu Plus-A; L for Outokumpu Plus-XAL or Plus-XHL; "
        description += "H for Outokumpu rifled; V for Outokumpu Plus-X2V; "
        description += "U for Unilloy cross-hatched; B for Brazeway 5/16” or 3/8” grooved; "
        description += "SR for SAPA 7mm rifled; SG for SAPA 7mm or 3/8” grooved; "
        description += "I for IGT 5mm rifled"
        super().__init__(
            code="TT",
            data_type=str,
            description=description
        )

from src.models.acond import HDR as COND_HDR
from src.models.acond import CON as COND_CON

class COND_SPHT(InputRange):
    def __init__(self):
        super().__init__(
            code="SPHT",
            data_type = float,
            description = "Superheat, °F for Heat Pump; omit for Cooling Only ",
            is_required = False,
            min_value = 0
        )

class COND_CF(InputRange):
    def __init__(self):
        super().__init__(
            code = "CF",
            data_type = int,
            description = "Quantity of Capillary Tubes for Heat Pump (if omitted computer reads CKT2); Omit for Cooling Only",
            is_required = False,
            min_value = 0
        )
