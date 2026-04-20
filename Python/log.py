from datetime import datetime

class Log:
    def __init__(self, timeFormat='%Y-%m-%d %H:%M:%S', outputFile='', fileOnly=False) -> None:
        '''
        outputFile: print log to a certain file. disabled not specify
        fileOnly:   turn off print on console
        '''
        if outputFile:
            self.file = outputFile
        self.console = not fileOnly
        self.timeFormat = timeFormat

    def info(self, text: str):
        text = f'[Info] {text}'
        self.output(text)

    def warn(self, text: str):
        text = f'[Warn] {text}'

    def error(self, text: str):
        text = f'[Error] {text}'

    def fatal(self, text: str):
        text = f'[Fatal] {text}'

    def output(self, text: str):
        now = datetime.now()
        text = f'[{now.strftime(self.timeFormat)}] {text}'
        if self.console:
            print(text)
        # else:
        #     pass

        if self.file:
            with open(self.file, 'a+') as f:
                f.write(text+'\n')
        # else:
        #     pass