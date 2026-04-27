# ----------------- main.py ------------------
# Author      : Lin Yiyang
# Description : PFC Triaxial Test Simulation.
#               Python Controll Code.
# DateTime    : 2026-04-10
# Language    : Python(PFC6.0 embedded)
# Email       : me@lycarus.cn
# --------------------------------------------

import itasca as it # type: ignore

# ===========import custom py file=========
import importlib

import Python.file
import Python.log
import Python.stepTimeRecord

# reloading is necessary
importlib.reload(Python.file)
importlib.reload(Python.log)
importlib.reload(Python.stepTimeRecord)

from Python.file import get_config, his_to_csv, batch_delete_files
from Python.log import Log
from Python.stepTimeRecord import StepTime, task_context
# =========================================

# ==========Settings=========
inputFile   = 'input.ini'
# ===========================

call_p3dat = lambda path: it.command(f"program call '{path}'")
save_model = lambda file: it.command(f"model save '{file}'")
read_model = lambda file: it.command(f"model restore '{file}'")
set_history_interval = lambda i: it.command(f"history interval {i}")
set = it.fish.set
pfc = it.command

if __name__ == "__main__":
    pfc('program echo false') # turn off echo
    task = StepTime()
    # it.command("python-reset-state false")
    it.command("model new")
    it.command("model title 'Triaxial Test'")

    # ===============pre-processing==================
    # read & load parameters from file
    config = get_config(inputFile)
    logFile = config['logFile']
    log = Log(outputFile=logFile)
    with task_context(task, log, 'Triaxial Test'):
        log.info('Try clean last simulation result file.')
        batch_delete_files(log, ['Result/*.sav', 'Result/*.csv'])

        log.info(config) # pyright: ignore[reportArgumentType]

        # particle size
        set("ball1Radius", config['balls'][0])
        set("ball2Radius", config['balls'][1])
        set('distance', config['distance'])
        set('domainSize', config['wallSize'])
        set('porosity', config['porosity'])
        set('dMax', config['dMax'])
        set('dMin', config['dMin'])
        set('clumpKn', config['clumpKn'])
        set('clumpFric', config['clumpFric'])
        set('density', config['density'])
        set('maxAllowedStrain', config['maxStrain'])
        set('wallFric', config['ballWallFric'])
        set('servoFac', config['servoFac'])
        emod = config['emod']
        kratio = config['kratio']

        # arrlinear parameter
        rrFric = config['rollfric']
        adForce = config['adForce']
        adRange = config['adRange']

        log.info("set seed.")
        it.command(f"model random {config['random']}")

        log.info("load lib codes.")
        call_p3dat('PFC/Lib/utils.fis')
        call_p3dat('PFC/Lib/servo.fis')

        log.info('Preprogress, Set domain.')
        it.command("model domain extent [-domainSize/2] [domainSize/2]")
        it.command("model domain condition destroy")

        log.info('Preprogress, Set cmat.')
        it.command('contact cmat default model linear property kn 5e6') # set defualt model linear, pebble-facet
        it.command(f"contact cmat default type pebble-pebble model arrlinear method deformability emod [{emod}] kratio [{kratio}]  property rr_fric [{rrFric}] adh_f0 [{adForce}] adh_d0 [{adRange}]") # set model, pebble-pebble

        # ===============================================

        log.info("Start main PFC program.")

        with task_context(task, log, 'Generate particles'):
            call_p3dat("PFC/generate.p3dat")
            save_model('Result/initial-state.sav')
            log.info(f"Clump numbers:{it.clump.count()}")

        log.info("Run confining and test circulation.")

        for i in range(1,3+1):
            read_model("Result/initial-state.sav")
            # recalculate history interval
            interval = int(config['interval']/(it.timestep()*config['loadRate']))
            log.info(f'History interval is: {interval}')
            set('epsilonRate', config['loadRate'])
            set_history_interval(interval)

            pressure = float(config[f'confiningPressure{i}'])

            set('confiningPressure', pressure)

            with task_context(task, log, f'Confining {pressure}Pa'):
                call_p3dat(f"PFC/confining.p3dat")
                save_model(f"Result/confining{pressure}.sav")

            with task_context(task, log, f"Exert z velocity"):
                call_p3dat("PFC/triaxialTest.p3dat")
                save_model(f"Result/triaxial{pressure}.sav")

            # output history
            it.command(f"history export 9 vs 6 reverse file '{pressure}.his'") # export zStress vs zEpsilon
            it.command(f"history export 10 file '{pressure}-aratio.his'")   # export aratio vs Step
            # process his to standard csv
            his_to_csv(f'{pressure}.his')
            his_to_csv(f'{pressure}-aratio.his')

    log.info(task) # pyright: ignore[reportArgumentType]
