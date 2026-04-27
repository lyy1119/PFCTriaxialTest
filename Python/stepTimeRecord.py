from datetime import datetime
from contextlib import contextmanager
from typing import Generator, Any

@contextmanager
def task_context(st_instance: Any, log: Any, name: str) -> Generator[int, None, None]:
    """
    Context manager compatible with Python 3.6.

    Args:
        st_instance: Instance of StepTime.
        log: Instance of Log.
        name: Task name string.
    """
    # Use f-strings (Supported in 3.6+)
    log.info(f"Start task: {name}")

    # st_instance.start returns an int
    stepId = st_instance.start(name)

    try:
        yield stepId
    finally:
        # Ensure finish is called even if an exception occurs
        st_instance.finish(stepId)
        log.succ(f"Finish task: {name}, time cost: {st_instance.cost_time(stepId)}")

# Standard usage in Python 3.6
# with task_context(st, logger, "Legacy_Process") as sid:
#     print(f"Executing step {sid}")

class StepTime():
    def __init__(self):
        self.timeList = []
        self.length = 0

    def step_id_check(self, step: int):
        if step < 0:
            raise ValueError('Step id should larger than 0.')
        if step >= self.length:
            raise ValueError(f'Step id: {step} is not recorded. The max Step id is {self.length - 1}.')

    def start(self, name='New Step'):
        t = {
            'start': datetime.now(),
            # 'end' : time,
            'name' : name
        }
        self.timeList.append(t)
        self.length += 1
        return self.length - 1

    def finish(self, step: int):
        self.step_id_check(step)
        self.timeList[step]['end'] = datetime.now()

    def cost_time(self, step: int):
        self.step_id_check(step)
        t = self.timeList[step]
        if not 'end' in t.keys():
            raise NameError(f'Current Step({step}) not ended.')
        return t['end'] - t['start']

    def __len__(self):
        return self.length

    def __str__(self):
        string = []
        for i in self.timeList:
            name  = i['name'];
            start = i['start']
            end   = i.get('end', False)
            cost  = end - start if end else 'Not Ended.'
            string.append(f'Step: {name} \t | Started at {start} \t | Ended at {end} \t | Time cost: {cost}')
        return '\n'.join(string)

if __name__ == '__main__':
    import time
    st = StepTime()

    s1 = st.start('step 1')
    time.sleep(1)
    st.finish(s1)

    s2 = st.start('s2')
    time.sleep(5)
    st.finish(s2)

    print(f'step2 cost {st.cost_time(s2)}')

    print('StepTime Table:')
    print(st)