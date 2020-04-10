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
    impactSevereCasesByRequestedTime = get15Percent(infectionsByRequestedTime)
    severeImpactSevereCasesByRequestedTime = get15Percent(severeInfectionsByRequestedTime
                                                          )
    hospitalBedsByRequestedTime = getHospitalBedsByRequestedTime(impactSevereCasesByRequestedTime,
                                                                 data['totalHospitalBeds'])
    severeHospitalBedsByRequestedTime = getHospitalBedsByRequestedTime(severeImpactSevereCasesByRequestedTime,
                                                                       data['totalHospitalBeds'])
    output = {
        'data': data,
        'impact': {
            'currentlyInfected': currentlyInfected,
            'infectionsByRequestedTime': infectionsByRequestedTime,
            'severeCasesByRequestedTime': int(impactSevereCasesByRequestedTime),
            'hospitalBedsByRequestedTime': int(hospitalBedsByRequestedTime)
        },
        'severeImpact': {
            'currentlyInfected': severeCurrentlyInfected,
            'infectionsByRequestedTime': severeInfectionsByRequestedTime,
            'severeCasesByRequestedTime': int(severeImpactSevereCasesByRequestedTime),
            'hospitalBedsByRequestedTime': int(severeHospitalBedsByRequestedTime)
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


def get15Percent(infectionsByRequestedTime):
    return float((15 / 100) * float(infectionsByRequestedTime))


def getHospitalBedsByRequestedTime(value, totalHospitalBeds):
    availableBeds = float((35 / 100) * float(totalHospitalBeds))
    return float(availableBeds - float(value))
