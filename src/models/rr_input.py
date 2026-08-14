from src.models.executable import InputValue
    
class C(InputValue):
    def __init__(self, value = None):
        super().__init__(code="C",
                         data_type=int,
                         description="1 for cooling system; 0 for heat pump cooling; -1 for heat pump heating")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value not in [-1, 0, 1]:
            raise ValueError("C must be -1, 0, or 1")
        super().setValue(value)

class ISO(InputValue):
    def __init__(self, value = None):
        super().__init__(code="ISO",
                         data_type=int,
                         description="0 if compressor in air stream, 1 if isolated, -1 if insulated jacket")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value not in [-1, 0, 1]:
            raise ValueError("ISO must be -1, 0, or 1")
        super().setValue(value)

class ASC(InputValue):
    def __init__(self, value = None):
        super().__init__(code="ASC",
                         data_type=float,
                         description="Additional liquid subcooling, degrees F from external source ")
        self.setValue(value)

class CD(InputValue):
    def __init__(self, value = None):
        super().__init__(code="CD",
                         data_type=int,
                         description="Degradation factor")
        self.setValue(value)

class DSUP(InputValue):
    def __init__(self, value = None):
        super().__init__(code="DSUP",
                         data_type=float,
                         description=" Enter degress F (or MAX) hot gas desuperheating from external source")
        self.setValue(value)

class LS(InputValue):
    def __init__(self, value = None):
        super().__init__(code="LS",
                         data_type=float,
                         description="Additional liquid subcooling, degrees F, from suction line heat exchange")
        self.setValue(value)

class SUBROWS(InputValue):
    def __init__(self, value = None):
        super().__init__(code="SUBROWS",
                         data_type=int,
                         description=" Enter number of subcooler coil rows (enter minus (-)rows if microchannel)")
        self.setValue(value)

class RHROWS(InputValue):
    def __init__(self, value = None):
        super().__init__(code="RHROWS",
                         data_type=int,
                         description="Enter model number of reheat coil (191, 193, 224, 225, 273, 395, 445, 615, 1020, 1139, 1208, 1227 or 1878)")
        self.setValue(value)

class NP(InputValue):
    def __init__(self, value = None):
        super().__init__(code="NP",
                         data_type=int,
                         description="New compressor, Enter 1 if a new element is to replace an old one; -1 if the element is to remain the same")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value not in [-1, 1]:
            raise ValueError("NP must be -1 or 1")
        super().setValue(value)

class NL(InputValue):
    def __init__(self, value = None):
        super().__init__(code="NL",
                         data_type=int,
                         description="New refrigerant lines, Enter 1 if a new element is to replace an old one; -1 if the element is to remain the same")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value not in [-1, 1]:
            raise ValueError("NL must be -1 or 1")
        super().setValue(value)

class NE(InputValue):
    def __init__(self, value = None):
        super().__init__(code="NE",
                         data_type=int,
                         description="New evaporator, if multi-split, enter number of evaporators; -1 if the element is to remain the same")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value not in [-1] and value < 1:
            raise ValueError("NE must be -1 or a positive integer")
        super().setValue(value)

class NC(InputValue):
    def __init__(self, value = None):
        super().__init__(code="NC",
                         data_type=int,
                         description="New condenser, Enter 1 if a new element is to replace an old one; -1 if the element is to remain the same")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value not in [-1, 1]:
            raise ValueError("NC must be -1 or 1")
        super().setValue(value)

class CNO(InputValue):
    def __init__(self, value = None):
        super().__init__(code="CNO",
                         data_type=int,
                         description="Compressor code number")
        self.setValue(value)

class EP(InputValue):
    def __init__(self, value = None):
        super().__init__(code="EP",
                         data_type=int,
                         description="Electrical power, enter 1 for single phase 60 cycle; enter 2 for three phase 60 cycle; enter 3 for single phase 50 cycle; enter 4 for three phase 50 cycle; enter RPM for an open compressor")
        self.setValue(value)

class CFW(InputValue):
    def __init__(self, value = None):
        super().__init__(code="CFW",
                         data_type=float,
                         description="Condenser fan watts or outdoor coil if heat pump, enter (-) watts if draw thru air flow, enter watts in blow thru, multi-split enter totals all zones")
        self.setValue(value)

