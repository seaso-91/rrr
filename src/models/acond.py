from src.models.executable import Executable
from src.models.input import Input, InputRange, InputClass
from src.models.rr_enums import Program, Dat
from pathlib import Path

## FIXME need to add is_required=True to all input initializations where necessary

class ACOND(Executable):
    def __init__(self):

        required_dats = [Dat.COIL, Dat.COIL1, Dat.REF]

        input_sequence = [[TAE(), TWB(), DC(), QL(), VT(), CT(), ISUB(), FSUB(), INC(), FNO(), FC(), FCT(), P()],
                          [N(), QTY(), FPI(), ROWS(), FH(), FL(), CFM(), SA(), CKT1(), CKT2(), NT1(), NT2(), 
                           FIN(), MTL(), T(), GD(), A(), NR(), B(), HDR(), CON(), HTP(), UM()]]

        result_mapping = {
            "QLBTU": 35,
            "QTR": 36,
            "DBL": 37,
            "WG": 40,
            "COILPD": 41,
            "HDRPD": 42,
            "LB/HR": 43,
            "CHRG": 44,
            "LBS FIN": 48,
            "LBS TUB": 49,
            "INT VOL": 51,
            "UM": 54
            }

        super().__init__(
            program=Program.ACOND,
            result_mapping=result_mapping, 
            input_sequence=input_sequence, 
            required_dats=required_dats
            )

class TAE(InputRange):
    def __init__(self):
        super().__init__(code="TAE",
                         data_type=float,
                         description="Air Dry Bulb Temperature, F",
                         is_required=True)

class TWB(InputRange):
    def __init__(self):
        super().__init__(code="TWB",
                         data_type=float,
                         description="Air Wet Bulb Temperature, F",
                         is_required=True)

class DC(InputClass):
    def __init__(self):
        description = "Enter 1 for Dry Coil, 2 for Wet Pan with condensate evaporated, "
        description += "3 for Dry Pan with condensate evaporated, 4 for Evaporative "
        description += "Condenser, or 5 for Wet Pan without condensate evaporated"
        super().__init__(code="DC",
                         data_type=str,
                         description=description,
                         options=['1', '2', '3', '4', '5'],
                         is_required=True
                         )

class QL(InputRange):
    def __init__(self):
        super().__init__(code="QL",
                         data_type=float,
                         description="BTUH from Evaporated Condenate",
                         min_value=0.0,
                        )

class VT(InputRange):
    def __init__(self):
        super().__init__(code="VT",
                         data_type=float,
                         description="Refrigerant Vapor Temperature, F, to the Condenser"
                        )
        
class CT(InputRange):
    def __init__(self):
        super().__init__(code="CT",
                         data_type=float,
                         description="Refrigerant Condensing Temperature, °F to 0.10°",
                         is_required=True)

class ISUB(InputRange):
    def __init__(self):
        super().__init__(code="ISUB",
                         data_type=float,
                         description="Initial Liquid Sub-cooling, °F to 0.10°",
                         is_required=True)

class FSUB(InputRange):
    def __init__(self):
        super().__init__(code="FSUB",
                         data_type=float,
                         description="Final Liquid Sub-cooling, °F to 0.10°",
                         min_value = 0.1,
                         is_required=True)

class INC(InputRange):
    def __init__(self):
        super().__init__(code="INC",
                         data_type=float,
                         description="Increment between ISUB and FSUB, °F to 0.10°",
                         min_value = 0.1,
                         is_required=True)
    
class FNO(InputClass):
    def __init__(self):
        super().__init__(code="FNO",
                         data_type=int,
                         description="Fluid Number (see Page FDP1)",
                         options=[53, 100, 103],
                         is_required=True)

class FC(InputRange):
    def __init__(self):
        super().__init__(code="FC",
                         data_type=float,
                         description="Fin coating factor (See page WD1A)",
                         min_value=0.0,
                         max_value=0.01)

class FCT(InputRange):
    def __init__(self):
        super().__init__(code="FCT",
                         data_type=float,
                         description="Fin Coating Thickness, mils x 10",
                         min_value=0.0)

class P(Input):
    def __init__(self):
        super().__init__(code="P",
                         data_type=float,
                         description=" Altitude in Feet Above Sea Level, thus 5000FT, or Pressure in PSIG, thus 100P",
                         )
    
    def _validate(self, value):
        if not super()._validate(value):
            return False
        if isinstance(value, str):
            if value[-2:] == "FT":
                try:
                    altitude = float(value[:-2])
                    if altitude < 0:
                        raise ValueError("Altitude cannot be negative")
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
        return True

class N(InputRange):
    def __init__(self):
        super().__init__(code="N",
                         data_type=int,
                         description="Coil code",
                         min_value=1,
                         is_required=True)

