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
    output = {
        'data': data,
        'impact': {
            'currentlyInfected': currentlyInfected,
            'infectionsByRequestedTime': infectionsByRequestedTime
        },
        'severeImpact': {
            'currentlyInfected': severeCurrentlyInfected,
            'infectionsByRequestedTime': severeInfectionsByRequestedTime
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
