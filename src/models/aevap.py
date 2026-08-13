from src.models.rr import Executable
from src.models.input import Input, InputRange, InputClass
from src.models.rr_components import Coil, Distributor, Header, Air, Refrigerant
from src.models.rr_enums import Program, Dat
from pathlib import Path

## FIXME need to add is_required=True to all input initializations where necessary
## FIXME need to add validation to each input, eg self.validate(): super()... more rules...



class AEVAP(Executable):
    def __init__(self):

        required_dats = [Dat.COIL, Dat.COIL1, Dat.REF]

        input_sequence = [[TAE(), TWB(), LT(), IET(), FET(), INC(), FNO(), CR(), FC(), FCT(), P()],
                          [N(), QTY(), FPI(), ROWS(), FH(), FL(), CFM(), SA(), CKT(), DL(), OD(), NZ(), SPHT(),
                           FLO(), FIN(), MTL(), T(), GD(), A(), NR(), B(), HDR(), CON(), FW(), RFW(), UM()]]

        result_mapping = {
            "QT": 38,
            "QS": 39,
            "DBL": 40,
            "WG": 41,
            "COILPD": 42,
            "HDRPD": 43,
            "ORIFPD": 44,
            "DISTPD": 45,
            "LB/MIN": 46,
            "REFVEL": 47,
            "CHRG": 48,
            "LBS FIN": 52,
            "LBS TUB": 53,
            "WBL": 54,
            "LATENT": 55,
            "INT VOL": 56,
            "TUBSVAP": 59,
            "LEV DEW": 60,
            "ERROR": 61,
            "UM": 62
            }

        super().__init__(
            program=Program.AEVAP,
            result_mapping=result_mapping, 
            input_sequence=input_sequence, 
            required_dats=required_dats
            )

    def setCoil(self, coil: Coil):
        self.setInput("FC",coil.finCoatingFactor)
        self.setInput("FCT",coil.finCoatingThickness)
        self.setInput("N",coil.coilCode)
        self.setInput("QTY",coil.quantity)
        self.setInput("FPI",coil.finsPerInch)
        self.setInput("ROWS",coil.rows)
        self.setInput("FH",coil.finnedHeight)
        self.setInput("FL",coil.finnedLength)
        self.setInput("CKT",coil.ckt)
        self.setInput("FLO",coil.circulatingArrangement)
        self.setInput("FIN",coil.thickness)
        self.setInput("MTL",coil.material)
        self.setInput("T",coil.tubeTreatmeant+coil.wallThickness)
        self.setInput("GD",coil.grooveDepth)
        self.setInput("A",coil.ridgeApexAngle)
        self.setInput("NR",coil.numberOfRidges)
        self.setInput("B",coil.leadHelixAngle)
        self.setInput("UM",coil.unitModel)

    def getCoil(self) -> Coil:
        coil = Coil(
            coilCode=self.inputs["N"],
            finnedHeight=self.inputs["FH"],
            finnedLength=self.inputs["FL"],
            rows=self.inputs["ROWS"],
            finthickness=self.inputs["FIN"],
            finsPerInch=self.inputs["FPI"],
            finMaterial=self.inputs["MTL"],
            finCoatingFactor=self.inputs["FC"],
            finCoatingThickness=self.inputs["FCT"],
            circulatingArrangement=self.inputs["FLO"],
            tubeTreatmeant=self.inputs["T"],
            wallThickness=self.inputs["GD"],
            grooveDepth=self.inputs["GD"],
            ridgeApexAngle=self.inputs["A"],
            numberOfRidges=self.inputs["NR"],
            leadHelixAngle=self.inputs["B"]
            )
        return coil

    def setDistributor(self, distributor: Distributor):
        self.setInput("NZ", distributor.orificeNumber)
        self.setInput("OD", distributor.lineOD)
        self.setInput("DL", distributor.lineLength)

    def getDistributor(self) -> Distributor:
        distributor = Distributor(
            orificeNumber=self.inputs["NZ"],
            lineOD=self.inputs["OD"],
            lineLength=self.inputs["DL"]
        )
        return distributor
    
    def setHeader(self, header: Header):
        self.setInput("HDR", header.OD)
        self.setInput("CON", header.connectionOD)

    def getHeader(self) -> Header:
        header = Header(
            OD=self.inputs["HDR"],
            connectionOD=self.inputs["CON"]
        )
        return header
    
    def setEnteringAir(self, enteringAir: Air):
        self.setInput("TAE", enteringAir.temperature)
        self.setInput("TWB", enteringAir.wetBulbTemperature)
        self.setInput("CFM", enteringAir.cfm)
        self.setInput("SA", enteringAir.standardAir)

    def getEnteringAir(self) -> Air:
        enteringAir = Air(
            temperature=self.inputs["TAE"],
            wetBulbTemperature=self.inputs["TWB"],
            cfm=self.inputs["CFM"],
            standardAir=self.inputs["SA"]
        )
        return enteringAir
    
    def setEnteringRefrigerant(self, enteringRefrigerant: Refrigerant):
        self.setInput("LT", enteringRefrigerant.temperature)
        self.setInput("IET", enteringRefrigerant.evaporatingTemperature)
        self.setInput("FET", enteringRefrigerant.evaporatingTemperature)
        self.setInput("FNO", enteringRefrigerant.fluidNumber)
        self.setInput("INC", 1)

    def getEnteringRefrigerant(self) -> Refrigerant:
        enteringRefrigerant = Refrigerant(
            temperature=self.inputs["LT"],
            evaporatingTemperature=self.inputs["IET"],
            fluidNumber=self.inputs["FNO"],
        )
        return enteringRefrigerant

    def setLeavingRefrigerant(self, leavingRefrigerant: Refrigerant):
        self.setInput("SPHT", leavingRefrigerant.superheat)

    def getLeavingRefrigerant(self) -> Refrigerant:
        leavingRefrigerant = Refrigerant(
            temperature=self.inputs["LT"],
            evaporatingTemperature=self.inputs["FET"],
            fluidNumber=self.inputs["FNO"],
            superheat=self.inputs["SPHT"]
        )
        return leavingRefrigerant
    

    def getComponents(self):
        return {
            "coil": self.getCoil(),
            "distributor": self.getDistributor(),
            "header": self.getHeader(),
            "enteringAir": self.getEnteringAir(),
            "leavingAir": self.getLeavingAir(),
            "enteringRefrigerant": self.getEnteringRefrigerant(),
            "leavingRefrigerant": self.getLeavingRefrigerant()
        }




