# log output
class Log():
    def __init__(self, filename='log.txt'):
        # empty file firs
        open(filename, 'w').close()

        # actually open now
        self.handle = open(filename, 'a')

        # peace of mind
        self('Log initialized')

    def log(self, text):
        self.handle.write('%s\n' % text)

    def __call__(self, *args, **kwargs):
        self.log(*args)