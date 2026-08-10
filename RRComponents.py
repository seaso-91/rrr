from enum import Enum

class State(Enum):
    LIQUID = 1
    MIXTURE = 2
    VAPOR = 3

class Property:
    name: str
    description: str
    value: any
    def __init__(self, name: str, description: str, value: any):
        self.name = name
        self.description = description
        self.value = value

class Part:
    def __init__(self, name:str):
        self.name = name
        self.properties = {}

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def getProperty(self, property_name: str):
        return self.properties.get(property_name, None)
    
    def getFields(self):
        return list(self.properties.keys())

class Distributor(Part):
    def __init__(self,
                 orificeNumber,
                 lineOD,
                 lineLength):
        super().__init__(name = "Distributor")
        self.properties["orificeNumber"] = Property(name="orificeNumber", description="FIX_ME", value=orificeNumber)
        self.properties["lineOD"] = Property(name="lineOD", description="Distributor Line OD", value=lineOD)
        self.properties["lineLength"] = Property(name="lineLength", description="Distributor Line Length", value=lineLength)
        
class Header(Part):
    def __init__(self,
                 OD,
                 connectionOD):
        super().__init__(name = "Header")
        self.properties["OD"] = Property(name="OD", description="Header OD", value=OD)
        self.properties["connectionOD"] = Property(name="connectionOD", description="Header Connection OD", value=connectionOD)

class Coil(Part):
    def __init__(self,
                coilCode,
                finnedHeight,
                finnedLength,
                rows,
                finthickness,
                finsPerInch,
                finMaterial,
                finCoatingFactor,
                finCoatingThickness,
                circulatingArraingment,
                tubeTreatmeant,
                wallThickness,
                grooveDepth,
                ridgeApexAngl,
                numberOfRidges,
                leadHelixAngle):
        super().__init__(name = "Coil")
        self.properties["coilCode"] = Property(name="coilCode", description="Coil Code", value=coilCode)
        self.properties["finnedHeight"] = Property(name="finnedHeight", description="Finned Height", value=finnedHeight)
        self.properties["finnedLength"] = Property(name="finnedLength", description="Finned Length", value=finnedLength)
        self.properties["rows"] = Property(name="rows", description="Number of Rows", value=rows)
        self.properties["thickness"] = Property(name="thickness", description="Fin Thickness", value=finthickness)
        self.properties["finsPerInch"] = Property(name="finsPerInch", description="Fins Per Inch", value=finsPerInch)
        self.properties["material"] = Property(name="material", description="Fin Material", value=finMaterial)
        self.properties["finCoatingFactor"] = Property(name="finCoatingFactor", description="Fin Coating Factor", value=finCoatingFactor)
        self.properties["finCoatingThickness"] = Property(name="finCoatingThickness", description="Fin Coating Thickness", value=finCoatingThickness) 
        self.properties["circulatingArrangement"] = Property(name="circulatingArrangement", description="Circulating Arrangement", value=circulatingArraingment)
        self.properties["tubeTreatment"] = Property(name="tubeTreatment", description="Tube Treatment", value=tubeTreatmeant)
        self.properties["wallThickness"] = Property(name="wallThickness", description="Wall Thickness", value=wallThickness)
        self.properties["grooveDepth"] = Property(name="grooveDepth", description="Depth of the groove", value=grooveDepth)
        self.properties["ridgeApexAngle"] = Property(name="ridgeApexAngle", description="Angle of the ridge apex", value=ridgeApexAngl)
        self.properties["numberOfRidges"] = Property(name="numberOfRidges", description="Number of ridges", value=numberOfRidges)
        self.properties["leadHelixAngle"] = Property(name="leadHelixAngle", description="Angle of the lead helix", value=leadHelixAngle)


class Fluid(Part):
    def __init__(self, name:str):
        super().__init__(name)
    
class Air(Fluid):
    def __init__(self,
                 dryBulb,
                 wetBulb,
                 dewPoint,
                 humidity,
                 pressure):
        super().__init__(name = "Air")
        self.properties["dryBulb"] = Property(name="dryBulb", description="Dry Bulb Temperature", value=dryBulb)
        self.properties["wetBulb"] = Property(name="wetBulb", description="Wet Bulb Temperature", value=wetBulb)
        self.properties["dewPoint"] = Property(name="dewPoint", description="Dew Point Temperature", value=dewPoint)
        self.properties["humidity"] = Property(name="humidity", description="Humidity", value=humidity)
        self.properties["pressure"] = Property(name="pressure", description="Pressure", value=pressure) 

class Refrigerant(Fluid):
    def __init__(self,
                 state: State,
                 fluidNumber,
                 liquidTemperature,
                 superheat,
                 evaporatingTemperature,
                 condensingTemperature,
                 saturationTemperature,
                 ):
        super().__init__(name = "Refrigerant")
        self.properties["state"] = Property(name="state", description="State", value=state)
        self.properties["fluidNumber"] = Property(name="fluidNumber", description="Fluid Number", value=fluidNumber)
        self.properties["liquidTemperature"] = Property(name="liquidTemperature", description="Liquid Temperature", value=liquidTemperature)
        self.properties["superheat"] = Property(name="superheat", description="Superheat", value=superheat)
        self.properties["evaporatingTemperature"] = Property(name="evaporatingTemperature", description="Evaporating Temperature", value=evaporatingTemperature)
        self.properties["condensingTemperature"] = Property(name="condensingTemperature", description="Condensing Temperature", value=condensingTemperature)
        self.properties["saturationTemperature"] = Property(name="saturationTemperature", description="Saturation Temperature", value=saturationTemperature)