class TAE(InputRange):
    def __init__(self, value = None):
        super().__init__(code="TAE",
                         data_type=float,
                         description="Air Dry Bulb Temperature, F",
                         value=value,
                         is_required=True)


class TWB(InputRange):
    def __init__(self, value = None):
        super().__init__(code="TWB",
                         data_type=float,
                         description="Air Wet Bulb Temperature, F",
                         value=value,
                         is_required=True)

class LT(InputRange):
    def __init__(self, value = None):
        super().__init__(code="LT",
                         data_type=float,
                         description="Liquid Temperature, F, to expansion device",
                         value=value,
                         is_required=True)

class IET(InputRange):
    def __init__(self, value = None):
        super().__init__(code="IET",
                         data_type=float,
                         description="Initial Evaporating Temperature (not lower than -99F), F to 0.10",
                         value=value,
                         min_value = -99.0,
                         is_required=True)

class FET(InputRange):
    def __init__(self, value = None):
        super().__init__(code="FET",
                         data_type=float,
                         description="Final Evaporating Temperature F to 0.10",
                         value=value,
                         min_value = 0.1,
                         is_required=True)

class INC(InputRange):
    def __init__(self, value = None):
        super().__init__(code="INC",
                         data_type=float,
                         description="Increment between initial and final evaporating temperatures (not less than .1)",
                         value=value,
                         min_value = 0.1,
                         is_required=True)

    def getValue(self):
        val = super().getValue()
        if val is None:
            val = 0.1
        return max(val, 0.1)
    
class FNO(InputClass):
    def __init__(self, value = None):
        super().__init__(code="FNO",
                         data_type=int,
                         description="Fluid Number (see Page FDP1)",
                         value=value,
                         options=[53, 100, 103],
                         is_required=True)

