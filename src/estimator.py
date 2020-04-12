def estimator(data):
    currentlyInfected = covid19ImpactEstimator(data['reportedCases'])
    severeCurrentlyInfected = covid19ImpactEstimator(data['reportedCases'],
                                                     severe=True)
    infectionsByRequestedTime = getInfectionsByRequestedTime(currentlyInfected,
                                                             data['periodType'],
                                                             data['timeToElapse'])
    severeInfectionsByRequestedTime = getInfectionsByRequestedTime(severeCurrentlyInfected,
                                                                   data['periodType'],
                                                                   data['timeToElapse'])
    impactSevereCasesByRequestedTime = getPercent(infectionsByRequestedTime,
                                                  percent=15)
    severeImpactSevereCasesByRequestedTime = getPercent(severeInfectionsByRequestedTime,
                                                        percent=15)
    hospitalBedsByRequestedTime = getHospitalBedsByRequestedTime(impactSevereCasesByRequestedTime,
                                                                 data['totalHospitalBeds'])
    severeHospitalBedsByRequestedTime = getHospitalBedsByRequestedTime(severeImpactSevereCasesByRequestedTime,
                                                                       data['totalHospitalBeds'])
    casesForICUByRequestedTime = getPercent(infectionsByRequestedTime,
                                            percent=5)
    severeCasesForICUByRequestedTime = getPercent(severeInfectionsByRequestedTime,
                                                  percent=5)
    casesForVentilatorsByRequestedTime = getPercent(infectionsByRequestedTime,
                                                    percent=2)
    severeCasesForVentilatorsByRequestedTime = getPercent(severeInfectionsByRequestedTime,
                                                          percent=2)
    numDays = getDays(data['periodType'], data['timeToElapse'])
    dollarsInFlight = getDollars(infectionsByRequestedTime,
                                 data['region']['avgDailyIncomeInUSD'],
                                 data['region']['avgDailyIncomePopulation'],
                                 numDays)
    severeDollarsFlight = getDollars(severeInfectionsByRequestedTime,
                                     data['region']['avgDailyIncomeInUSD'],
                                     data['region']['avgDailyIncomePopulation'],
                                     numDays)
    output = {
        'data': data,
        'impact': {
            'currentlyInfected': currentlyInfected,
            'infectionsByRequestedTime': infectionsByRequestedTime,
            'severeCasesByRequestedTime': int(impactSevereCasesByRequestedTime),
            'hospitalBedsByRequestedTime': int(hospitalBedsByRequestedTime),
            'casesForICUByRequestedTime': int(casesForICUByRequestedTime),
            'casesForVentilatorsByRequestedTime': int(casesForVentilatorsByRequestedTime),
            'dollarsInFlight': int(dollarsInFlight)
        },
        'severeImpact': {
            'currentlyInfected': severeCurrentlyInfected,
            'infectionsByRequestedTime': severeInfectionsByRequestedTime,
            'severeCasesByRequestedTime': int(severeImpactSevereCasesByRequestedTime),
            'hospitalBedsByRequestedTime': int(severeHospitalBedsByRequestedTime),
            'casesForICUByRequestedTime': int(severeCasesForICUByRequestedTime),
            'casesForVentilatorsByRequestedTime': int(severeCasesForVentilatorsByRequestedTime),
            'dollarsInFlight': int(severeDollarsFlight)
        }
    }
    return output


def covid19ImpactEstimator(reportedCases, severe=False):
    if severe:
        return reportedCases * 50
    return reportedCases * 10


def getDays(periodType, value):
    if periodType == 'days':
        return value
    elif periodType == 'weeks':
        return value * 7
    else:
        return value * 30


def getInfectionsByRequestedTime(currentlyInfected, periodType, timeToElapse):
    numDays = getDays(periodType, timeToElapse)
    factor = numDays // 3
    return currentlyInfected * pow(2, factor)


def getPercent(infectionsByRequestedTime, percent):
    return float((percent / 100) * float(infectionsByRequestedTime))


def getHospitalBedsByRequestedTime(value, totalHospitalBeds):
    availableBeds = float((35 / 100) * float(totalHospitalBeds))
    return float(availableBeds - float(value))


def getDollars(infections, avgUSD, avgPop, numDays):
    return float((float(infections) * avgPop * avgUSD) / numDays)