class QTY(InputRange):
    def __init__(self):
        super().__init__(code="QTY",
                         data_type=int,
                         description="Quantity of coils piped in parallel air and fluid flow",
                         min_value=1)
        
class FPI(InputRange):
    def __init__(self):
        super().__init__(code="FPI",
                         data_type=float,
                         description="Fins per inch",
                         min_value=1.0,
                         max_value=16.0)

class ROWS(InputRange):
    def __init__(self):
        super().__init__(code="ROWS",
                         data_type=float,
                         description="Number of Rows, each coil (accepts partial rows to second decimal)",
                         min_value=0.0)

class FH(InputRange):
    def __init__(self):
        super().__init__(code="FH",
                         data_type=float,
                         description="Fin Height in inches",
                         min_value=0.0)

class FL(InputRange):
    def __init__(self):
        super().__init__(code="FL",
                         data_type=float,
                         description="Fin Length in inches",
                         min_value=0.0)

class CFM(InputRange):
    def __init__(self):
        super().__init__(code="CFM",
                         data_type=float,
                         description="Airflow in Cubic Feet per Minute, total all coils",
                         min_value=0.0)

class SA(InputClass):
    def __init__(self):
        super().__init__(code="SA",
                         data_type=str,
                         description="Enter S for Standard airflow, or A for Actual airflow",
                         options=['S', 'A', None])

class CKT1(InputRange):
    def __init__(self):
        super().__init__(
            code = "CKT1",
            data_type = int,
            description = "Number of ckts. in first ckt.",
            min_value= 1
        )

class CKT2(InputRange):
    def __init__(self):
        super().__init__(
            code = "CKT2",
            data_type = int,
            description = "Number of ckts. in second ckt.",
            min_value= 1
        )

class NT1(InputRange):
    def __init__(self):
        super().__init__(
            code = "NT1",
            data_type = int,
            description = "Number of tubes in first ckt.",
            min_value= 1
        )

class NT2(InputRange):
    def __init__(self):
        super().__init__(
            code = "NT2",
            data_type = int,
            description = "Number of tubes in second ckt.",
            min_value= 1
        )

class FIN(InputRange):
    def __init__(self):
        super().__init__(code="FIN",
                         data_type=float,
                         description="Fin Thickness, mils*10, enter 0 for bare tubes",
                         min_value=0.0)

class MTL(InputClass):
    def __init__(self):
        super().__init__(code="MTL",
                         data_type=int,
                         description="Fin Material; 0 = Aluminum; 1 = Copper; 2 = Carbon Steel 3 = 90/10 Cupronickel; 4 = 302 Stainless Steel; 5 = bare tubes",
                         options=[0, 1, 2, 3, 4, 5])

class T(Input):
    def __init__(self):
        super().__init__(code="T",
                         data_type=str,
                         description="Tube treatement and wall thickness, see documentation for details",
                         )
        
    def _validate(self, value):
        if not super()._validate(value):
            return False
        # the first char must be either Z, F, Y, X, A, L, H, V, N, U, B, S, or I
        # the remaining chars must be a number with or without a decimal
        if value[0] not in ['Z', 'F', 'Y', 'X', 'A', 'L', 'H', 'V', 'N', 'U', 'B', 'S', 'I']:
            raise ValueError("Invalid tube treatment (tube treatment and wall thickness)")
        try:
            if float(value[1:]) < 0:
                raise ValueError("Wall thickness must be greater than or equal to 0 (tube treatment and wall thickness)")
        except ValueError:
            raise ValueError("Invalid wall thickness (tube treatment and wall thickness)")
        return True

class GD(InputRange):
    def __init__(self):
        super().__init__(code="GD",
                         data_type=float,
                         description="Groove Depth in mils",
                         min_value=0.0)

class A(InputRange):
    def __init__(self):
        super().__init__(code="A",
                         data_type=float,
                         description="Ridge apex angle in degrees",
                         min_value=0.0,
                         max_value=180.0)

class NR(InputRange):
    def __init__(self):
        super().__init__(code="NR",
                         data_type=int,
                         description="Number of ridges",
                         min_value=0)

class B(InputRange):
    def __init__(self):
        super().__init__(code="B",
                         data_type=float,
                         description="Lead helix angle in degrees",
                         min_value=0.0,
                         max_value=180.0)

class HDR(Input):
    def __init__(self):
        super().__init__(code="HDR",
                         data_type=str,
                         description="O.D. in 1/8th inches + coil adapter tube fabrication technique, see documentation for details",
                        )

    def _validate(self, value):
        if not super()._validate(value):
            return False
        # the value can be 0, OR...
        # the last character must be either S or E
        # the first characters must be an integer
        if value == "0":
            return True
        if value[-1] not in ['S', 'E']:
            raise ValueError("Invalid tube treatment (HDR). Last character must be either S or E")
        try:
            if int(value[0:-1]) < 0:
                raise ValueError("suction header OD must be greater than 0 (HDR)")
        except ValueError:
            raise ValueError("Invalid suction header OD (HDR)")
        return True

