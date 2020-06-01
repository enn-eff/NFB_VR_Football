
import platform
import os

# Depending on platform, get paths from environment variables
current_system = platform.system()
if current_system == 'Linux':
    name_env_variable = 'HOME'
elif current_system == 'Windows':
    name_env_variable = 'USERPROFILE'
else:
    raise RuntimeError('Not expected to run on \'' + str(current_system) + '\'')
path_user = os.environ[name_env_variable]


filenames = []
active_objs = []

class TemporaryFile:
    def __init__(self, filename=None, path=None):
        if filename is None or path is None:
            raise ValueError()

        path = self._check_path_shortcut(path)

        self.filename = os.path.join(path, filename)

        # Create the file and immediately close it
        with open(self.filename, 'w') as f:
            pass

        filenames.append(self.filename)

    def append(self, str_append):
        with open(self.filename, 'w') as f:
            str_current = f.read()
            f.write(str_current + str_append)

    def write(self, str_write):
        with open(self.filename, 'w') as f:
            f.write(str_write)

    def _check_path_shortcut(self, path):
        if path == 'user_dir':
            path = path_user

        return path

    def __enter__(self):
        active_objs.append(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        active_objs.remove(self)
        os.unlink(self.filename)


'''
import atexit

def on_exit(filenames, active_objs):
    print(filenames)
    for filename in filenames:
        if os.path.exists(filename):
            print(filename)
            os.unlink(filename)
    #for active_obj in active_objs:
    #    del active_obj


atexit.register(on_exit, filenames, active_objs)
'''