class CR(InputRange):
    def __init__(self, value = None):
        super().__init__(code="CR",
                         data_type=float,
                         description="Circulating Rate; enter overfeed rate + 1.0 ",
                         value=value,
                         min_value=0.0,
                         is_required = False)

class FC(InputRange):
    def __init__(self, value = None):
        super().__init__(code="FC",
                         data_type=float,
                         description="Fin coating factor (See page WD1A)",
                         value=value,
                         min_value=0.0,
                         max_value=0.01)

class FCT(InputRange):
    def __init__(self, value = None):
        super().__init__(code="FCT",
                         data_type=float,
                         description="Fin Coating Thickness, mils x 10",
                         value=value,
                         min_value=0.0)

class P(Input):
    def __init__(self, value = None):
        super().__init__(code="P",
                         data_type=float,
                         description=" Altitude in Feet Above Sea Level, thus 5000FT, or Pressure in PSIG, thus 100P",
                         value=value)
    
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

class N(InputRange):
    def __init__(self, value = None):
        super().__init__(code="N",
                         data_type=int,
                         description="Coil code",
                         value=value,
                         min_value=1,
                         is_required=True)

class QTY(InputRange):
    def __init__(self, value = None):
        super().__init__(code="QTY",
                         data_type=int,
                         description="Quantity of coils piped in parallel air and fluid flow",
                         value=value,
                         min_value=1)
        
class FPI(InputRange):
    def __init__(self, value = None):
        super().__init__(code="FPI",
                         data_type=float,
                         description="Fins per inch",
                         value=value,
                         min_value=1.0,
                         max_value=16.0)

class ROWS(InputRange):
    def __init__(self, value = None):
        super().__init__(code="ROWS",
                         data_type=float,
                         description="Number of Rows, each coil (accepts partial rows to second decimal)",
                         value=value,
                         min_value=0.0)

class FH(InputRange):
    def __init__(self, value = None):
        super().__init__(code="FH",
                         data_type=float,
                         description="Fin Height in inches",
                         value=value,
                         min_value=0.0)

class FL(InputRange):
    def __init__(self, value = None):
        super().__init__(code="FL",
                         data_type=float,
                         description="Fin Length in inches",
                         value=value,
                         min_value=0.0)

class CFM(InputRange):
    def __init__(self, value = None):
        super().__init__(code="CFM",
                         data_type=float,
                         description="Airflow in Cubic Feet per Minute, total all coils",
                         value=value,
                         min_value=0.0)

class SA(InputClass):
    def __init__(self, value = None):
        super().__init__(code="SA",
                         data_type=str,
                         description="Enter S for Standard airflow, or A for Actual airflow",
                         value=value,
                         options=['S', 'A', None])

class CKT(InputRange):
    def __init__(self, value = None):
        super().__init__(code="CKT",
                         data_type=int,
                         description="Number of circuits each coil",
                         value=value,
                         min_value=1)

class DL(InputRange):
    def __init__(self, value = None):
        super().__init__(code="DL",
                         data_type=float,
                         description="Length in inches of distributor lines, if no distributor enter 0",
                         value=value,
                         min_value=0.0)

class OD(InputRange):
    def __init__(self, value = None):
        super().__init__(code="OD",
                         data_type=float,
                         description="Distributor Line OD in inches",
                         value=value,
                         min_value=0.0)

class NZ(InputClass):
    def __init__(self, value = None):
        super().__init__(code="NZ",
                         data_type=str,
                         description="Distributor Orifice Number, see documentation for details",
                         value=value,
                         options=["0", ".5",  ".75",  "1",  "1.5", "1.75",  "2",  "2.5",  "3",  "3.5",  "4",  "4.5" , "5",  "6",  "8",  "10",  "12",  "15",  "17",  "20",  "25",  "30",  "35",  "40" , "50", '"V"'])

class SPHT(InputRange):
    def __init__(self, value = None):
        super().__init__(code="SPHT",
                         data_type=float,
                         description="Superheat in degrees Fahrenheit",
                         value=value,
                         min_value=0.0)