class EFW(InputValue):
    def __init__(self, value = None):
        super().__init__(code="EFW",
                         data_type=float,
                         description="Evaporator fan watts or indoor coil if heat pump, enter (-) watts if draw thru air flow, enter watts in blow thru, multi-split enter totals all zones")
        self.setValue(value)

class K(InputValue):
    def __init__(self, value = None):
        super().__init__(code="K",
                         data_type=float,
                         description=" System configuration code (See Page SK for schedule)")
        self.setValue(value)

class MC(InputValue):
    def __init__(self, value = None):
        super().__init__(code="MC",
                         data_type=float,
                         description="Compressor nominal BTUH multiplier")
        self.setValue(value)
    
    def setValue(self, value):
        value = self._coerce(value)
        if value <= 0 or value > 1:
            raise ValueError("MC must be between 0 and 1")
        super().setValue(value)

class MW(InputValue):
    def __init__(self, value = None):
        super().__init__(code="MW",
                         data_type=float,
                         description="Compressor nominal watts multiplier")
        self.setValue(value)
    
    def setValue(self, value):
        value = self._coerce(value)
        if value <= 0 or value > 1:
            raise ValueError("MW must be between 0 and 1")
        super().setValue(value)

class DC(InputValue):
    def __init__(self, value = None):
        super().__init__(code="DC",
                         data_type=int,
                         description="1 for dry condenser pan but condensate re-evaporated, 0 for all others")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value not in [0, 1]:
            raise ValueError("DC must be 0 or 1")
        super().setValue(value)

class NM(InputValue):
    def __init__(self, value = None):
        description = "Enter 1C for a single motor located in the condenser air "   
        description += "driving both evaporator and condenser fans; "
        description += "enter 1E when the single motor is located in the evaporator air; " 
        description += "otherwise enter 2"
        super().__init__(code="NM",
                         data_type=str,
                         description=description)
        self.setValue(value)
    
    def setValue(self, value):
        value = self._coerce(value)
        if value not in ["1C", "1E", "2"]:
            raise ValueError("NM must be 1C, 1E, or 2")
        super().setValue(value)

class ME(InputValue):
    def __init__(self, value = None):
        description = "Evaporator motor efficiency; when NM = 2 enter 1 when motor in air "
        description += "stream, or motor efficiency as a decimal when not in air stream; "
        description += "when NM = 1C or 1E  enter motor efficiency as a decimal; "
        description += "enter 0 if gross QT and QS are desired"
        super().__init__(code="ME",
                         data_type=float,
                         description=description)
        self.setValue(value)
    
    def setValue(self, value):
        value = self._coerce(value)
        if value < 0 or value > 1:
            raise ValueError("ME must be between 0 and 1")
        super().setValue(value)

class W(InputValue):
    def __init__(self, value = None):
        super().__init__(code="W",
                         data_type=float,
                         description="Miscellaneous watts, such as crakecase heater, control transofmer, etc.")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("W must be greater than or equal to 0")
        super().setValue(value)

class OZ(InputValue):
    def __init__(self, value = None):
        super().__init__(code="OZ",
                         data_type=float,
                         description="Fluid ounces oil added beyond the compressor initial charge requirement")
        self.setValue(value)
    
    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("OZ must be greater than or equal to 0")
        super().setValue(value)

class M(InputValue):
    def __init__(self, value = None):
        super().__init__(code="M",
                         data_type=str,
                         description = "Enter M for metric print-out or leave blank for English print-out")
        self.setValue(value)
    
    def setValue(self, value):
        value = self._coerce(value)
        if value not in ['M', None]:
            raise ValueError("M must be 'M' or None")
        super().setValue(value)

class DD(InputValue):
    def __init__(self, value = None):
        super().__init__(code="DD",
                         data_type=int,
                         description="Discharge Line OD in 1/8th inches")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Discharge Line OD cannot be negative")
        super().setValue(value)

class DL2(InputValue):
    def __init__(self, value = None):
        super().__init__(code="DL",
                         data_type=float,
                         description="Discharge line length (feet)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Discharge line length cannot be negative")
        super().setValue(value)

class VD1(InputValue):
    def __init__(self, value = None):
        super().__init__(code="VD1",
                         data_type=int,
                         description="Vapor Lines SL1, VL1, VL2, VL3 O.D. in 1/8 inches")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Vapor line OD cannot be negative")
        super().setValue(value)