class CON(InputRange):
    def __init__(self):
        super().__init__(code="CON",
                         data_type=int,
                         description="Connection O.D. in 1/8th inches",
                         min_value=0)

class HTP(InputClass):
    def __init__(self):
        super().__init__(code="HTP",
                         data_type=str,
                         description="Enter 1 for Heat Pipe (oil free); omit when matched with a compressor",
                         options=['1'],
                         is_required=False
                         )

class UM(Input):
    def __init__(self):
        super().__init__(code="UM",
                         data_type=str,
                         description="Unit Model, 25 characters maximum",
                         )

    def _validate(self, value):
        if not super()._validate(value):
            return False
        if value is not None and len(value) > 16:
            raise ValueError("Unit Model cannot exceed 16 characters 9 characters are reserved backend purposes. We can increase the length by using a higher base serialization format, but this will require a change to the backend. Please contact support if you need a longer unit model name.")


# class QT(InputRange):
#     def __init__(self):
#         super().__init__(code="QT",
#                          data_type=float,
#                          description="Total Heat Transfer Rate, Btu/hr",
#                          min_value=0.0)

# class QS(InputRange):
#     def __init__(self):
#         super().__init__(code="QS",
#                          data_type=float,
#                          description="Sensible Heat Transfer Rate, Btu/hr",
#                          min_value=0.0)

# class DBL(InputRange):
#     def __init__(self):
#         super().__init__(code="DBL",
#                          data_type=float,
#                          description="Air Dry Bulb Temperature Leaving Coil, F",
#                          )

# class WG(InputRange):
#     def __init__(self):
#         super().__init__(code="WG",
#                          data_type=float,
#                          description="Pressure Drop of Air Across Coil, in. w.g.",
#                          min_value=0.0)

# class COILPD(InputRange):
#     def __init__(self):
#         super().__init__(code="COILPD",
#                          data_type=float,
#                          description="Pressure Drop of Refrigerant Across Coil, psig",
#                          min_value=0.0)

# class HDRPD(InputRange):
#     def __init__(self):
#         super().__init__(code="HDRPD",
#                          data_type=float,
#                          description="Pressure Drop of Refrigerant Across Header, psig",
#                          min_value=0.0)

# class ORIFPD(InputRange):
#     def __init__(self):
#         super().__init__(code="ORIFPD",
#                          data_type=float,
#                          description="Pressure Drop of Refrigerant Across Distributor Orifice, psig",
#                          min_value=0.0)

# class DISTPD(InputRange):
#     def __init__(self):
#         super().__init__(code="DISTPD",
#                          data_type=float,
#                          description="Pressure Drop of Refrigerant Across Distributor Line, psig",
#                          min_value=0.0)

# class LBMIN(InputRange):
#     def __init__(self):
#         super().__init__(code="LB/MIN",
#                          data_type=float,
#                          description="Refrigerant Mass Flow Rate, lb/min",
#                          min_value=0.0)

# class REFVEL(InputRange):
#     def __init__(self):
#         super().__init__(code="REFVEL",
#                          data_type=float,
#                          description="Refrigerant Velocity, ft/sec",
#                          min_value=0.0)

# class CHRG(InputRange):
#     def __init__(self):
#         super().__init__(code="CHRG",
#                          data_type=float,
#                          description="Refrigerant Charge, lb",
#                          min_value=0.0)

# class LBSFIN(InputRange):
#     def __init__(self):
#         super().__init__(code="LBS FIN",
#                          data_type=float,
#                          description="Fin Weight, lb",
#                          min_value=0.0)

# class LBSTUB(InputRange):
#     def __init__(self):
#         super().__init__(code="LBS TUB",
#                          data_type=float,
#                          description="Tube Weight, lb",
#                          min_value=0.0)

# class WBL(InputRange):
#     def __init__(self):
#         super().__init__(code="WBL",
#                          data_type=float,
#                          description="Wet Bulb Temperature Leaving Coil, F",
#                          )

# class LATENT(InputRange):
#     def __init__(self):
#         super().__init__(code="LATENT",
#                          data_type=float,
#                          description="Latent Heat Transfer Rate, Btu/hr",
#                          min_value=0.0)

# class INTVOL(InputRange):
#     def __init__(self):
#         super().__init__(code="INT VOL",
#                          data_type=float,
#                          description="Internal Volume of Coil, in^3",
#                          min_value=0.0)

# class TUBSVAP(Input):
#     def __init__(self):
#         super().__init__(code="TUBSVAP",
#                          data_type=float,
#                          description="FIXME",
#                          )

# class DPL(InputRange):
#     def __init__(self):
#         super().__init__(code="LEV DEW",
#                          data_type=float,
#                          description="Dew Point Temperature Leaving Coil, F",
#                          )
        