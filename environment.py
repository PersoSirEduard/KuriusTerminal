import datetime

class EnvironmentManager:
    def __init__(self):

        # Hardcoded variables
        self._delta_time = datetime.timedelta(0)
        self._start_time = datetime.datetime(1984, 2, 1, 5)
        self._computer_name = "Winston Smyth"

        self._variables = {}

    def get(self, variable : str):
        if variable == "datetime":
            return self.getSystemTime().strftime("%Y-%m-%d %H:%M:%S")
        elif variable == "uptime":
            return str(self.getRunTime())[:-7]
        elif variable == "computer_name":
            return self._computer_name
        else:
            return self._variables.get(variable, None)
    
    def getAllVars(self):
        dict = self._variables
        dict["datetime"] = self.get("datetime")
        dict["uptime"] = self.get("uptime")
        dict["computer_name"] = self.get("computer_name")
        return dict

    def set(self, variable : str, value : str):
        if variable == "datetime":
            newTime = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            self._delta_time = newTime - datetime.datetime.now()
        elif variable == "computer_name":
            self._computer_name = value[:15] if len(value) > 75 else value
        else:
            self._variables[variable] = value

    def delete(self, variable : str):
        if variable in self._variables:
            self._variables.pop(variable, None)
            return True
        else:
            return False

    def getSystemTime(self):
        return datetime.datetime.now() + self._delta_time

    def getRunTime(self):
        return self.getSystemTime() - self._start_time

    def applyVars(self, text : str):
        text = text.replace(f"%datetime%", self.get("datetime"))
        text = text.replace(f"%uptime%", self.get("uptime"))
        text = text.replace(f"%computer_name%", self.get("computer_name"))

        for variable in self._variables:
            text = text.replace("%" + variable + "%", self._variables[variable])
        
        return text