class VL1(InputValue):
    def __init__(self, value = None):
        super().__init__(code="VL2",
                         data_type=float,
                         description="Vapor Line 1 length (feet)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Vapor line #1 length cannot be negative")
        super().setValue(value)

class VL2O(InputValue):
    def __init__(self, value = None):
        super().__init__(code="VL2O",
                         data_type=float,
                         description="Vapor Line #2 Length (feet) outdoor (enter 10 ft. for ARI rating)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Vapor line #2 length cannot be negative")
        super().setValue(value)

class VL2I(InputValue):
    def __init__(self, value = None):
        super().__init__(code="VL2I",
                         data_type=float,
                         description="Vapor Line #2 Length (feet) indoor (enter 15 ft. for ARI rating)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Vapor line #2 length cannot be negative")
        super().setValue(value)

class VL3(InputValue):
    def __init__(self, value = None):
        super().__init__(code="VL3",
                         data_type=float,
                         description="Vapor Line #3 Length (feet)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Vapor line #3 length cannot be negative")
        super().setValue(value)

class VD4(InputValue):
    def __init__(self, value = None):
        super().__init__(code="VD4",
                         data_type=int,
                         description="Vapor Line #4 O.D. in 1/8 inches")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Vapor line #4 OD cannot be negative")
        super().setValue(value)

class VL4(InputValue):
    def __init__(self, value = None):
        super().__init__(code="VL4",
                         data_type=float,
                         description="Vapor Line #4 Length (feet)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Vapor line #4 length cannot be negative")
        super().setValue(value)

class SL1(InputValue):
    def __init__(self, value = None):
        super().__init__(code="SL1",
                         data_type=float,
                         description="Suction Line #1 Length (feet)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Suction line #1 length cannot be negative")
        super().setValue(value)

class SD2(InputValue):
    def __init__(self, value = None):
        super().__init__(code="SD2",
                         data_type=int,
                         description="Suction Line #2 O.D. in 1/8 inches")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Suction line #2 OD cannot be negative")
        super().setValue(value)

class SL2(InputValue):
    def __init__(self, value = None):
        super().__init__(code="SL2",
                         data_type=float,
                         description="Suction Line #2 Length (feet)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Suction line #2 length cannot be negative")
        super().setValue(value)

class LD(InputValue):
    def __init__(self, value = None):
        super().__init__(code="LD",
                         data_type=int,
                         description="Liquid Line O.D. in 1/8 inches")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Liquid line OD cannot be negative")
        super().setValue(value)

class LL(InputValue):
    def __init__(self, value = None):
        super().__init__(code="LL",
                         data_type=float,
                         description="Liquid Line Length (feet), if insulated enter (-) length")
        self.setValue(value)

class FD(InputValue):
    def __init__(self, value = None):
        description= "filter-drier models from page S2-B1; enter 0 if none"
        super().__init__(code="FD",
                         data_type=str,
                            description=description)
        self.setValue(value)

class SSV(InputValue):
    def __init__(self, value = None):
        description= "Suction Service Valve; enter 1 or 0 if none; "
        description += "or Aeroquip model size, i.e. 10, etc."
        super().__init__(code="SSV",
                         data_type=str,
                         description=description)
        self.setValue(value)

class LSV(InputValue):
    def __init__(self, value = None):
        description= "Liquid Service Valve; enter 1 or 0 if none; "
        description += "or Aeroquip model size, i.e. 6, etc."
        super().__init__(code="LSV",
                         data_type=str,
                         description=description)
        self.setValue(value)

class NREV(InputValue):
    def __init__(self, value = None):
        super().__init__(code="NREV",
                         data_type=str,
                         description="Reversing Valve (see schedule) Page NREV")
        self.setValue(value)

class LF(InputValue):
    def __init__(self, value = None):
        super().__init__(code="LF",
                         data_type=float,
                         description="NREV leakage factor")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value <= 0 or value > 1:
            raise ValueError("LF must be greater than 0 and less than or equal to 1")
        super().setValue(value)

class MF(InputValue):
    def __init__(self, value = None):
        super().__init__(code="MF",
                         data_type=str,
                         description="Body/Seat/Connections Metals Factor (see Page NREV)")
        self.setValue(value)

class ACCU(InputValue):
    def __init__(self, value = None):
        super().__init__(code="ACCU",
                         data_type=int,
                         description="Accumulator Connection size (0 if none, or connection O.D in 1/8 inches)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Accumulator connection size cannot be negative")
        super().setValue(value)

