# python 3.6 embedded in PFC6.0
import configparser as ini
import itasca as it
import os

run = it.command

def get_config(fileName: str):
    '''
    read config from fileName
    return {
        'balls' : [...],
        'distance' : float
    }
    '''
    config = ini.ConfigParser()
    config.read(fileName, encoding='UTF-8')

    return {
        # clump
        'balls'     : [float(config.get('clump', 'ball1')), float(config.get('clump', 'ball2'))],
        'distance'  : float(config.get('clump', 'distance')),
        'density'   : float(config.get('clump', 'density')),
        'dMax'      : float(config.get('clump', 'maxSize')),
        'dMin'      : float(config.get('clump', 'minSize')),
        'clumpKn'   : float(config.get('clump', 'kn')),
        'clumpFric' : float(config.get('clump', 'fric')),
        'emod'      : float(config.get('clump', 'emod')),
        'kratio'    : float(config.get('clump', 'kratio')),
        # output
        'logFile'   : config.get('output', 'logFile'),
        # pfc
        'random'    : config.get('pfc', 'randomSeed'),
        'porosity'  : float(config.get('pfc', 'initPorosity')),
        'interval'  : float(config.get('pfc', 'recordEpsilonInterval')),
        'loadRate'  : float(config.get('pfc', 'compressRate')),
        'maxStrain'  : float(config.get('pfc', 'maxStrain')),
        # wall settings
        'wallSize'           : float(config.get('wall', 'size')),
        'confiningPressure1' : float(config.get('wall', 'confiningPressure1')),
        'confiningPressure2' : float(config.get('wall', 'confiningPressure2')),
        'confiningPressure3' : float(config.get('wall', 'confiningPressure3')),
        'ballWallFric'       : float(config.get('wall', 'fric')),
        # servo
        'servoFac'  : float(config.get('servo', 'fac')),
    }

def output_history(id: int, filename: str):
    # output a history to csv by id
    # a history data is versus by step
    if not filename.endswith('.csv'):
        filename += '.csv'

    if os.path.exists(filename):
        os.remove(filename)

    run(f"history export {id} file '{filename}'")
    # process file to a standardized csv file
    with open(filename, 'r') as fIn, open(f'{filename}.tmp', 'w') as fOut:
        for line in fIn:
            if '-' in line:
                continue
            elif line:
                lines = line.split()
                newLine = ','.join(lines)
                fOut.write(f"{newLine}\n")

    os.replace(f'{filename}.tmp', filename)

def his_to_csv(hisFile: str):
    csvFile = hisFile.split('.his')[0] + '.csv'
    with open(csvFile, 'w', encoding='UTF-8') as o:
        with open(hisFile, 'r') as i:
            for line in i:
                if '---' in line: 
                    continue # pass "---"" line
                o.write(','.join(line.split()) + '\n')
    os.remove(hisFile) # remove hisfile
    os.rename(csvFile, f"Result/{csvFile}")

if __name__ == "__main__":
    config = get_config("input.ini")
    print(config)