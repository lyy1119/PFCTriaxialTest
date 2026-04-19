from datetime import datetime

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