class FLO(InputClass):
    def __init__(self, value = None):
        super().__init__(code="FLO",
                         data_type=float,
                         description="Circuiting Arrangement (0 = Cross; 1 = Parallel; 2 = Parallel except superheat in entering air row; -1 = Counter)",
                         value=value,
                         options=[0, 1, 2, -1])

class FIN(InputRange):
    def __init__(self, value = None):
        super().__init__(code="FIN",
                         data_type=float,
                         description="Fin Thickness, mils*10",
                         value=value,
                         min_value=0.0)

class MTL(InputClass):
    def __init__(self, value = None):
        super().__init__(code="MTL",
                         data_type=int,
                         description="Fin Material; 0 = Aluminum; 1 = Copper; 2 = Carbon Steel 3 = 90/10 Cupronickel; 4 = 302 Stainless Steel; 5 = bare tubes",
                         value=value,
                         options=[0, 1, 2, 3, 4, 5])

class T(Input):
    def __init__(self, value = None):
        super().__init__(code="T",
                         data_type=str,
                         description="Tube treatement and wall thickness, see documentation for details",
                         value=value)
        
    def setValue(self, value):
        # the first char must be either Z, F, Y, X, A, L, H, V, N, U, B, S, or I
        # the remaining chars must be a number with or without a decimal
        if value is None:
            super().setValue(value)
            return
        if value[0] not in ['Z', 'F', 'Y', 'X', 'A', 'L', 'H', 'V', 'N', 'U', 'B', 'S', 'I']:
            raise ValueError("Invalid tube treatment (tube treatment and wall thickness)")
        try:
            if float(value[1:]) < 0:
                raise ValueError("Wall thickness must be greater than or equal to 0 (tube treatment and wall thickness)")
        except ValueError:
            raise ValueError("Invalid wall thickness (tube treatment and wall thickness)")
        super().setValue(value)

class GD(InputRange):
    def __init__(self, value = None):
        super().__init__(code="GD",
                         data_type=float,
                         description="Groove Depth in mils",
                         value=value,
                         min_value=0.0)

class A(InputRange):
    def __init__(self, value = None):
        super().__init__(code="A",
                         data_type=float,
                         description="Ridge apex angle in degrees",
                         value=value,
                         min_value=0.0,
                         max_value=180.0)

class NR(InputRange):
    def __init__(self, value = None):
        super().__init__(code="NR",
                         data_type=int,
                         description="Number of ridges",
                         value=value,
                         min_value=0)

class B(InputRange):
    def __init__(self, value = None):
        super().__init__(code="B",
                         data_type=float,
                         description="Lead helix angle in degrees",
                         value=value,
                         min_value=0.0,
                         max_value=180.0)

class HDR(Input):
    def __init__(self, value = None):
        super().__init__(code="HDR",
                         data_type=str,
                         description="O.D. in 1/8th inches + coil adapter tube fabrication technique, see documentation for details",
                         value=value)

    def setValue(self, value):
        if value is None:
            super().setValue(value)
            return
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

class CON(InputRange):
    def __init__(self, value = None):
        super().__init__(code="CON",
                         data_type=int,
                         description="Connection O.D. in 1/8th inches",
                         value=value,
                         min_value=0)

class FW(InputRange):
    def __init__(self, value = None):
        super().__init__(code="FW",
                         data_type=float,
                         description="Fan watts if a fan/coil assembly, enter (-) watts if draw thru air flow, enter watts in blow thru, omit if coil only",
                         value=value)

class RFW(InputRange):
    def __init__(self, value = None):
        super().__init__(code="RFW",
                         data_type=float,
                         description="Fan motor position/efficiency (enter 1 when fan motor not in airstream)",
                         value=value,
                         min_value=0.0,
                         max_value=1.0)

class UM(Input):
    def __init__(self, value = None):
        super().__init__(code="UM",
                         data_type=str,
                         description="Unit Model, 25 characters maximum",
                         value=value)

    def setValue(self, value):
        if value is not None and len(value) > 25:
            raise ValueError("Unit Model cannot exceed 25 characters")
        super().setValue(value)

class QT(InputRange):
    def __init__(self, value = None):
        super().__init__(code="QT",
                         data_type=float,
                         description="Total Heat Transfer Rate, Btu/hr",
                         value=value,
                         min_value=0.0)