class CL(InputValue):
    def __init__(self, value = None):
        super().__init__(code="CL",
                         data_type=int,
                         description="Compressor Location (0 for outdoor; 1 for indoor)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value not in [0, 1]:
            raise ValueError("Compressor location must be 0 or 1")
        super().setValue(value)

class VD2(InputValue):
    def __init__(self, value = None):
        super().__init__(code="VD2",
                         data_type=int,
                         description="Vapor Line #2 O.D. in 1/8 inches")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Vapor line #2 OD cannot be negative")
        super().setValue(value)

class QFD(InputValue):
    def __init__(self, value = None):
        super().__init__(code="QFD",
                         data_type=int,
                         description="Quantity of filter-driers (if multiples installed in parallel)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Quantity of filter-driers cannot be negative")
        super().setValue(value)

class SD1A(InputValue):
    def __init__(self, value = None):
        super().__init__(code="SD1A",
                         data_type=int,
                         description="Suction Line O.D. in 1/8 inches (thus 7 for 7/8 inches)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Suction line O.D. cannot be negative")
        super().setValue(value)

class SLENO(InputValue):
    def __init__(self, value = None):
        super().__init__(code="SLENO",
                         data_type=float,
                         description="Suction Line Length (ft.) outdoor (enter 10 ft. for ARI rating)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Suction line length cannot be negative")
        super().setValue(value)

class SLENI(InputValue):
    def __init__(self, value = None):
        super().__init__(code="SLENI",
                         data_type=float,
                         description="Suction Line Length (ft.) indoor (enter 15 ft. for ARI rating)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Suction line length cannot be negative")
        super().setValue(value)

class ELE(InputValue):
    def __init__(self, value = None):
        super().__init__(code="ELE",
                         data_type=float,
                         description="Elevation (ft.) compressor above evaporator, omit when compressor at or below evap level")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            value = None
        super().setValue(value)

class ELC(InputValue):
    def __init__(self, value = None):
        super().__init__(code="ELC",
                         data_type=float,
                         description="Elevation (ft.) compressor above condenser, omit when compressor at or below cond level")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            value = None
        super().setValue(value)

class N(InputValue):
    def __init__(self, value = None):
        super().__init__(code="N",
                         data_type=int,
                         description="Coil code")
        self.setValue(value)

class FIRSTSUB(InputValue):
    def __init__(self, value = None):
        super().__init__(code="FIRSTSUB",
                         data_type=int,
                         description="First subcooling temperature in degrees Fahrenheit")
        self.setValue(value)

class LASTSUB(InputValue):
    def __init__(self, value = None):
        super().__init__(code="LASTSUB",
                         data_type=int,
                         description="Last subcooling temperature in degrees Fahrenheit")
        self.setValue(value)


class QTY(InputValue):
    def __init__(self, value = None):
        super().__init__(code="QTY",
                         data_type=int,
                         description="Quantity of coils piped in parallel air and fluid flow")
        self.setValue(value)
        
class FPI(InputValue):
    def __init__(self, value = None):
        super().__init__(code="FPI",
                         data_type=float,
                         description="Fins per inch")
        self.setValue(value)
        
    def setValue(self, value):
        value = self._coerce(value)
        if value<1:
            raise ValueError("FPI must be greater or equal to 1")
        super().setValue(value)

class ROWS(InputValue):
    def __init__(self, value = None):
        super().__init__(code="ROWS",
                         data_type=float,
                         description="Number of Rows, each coil (accepts partial rows to second decimal)")
        self.setValue(value)
    
    def setValue(self, value):
        value = self._coerce(value)
        if value<=0:
            raise ValueError("ROWS must be greater or equal to 0")
        super().setValue(value)

class FH(InputValue):
    def __init__(self, value = None):
        super().__init__(code="FH",
                         data_type=float,
                         description="Fin Height in inches")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value<=0:
            raise ValueError("FH must be greater than 0")
        super().setValue(value)

class FL(InputValue):
    def __init__(self, value = None):
        super().__init__(code="FL",
                         data_type=float,
                         description="Fin Length in inches")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value<=0:
            raise ValueError("FL must be greater than 0")
        super().setValue(value)

class CFM(InputValue):
    def __init__(self, value = None):
        super().__init__(code="CFM",
                         data_type=float,
                         description="Airflow in Cubic Feet per Minute, total all coils")
        self.setValue(value)
        
    def setValue(self, value):
        value = self._coerce(value)
        if value<=0:
            raise ValueError("CFM must be greater than 0")
        super().setValue(value)

class SA(InputValue):
    def __init__(self, value = None):
        super().__init__(code="SA",
                         data_type=str,
                         description="Enter S for Standard airflow, or A for Actual airflow")
        self.setValue(value)

    def setValue(self, value):
        if value not in ['S', 'A']:
            raise ValueError("SA must either be 'S' or 'A'")
        super().setValue(value)

class CKT(InputValue):
    def __init__(self, value = None):
        super().__init__(code="CKT",
                         data_type=int,
                         description="Number of circuits each coil")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value <= 0:
            raise ValueError("CKT must be a positive integer")
        super().setValue(value)

class CKT1(InputValue):
    def __init__(self, value = None):
        super().__init__(code="CKT1",
                         data_type=int,
                         description="Number of Circuits in first circuit")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value <= 0:
            raise ValueError("CKT1 must be a positive integer")
        super().setValue(value)

class CKT2(InputValue):
    def __init__(self, value = None):
        super().__init__(code="CKT2",
                         data_type=int,
                         description="Number of Circuits in second circuit")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value <= 0:
            raise ValueError("CKT2 must be a positive integer")
        super().setValue(value)

class NT1(InputValue):
    def __init__(self, value = None):
        super().__init__(code="NT1",
                         data_type=int,
                         description="Number of tubes in first circuit")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value <= 0:
            raise ValueError("NT1 must be a positive integer")
        super().setValue(value)

class NT2(InputValue):
    def __init__(self, value = None):
        super().__init__(code="NT2",
                         data_type=int,
                         description="Number of tubes in second circuit")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value <= 0:
            raise ValueError("NT2 must be a positive integer")
        super().setValue(value)

class DL(InputValue):
    def __init__(self, value = None):
        super().__init__(code="DL",
                         data_type=float,
                         description="Length in inches of distributor lines, if no distributor enter 0")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("DL must be greater than or equal to 0")
        super().setValue(value)

class OD(InputValue):
    def __init__(self, value = None):
        super().__init__(code="OD",
                         data_type=float,
                         description="Distributor Line OD in inches")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value <= 0:
            raise ValueError("Distributor Line OD must be greater than 0")
        super().setValue(value)

class NZ(InputValue):
    def __init__(self, value = None):
        super().__init__(code="NZ",
                         data_type=str,
                         description="Distributor Orifice Number, see documentation for details")
        self.setValue(value)

    def setValue(self, value):
        if value not in ["0", ".5",  ".75",  "1",  "1.5", "1.75",  "2",  "2.5",  "3",  "3.5",  "4",  "4.5" , "5",  "6",  "8",  "10",  "12",  "15",  "17",  "20",  "25",  "30",  "35",  "40" , "50", '"V"']:
            raise ValueError("NZ must be greater than or equal to 0. Enter V for Venturi style")
        super().setValue(value)

class SPHT(InputValue):
    def __init__(self, value = None):
        super().__init__(code="SPHT",
                         data_type=float,
                         description="Superheat in degrees Fahrenheit")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Superheat must be greater than or equal to 0")
        super().setValue(value)

class CF(InputValue):
    def __init__(self, value = None):
        super().__init__(code="CF",
                         data_type=int,
                         description="Quantity of Capillary Tubes")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value <= 0:
            raise ValueError("Quantity of Capillary Tubes")
        super().setValue(value)

class FLO(InputValue):
    def __init__(self, value = None):
        super().__init__(code="FLO",
                         data_type=float,
                         description="Circuiting Arrangement (0 = Cross; 1 = Parallel; 2 = Parallel except superheat in entering air row; -1 = Counter)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value not in [0, 1, 2, -1]:
            raise ValueError("Circuiting arrangement must be 0, 1, 2, or -1")
        super().setValue(value)

class FIN(InputValue):
    def __init__(self, value = None):
        super().__init__(code="FIN",
                         data_type=float,
                         description="Fin Thickness, mils*10")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Fin thickness cannot be negative")
        super().setValue(value)

class MTL(InputValue):
    def __init__(self, value = None):
        super().__init__(code="MTL",
                         data_type=int,
                         description="Fin Material; 0 = Aluminum; 1 = Copper; 2 = Carbon Steel 3 = 90/10 Cupronickel; 4 = 302 Stainless Steel; 5 = bare tubes")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value not in [0, 1, 2, 3, 4, 5]:
            raise ValueError("Fin material must be 0, 1, 2, 3, 4, or 5")
        super().setValue(value)

class T(InputValue):
    def __init__(self, value = None):
        super().__init__(code="T",
                         data_type=str,
                         description="Tube treatement and wall thickness, see documentation for details")
        self.setValue(value)
        
    def setValue(self, value):
        # the first char must be either Z, F, Y, X, A, L, H, V, N, U, B, S, or I
        # the remaining chars must be a number with or without a decimal
        if value[0] not in ['Z', 'F', 'Y', 'X', 'A', 'L', 'H', 'V', 'N', 'U', 'B', 'S', 'I']:
            raise ValueError("Invalid tube treatment (tube treatment and wall thickness)")
        try:
            if float(value[1:]) < 0:
                raise ValueError("Wall thickness must be greater than or equal to 0 (tube treatment and wall thickness)")
        except ValueError:
            raise ValueError("Invalid wall thickness (tube treatment and wall thickness)")
        super().setValue(value)

class TW(InputValue):
    def __init__(self, value = None):
        super().__init__(code="TW",
                         data_type=float,
                         description="Tube wall thickness in mils")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Tube wall thickness cannot be negative")
        super().setValue(value)

class TT(InputValue):
    def __init__(self, value = None):
        super().__init__(code="TT",
                         data_type=str,
                         description="Tube treatement, see documentation for details")
        self.setValue(value)


class GD(InputValue):
    def __init__(self, value = None):
        super().__init__(code="GD",
                         data_type=float,
                         description="Groove Depth in mils")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Groove depth cannot be negative")
        super().setValue(value)

class A(InputValue):
    def __init__(self, value = None):
        super().__init__(code="A",
                         data_type=float,
                         description="Ridge apex angle in degrees")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0 or value > 180:
            raise ValueError("Ridge apex angle must be between 0 and 180 degrees")
        super().setValue(value)

class NR(InputValue):
    def __init__(self, value = None):
        super().__init__(code="NR",
                         data_type=int,
                         description="Number of ridges")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Number of ridges cannot be negative")
        super().setValue(value)

class B(InputValue):
    def __init__(self, value = None):
        super().__init__(code="B",
                         data_type=float,
                         description="Lead helix angle in degrees")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0 or value > 180:
            raise ValueError("Lead helix angle must be between 0 and 180 degrees")
        super().setValue(value)

class HDR(InputValue):
    def __init__(self, value = None):
        super().__init__(code="HDR",
                         data_type=str,
                         description="O.D. in 1/8th inches + coil adapter tube fabrication technique, see documentation for details")
        self.setValue(value)

    def setValue(self, value):
        # the value can be 0, OR...
        # the last character must be either S or E
        # the first characters must be an integer
        if value == "0":
            super().setValue(value)
            return
        if value[-1] not in ['S', 'E']:
            raise ValueError("Invalid tube treatment (HDR). Last character must be either S or E")
        try:
            if int(value[0:-1]) < 0:
                raise ValueError("suction header OD must be greater than 0 (HDR)")
        except ValueError:
            raise ValueError("Invalid suction header OD (HDR)")
        super().setValue(value)

class CON(InputValue):
    def __init__(self, value = None):
        super().__init__(code="CON",
                         data_type=int,
                         description="Connection O.D. in 1/8th inches")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 0:
            raise ValueError("Connection O.D. cannot be negative")
        super().setValue(value)

class HTP(InputValue):
    def __init__(self, value = None):
        super().__init__(code="HTP",
                         data_type=int,
                         description=" Enter 1 for Heat Pipe (oil free); omit when matched with a compressor")
        self.setValue(value)
    
    def setValue(self, value):
        if value is None:
            super().setValue(value)
            return
        if value not in [0, 1]:
            raise ValueError("HTP must be either 0 or 1 (or none)")
        super().setValue(value)

class FW(InputValue):
    def __init__(self, value = None):
        super().__init__(code="FW",
                         data_type=float,
                         description="Fan watts if a fan/coil assembly, enter (-) watts if draw thru air flow, enter watts in blow thru, omit if coil only")
        self.setValue(value)

class RFW(InputValue):
    def __init__(self, value = None):
        super().__init__(code="RFW",
                         data_type=float,
                         description="Fan motor position/efficiency (enter 1 when fan motor not in airstream)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value > 1:
            raise ValueError("Fan motor efficiency cannot be greater than 1")
        if value <= 0:
            raise ValueError("Fan motor efficiency cannot be negative")
        super().setValue(value)

class UM(InputValue):
    def __init__(self, value = None):
        super().__init__(code="UM",
                         data_type=str,
                         description="Unit Model, 25 characters maximum")
        self.setValue(value)

    def setValue(self, value):
        if len(value) > 25:
            raise ValueError("Unit Model cannot exceed 25 characters")
        super().setValue(value)

class TAE(InputValue):
    def __init__(self, value = None):
        super().__init__(code="TAE",
                         data_type=float,
                         description="Air Dry Bulb Temperature, F")
        self.setValue(value)

    def setValue(self, value):
        super().setValue(value)

class TWB(InputValue):
    def __init__(self, value = None):
        super().__init__(code="TWB",
                         data_type=float,
                         description="Air Wet Bulb Temperature, F")
        self.setValue(value)

    def setValue(self, value):
        super().setValue(value)

class LT(InputValue):
    def __init__(self, value = None):
        super().__init__(code="LT",
                         data_type=float,
                         description="Liquid Temperature, F, to expansion device")
        self.setValue(value)

    def setValue(self, value):
        super().setValue(value)

class IET(InputValue):
    def __init__(self, value = None):
        super().__init__(code="IET",
                         data_type=float,
                         description="Initial Evaporating Temperature (not lower than -99F), F to 0.10")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < -99:
            raise ValueError("Initial evaporating temperature cannot be lower than -99F")
        super().setValue(value)

class FET(InputValue):
    def __init__(self, value = None):
        super().__init__(code="FET",
                         data_type=float,
                         description="Final Evaporating Temperature F to 0.10")
        self.setValue(value)

    def setValue(self, value):
        super().setValue(value)

class FNO(InputValue):
    def __init__(self, value = None):
        super().__init__(code="FNO",
                         data_type=int,
                         description="Fluid Number (see Page FDP1)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value < 1:
            raise ValueError("Fluid number (see Page FDP1) must be a positive integer")
        super().setValue(value)

class CR(InputValue):
    def __init__(self, value = None):
        super().__init__(code="CR",
                         data_type=float,
                         description="Circulating Rate; enter overfeed rate + 1.0 ")
        self.setValue(value)

    def setValue(self, value):
        super().setValue(value)

class FC(InputValue):
    def __init__(self, value = None):
        super().__init__(code="FC",
                         data_type=float,
                         description="Fin coating factor (See page WD1A)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value <= 0:
            raise ValueError("Circulating fluid specific heat must be greater than 0")
        super().setValue(value)

class FCT(InputValue):
    def __init__(self, value = None):
        super().__init__(code="FCT",
                         data_type=float,
                         description="Fin Coating Thickness, mils x 10")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value <= 0:
            raise ValueError("Fin coating thickness must be greater than 0")
        super().setValue(value)

class P(InputValue):
    def __init__(self, value = None):
        super().__init__(code="P",
                         data_type=float,
                         description=" Altitude in Feet Above Sea Level, thus 5000FT, or Pressure in PSIG, thus 100P")
        self.setValue(value)
    
    def setValue(self, value):
        if isinstance(value, str):
            if value[-2:] == "FT":
                try:
                    altitude = float(value[:-2])
                    if altitude < 0:
                        raise ValueError("Altitude cannot be negative")
                    super().setValue(value)
                except ValueError:
                    raise ValueError("Invalid altitude value")
            elif value[-1:] == "P":
                try:
                    pressure = float(value[:-1])
                    if pressure < 0:
                        raise ValueError("Pressure cannot be negative")
                    super().setValue(value)
                except ValueError:
                    raise ValueError("Invalid pressure value")
            else:
                raise ValueError("P must end with either 'FT' or 'P'")
        
        super().setValue(value)

class INC(InputValue):
    def __init__(self, value = None):
        super().__init__(code="INC",
                         data_type=float,
                         description="Increment between initial and final evaporating temperatures (not less than .1)")
        self.setValue(value)

    def setValue(self, value):
        value = self._coerce(value)
        if value <= 0:
            raise ValueError("Increment between initial and final evaporating temperatures must be greater than 0")
        super().setValue(value)

    def getValue(self):
        return max(super().getValue(), 0.1)