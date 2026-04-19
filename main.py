# ----------------- main.py ------------------
# Author      : Lin Yiyang
# Description : PFC Triaxial Test Simulation.
#               Python Controll Code.
# DateTime    : 2026-04-10
# Language    : Python(PFC6.0 embedded)
# Email       : me@lycarus.cn
# --------------------------------------------

import itasca as it

# ===========import custom py file=========
import importlib

import Python.file
import Python.log
import Python.stepTimeRecord

# reloading is necessary
importlib.reload(Python.file)
importlib.reload(Python.log)
importlib.reload(Python.stepTimeRecord)

from Python.file import get_config
from Python.log import Log
from Python.stepTimeRecord import StepTime
# =========================================

# ==========Settings=========
inputFile   = 'input.ini'
# ===========================

call_p3dat = lambda path: it.command(f"program call '{path}'")
save_model = lambda file: it.command(f"model save '{file}'")
read_model = lambda file: it.command(f"model restore '{file}'") 
set = it.fish.set

if __name__ == "__main__":
    task = StepTime()
    taskid = task.start('simulation')
    # it.command("python-reset-state false")
    it.command("model new")
    it.command("model title 'Triaxial Test'")

    # ===============pre-processing==================
    # read & load parameters from file
    config = get_config(inputFile)
    logFile = config['logFile']
    log = Log(outputFile=logFile)
    
    log.info(config)
    
    # particle size
    set("ball1Radius", config['balls'][0])
    set("ball2Radius", config['balls'][1]) 
    set('distance', config['distance'])    
    set('domainSize', config['wallSize'])
    set('porosity', config['porosity'])
    set('rMax', config['rMax'])
    set('rMin', config['rMin'])
    set('clumpKn', config['clumpKn'])
    set('clumpFric', config['clumpFric'])
    
    set('servoFac', config['servoFac'])
    
    set('wallFric', config['wallFric'])
    
    log.info("set seed.")
    it.command(f"model random {config['random']}")
    
    log.info("load lib codes.")
    call_p3dat('PFC/Lib/utils.fis')
    call_p3dat('PFC/Lib/servo.fis')
    
    log.info('Preprogress, Set domain.')
    it.command("model domain extent [-domainSize/2] [domainSize/2]")
    it.command("model domain condition destroy")
    
    log.info('Preprogress, Set cmat.')
    it.command("contact cmat default model linear method deformability emod [1.0e9] kratio [2.0]")
    
    it.command(f"history interval {config['interval']}")
    
    # ===============================================

    log.info("Start main PFC program.")
    
    log.info("Step 1, generate particles")
    s1 = task.start('generate particles')
    call_p3dat("PFC/generate.p3dat")
    save_model('Result/initial-state.sav')
    task.finish(s1)
    log.info(f"Finished Step 1, time cost: {task.cost_time(s1)}")
    log.info(f"Clump numbers:{it.clump.count()}")
    
    log.info("Run inspection program.")
    
    
    for i in range(1,3+1):
        pressure = float(config[f'confiningPressure{i}'])      
        
        read_model("Result/initial-state.sav")
        set('confiningPressure', pressure)
        
        log.info(f'Step 2, exert confining pressure{i}: {pressure} Pa.')
        s2 = task.start('exert confining pressure')
        call_p3dat(f"PFC/confining.p3dat")
        save_model(f"Result/confining{pressure}.sav")
        task.finish(s2)
        log.info(f"Finished Step 2, time cost: {task.cost_time(s2)}")
        
        log.info('step 3, exert z direction velocity.')
        call_p3dat('PFC/inspection.p3dat')
        s3 = task.start('exert z velocity')
        call_p3dat("PFC/triaxialTest.p3dat")
        save_model(f"Result/triaxial{pressure}.sav")
        task.finish(s3)
        log.info(f'Finished Step 3, time cost: {task.cost_time(s3)}')
        
    task.finish(taskid)
    log.info("Simulation finished.")
    log.info(task)
    
    # ===============after-processing================
    # ===============================================

    # it.command("return")