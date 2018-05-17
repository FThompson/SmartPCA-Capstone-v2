from util.time import millis

class Prescription:
    def __init__(self, label, max_dose, dose_window, show_override):
        self.label = label
        self.max_dose = max_dose
        self.dose_window = dose_window
        self.show_override = show_override
        self.last_dose_times = [0] * max_dose

    def get_time_until_next_dose(self):
        if self.last_dose_times[0] > 0:
            for i in range(0, self.max_dose):
                time_since_last_dose = millis() - self.last_dose_times[i]
                time_until_next_dose = self.dose_window * (i + 1) - time_since_last_dose
                if time_until_next_dose >= 0:
                    return time_until_next_dose
        return 0

    def get_available_doses(self):
        available = 0
        now = millis()
        for i in range(0, self.max_dose):
            if self.last_dose_times == 0:
                available += 1
            else:
                current_window = self.dose_window * (i + 1)
                if now - self.last_dose_times[i] > current_window:
                    available += 1
        return available

    def use(self, count):
        for i in range(self.max_dose, 0, -1):
            self.last_dose_times[i] = self.last_dose_times[i - 1]
        now = millis()
        for i in range(0, count):
            self.last_dose_times[i] = now