class QS(InputRange):
    def __init__(self, value = None):
        super().__init__(code="QS",
                         data_type=float,
                         description="Sensible Heat Transfer Rate, Btu/hr",
                         value=value,
                         min_value=0.0)

class DBL(InputRange):
    def __init__(self, value = None):
        super().__init__(code="DBL",
                         data_type=float,
                         description="Air Dry Bulb Temperature Leaving Coil, F",
                         value=value)

class WG(InputRange):
    def __init__(self, value = None):
        super().__init__(code="WG",
                         data_type=float,
                         description="Pressure Drop of Air Across Coil, in. w.g.",
                         value=value,
                         min_value=0.0)

class COILPD(InputRange):
    def __init__(self, value = None):
        super().__init__(code="COILPD",
                         data_type=float,
                         description="Pressure Drop of Refrigerant Across Coil, psig",
                         value=value,
                         min_value=0.0)

class HDRPD(InputRange):
    def __init__(self, value = None):
        super().__init__(code="HDRPD",
                         data_type=float,
                         description="Pressure Drop of Refrigerant Across Header, psig",
                         value=value,
                         min_value=0.0)

class ORIFPD(InputRange):
    def __init__(self, value = None):
        super().__init__(code="ORIFPD",
                         data_type=float,
                         description="Pressure Drop of Refrigerant Across Distributor Orifice, psig",
                         value=value,
                         min_value=0.0)

class DISTPD(InputRange):
    def __init__(self, value = None):
        super().__init__(code="DISTPD",
                         data_type=float,
                         description="Pressure Drop of Refrigerant Across Distributor Line, psig",
                         value=value,
                         min_value=0.0)

class LBMIN(InputRange):
    def __init__(self, value = None):
        super().__init__(code="LB/MIN",
                         data_type=float,
                         description="Refrigerant Mass Flow Rate, lb/min",
                         value=value,
                         min_value=0.0)

class REFVEL(InputRange):
    def __init__(self, value = None):
        super().__init__(code="REFVEL",
                         data_type=float,
                         description="Refrigerant Velocity, ft/sec",
                         value=value,
                         min_value=0.0)

class CHRG(InputRange):
    def __init__(self, value = None):
        super().__init__(code="CHRG",
                         data_type=float,
                         description="Refrigerant Charge, lb",
                         value=value,
                         min_value=0.0)

class LBSFIN(InputRange):
    def __init__(self, value = None):
        super().__init__(code="LBS FIN",
                         data_type=float,
                         description="Fin Weight, lb",
                         value=value,
                         min_value=0.0)

class LBSTUB(InputRange):
    def __init__(self, value = None):
        super().__init__(code="LBS TUB",
                         data_type=float,
                         description="Tube Weight, lb",
                         value=value,
                         min_value=0.0)

class WBL(InputRange):
    def __init__(self, value = None):
        super().__init__(code="WBL",
                         data_type=float,
                         description="Wet Bulb Temperature Leaving Coil, F",
                         value=value)

class LATENT(InputRange):
    def __init__(self, value = None):
        super().__init__(code="LATENT",
                         data_type=float,
                         description="Latent Heat Transfer Rate, Btu/hr",
                         value=value,
                         min_value=0.0)

class INTVOL(InputRange):
    def __init__(self, value = None):
        super().__init__(code="INT VOL",
                         data_type=float,
                         description="Internal Volume of Coil, in^3",
                         value=value,
                         min_value=0.0)

class TUBSVAP(Input):
    def __init__(self, value = None):
        super().__init__(code="TUBSVAP",
                         data_type=float,
                         description="FIXME",
                         value=value)

class DPL(InputRange):
    def __init__(self, value = None):
        super().__init__(code="LEV DEW",
                         data_type=float,
                         description="Dew Point Temperature Leaving Coil, F",
                         value=value)



if __name__ == "__main__":
    import time
    aevap = AEVAP()
    aevap.setPath(Path.cwd())
    aevap.importData()
    aevap.setInput("UM", f"{time.time()}")
    aevap.input_file.setName(f"test.dat")
    aevap.write()
    aevap.run()