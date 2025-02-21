import sys
import os
import platform
import tempfile
import shutil
import argparse
import subprocess
import site
from importlib import reload
import socket

os.chdir(os.path.dirname(__file__))

#region: Check python version
pythonVersion = platform.python_version_tuple()
if (int(pythonVersion[0]) != 3) or (int(pythonVersion[1]) < 6):
    print('Error: Install requires python version 3.6 or newer.')
    print("The latest version of python can be downloaded "
          + "using the following link: https://www.python.org")
    print('\nInstall unsuccessful.')
    quit()
#endregion

#region: Check if QUARC is installed
try:
    from quanser.common import Timeout
except ImportError:

    if os.name == 'nt':

        if 'QUARC_DIR' in os.environ:
            # QUARC installed, but whls have not been setup yet.
            quarcInstalled = True
            whlsPath = os.path.join(os.environ['QUARC_DIR'], 'python')

            # Assume whls files are missing until proven otherwise.
            whlsMissing = True
            if os.path.exists(whlsPath):
                for file in os.listdir(whlsPath):
                    if file.startswith("quanser_api"):
                        filePath = os.path.join(whlsPath, file)
                        subprocess.check_call([
                            sys.executable, '-m', 'pip', 'install',
                            '--upgrade', filePath, '--find-links', whlsPath
                        ])
                        whlsMissing = False
                        break

            if whlsMissing == True:
                print(
                    'Error: QUARC whls files are missing. QUARC or Quanser '
                    + 'Interactive Labs may not be installed properly.'
                )
                print('\nInstall unsuccessful.')
                quit()
        else:
            quarcInstalled = False

        if quarcInstalled == False:
            print(
                'Error: Before running this installer, you must first install '
                + 'either QUARC 2023 or Quanser Interactive Labs. '
            )
            print('\nInstall unsuccessful.')
            quit()
    else:
        print('Please ensure that the QUARC python .whls have been installed.')
#endregion

#region: Parse Command Line Arguments
parser = argparse.ArgumentParser()

parser.add_argument(
    "-i",
    "--install_dir",
    help="path to where QAL should be installed",
    action="store"
)
parser.add_argument(
    "-s",
    "--source",
    help="folder or .zip file to be installed",
    action="store"
)

parser.add_argument(
    "-d",
    "--ignore_dependencies",
    help="skip installing required python packages",
    action="store_true"
)
parser.add_argument(
    "-e",
    "--skip_envvar_setup",
    help="skip setting up required environment variables",
    action="store_true"
)

# TODO: Implement the following control features
# group = parser.add_mutually_exclusive_group()
# group.add_argument(
#     "-u",
#     "--uninstall",
#     help="uninstall",
#     action="store_true"
# )
# group.add_argument(
#     "-m",
#     "--move",
#     help="move current installation to specified new location",
#     action="store"
# )
# group.add_argument(
#     "-r",
#     "--reinstall",
#     help="reinstall",
#     action="store_true"
# )

args = parser.parse_args()
#endregion

#region: Determine Install Location
if args.install_dir is not None:
    install_dir = args.install_dir # XXX Strip Quotes?
else:
    # Default install location is Quanser folder in home directory
    if (os.name == 'nt'):
        install_dir = os.environ['USERPROFILE'] + '/Documents/Quanser/'
    elif (os.name == 'posix'):
        install_dir = os.environ['HOME'] + '/Quanser/'
    else:
        print('Error: Unsupported OS')
        print('\nInstall unsuccessful.')
        quit()

install_dir = os.path.normpath(install_dir)

if 'QAL_DIR' in os.environ:
    # This installer has already completed successfully at some point
    if install_dir != os.environ['QAL_DIR']:
        print('Error: QAL is already installed in a different location.')
        print('Current location: ' + os.environ['QAL_DIR'])
        print('Attempted new location: ' + install_dir)
        print('\nInstall unsuccessful.')
        quit()

    print('')
    confirmation = input(
        'Warning: QAL is already installed at "' + os.environ['QAL_DIR']
        + '". Continuing with this installer will overwrite files from the '
        + 'current installation. Are you sure you want to continue? (y,[n])'
    )
    if 'y' not in confirmation.lower():
        print('Installation cancelled.')
        quit()
elif os.path.isdir(install_dir):
    # The Quanser folder already exists, but we didn't create it
    confirmation = input(
        'Warning: This installer copies the contents of the src directory to '
        + '"' + install_dir + '". Please be aware that this directory already '
        + 'exists and may contain unrelated files that could potentially be '
        + 'overwritten or lost. Are you sure you want to continue? (y,[n])'
    )
    if 'y' not in confirmation.lower():
        print('Installation cancelled.')
        quit()

# Create install directory is it doesn't already exist
if not os.path.isdir(install_dir):
    try:
        os.mkdir(install_dir)
    except:
        print('Error: Invalid install location.')
        print('\nInstall unsuccessful.')
        quit()
#endregion

#region Check Internet Connection
connectedToInternet = False

socket.setdefaulttimeout(5)
try:
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
        ("www.google.com", 80)
    )
    connectedToInternet = True
except socket.error as ex:
    try:
        # Since google is banned in China...
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
            ("www.baidu.com", 80)
        )
        connectedToInternet = True
    except socket.error as ex:
        pass
#endregion

#region: Install Dependencies
packages = [
    'numpy',
    'scipy',
    'pygit2',
    'opencv-python',
    'pytransform3d',
    'matplotlib',
    'PyQt6',
    'pyqtgraph'
]
print('Installing required python packages...')
if not connectedToInternet:
    print(
        'Warning: No internet detected detected.'
        + 'Please ensure the following python packages are installed:')
    print(packages)

    confirmation = input(
        'Would you like to skip this part for now '
        + 'and finish with the rest of the installation? (y,[n])'
    )
    if 'y' not in confirmation.lower():
        print('Installation cancelled.')
        quit()
elif not args.ignore_dependencies:
    try:
        subprocess.check_call([sys.executable,'-m','pip','install'] + packages)
        reload(site)
        # Must be placed here since it gets installed earlier in script
        import pygit2
    except:
        print('Error: Failed to install required python packages '
            + '(Note: this requires a valid internet connection).'
        )
        confirmation = input(
            'Would you like to skip installing dependencies for now '
            + 'and finish with the rest of the installation? (y,[n])'
        )
        if 'y' not in confirmation.lower():
            print('Installation cancelled.')
            quit()
#endregion

#region: Install src Material
if args.source is not None:
    source = args.source
    pass
else:
    source = './src/'

# Check if source exists.
if not os.path.isdir(source):
    print('Error: Invalid install source')
    print('\nInstall unsuccessful.')
    quit()

print("\nInstalling src material...")

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

copytree(source, install_dir)
#endregion

# #region: Install files from GitHub
# print('Installing Quanser virtual libraries...')
# try:
#     tmpdir = tempfile.TemporaryDirectory()
#     pygit2.clone_repository(
#         'https://github.com/quanser/Quanser_Interactive_Labs_Resources.git',
#         tmpdir.name
#     )
#     shutil.copytree(
#         tmpdir.name + '/python/qvl/',
#         os.path.join(install_dir,'libraries/python/qvl'),
#         dirs_exist_ok=True,
#         ignore=shutil.ignore_patterns('.*')
#     )
#     shutil.copytree(
#         tmpdir.name + '/rtmodels/QCar/',
#         os.path.join(install_dir,'libraries/resources/rt_models/qcar'),
#         dirs_exist_ok=True,
#         ignore=shutil.ignore_patterns('.*')
#     )
#     try:
#         tmpdir.cleanup()
#     except:
#         pass
# except:
#     print('Error: Failed to update QuanserVirtualLibraries from GitHub '
#         + '(Note: this requires a valid internet connection). '
#         + 'QVL libraries match the state of the GitHub '
#         + 'repository as of the newest date shown in the changelog. '
#         + 'If you require updated files, please contact tech@quanser.com for '
#         + 'a guide for manually installing the files.'
#     )
#endregion

#region: Setup Environment Variables
environmentVariablesSet = False
if not args.skip_envvar_setup:

    pythonPath = os.path.normpath(install_dir + '/libraries/python/')
    rtmodelsPath = os.path.normpath(
        install_dir + '/libraries/resources/rt_models')

    if os.name == 'nt':
        if not('PYTHONPATH' in os.environ):
            os.system('setx PYTHONPATH "' + pythonPath + '"')
            environmentVariablesSet = True

        elif not(pythonPath in os.environ['PYTHONPATH']):
            pythonPath = os.environ['PYTHONPATH'] + ';' + pythonPath
            os.system('setx PYTHONPATH "' + pythonPath + '"')
            environmentVariablesSet = True

        if not('QAL_DIR' in os.environ):
            os.system('setx QAL_DIR "' + install_dir + '"')
            environmentVariablesSet = True

        if not('RTMODELS_DIR' in os.environ):
            os.system('setx RTMODELS_DIR "' + rtmodelsPath + '"')
            environmentVariablesSet = True

    elif os.name == 'posix':
        shell = os.environ.get('SHELL')
        if shell and 'bash' in shell:
            shellConfigFile = '.bashrc'
        elif shell and 'zsh' in shell:
            shellConfigFile = '.zshrc'
        else:
            print('Error: Unsupported shell interface. '
                +'Only bash and zsh supported.'
            )
            quit()
        configFilePath = os.path.join(os.environ['HOME'], shellConfigFile)

        alreadySetup = False
        if os.path.exists(configFilePath):
            with open(configFilePath, 'r') as config_file:
                for line in config_file.readlines():
                    if 'QAL_DIR' in line.strip():
                        alreadySetup = True
                        break

        if not alreadySetup:
            msg = (
                '\n# Environment variables for Quanser Application Libraries'
                + '\nexport QAL_DIR="' + install_dir + '"'
                + '\nexport PYTHONPATH="${PYTHONPATH}:'+ pythonPath + '"'
                + '\nexport RTMODELS_DIR="' + rtmodelsPath + '"'
            )
            with open(configFilePath, 'a') as config_file:
                config_file.write(msg)
            environmentVariablesSet = True
    else:
        print('Error: unrecognized OS.')
        quit()
#endregion


print('\nInstall Successful!')
print('Location: ' + install_dir)
print('')
if environmentVariablesSet:
    if (os.name == 'nt'):
        print('Windows must be reset in order '
            + 'to finish setup of environment variables.'
        )
    elif (os.name == 'posix'):
        print('Close this terminal and open a new one '
            + 'to finish setup of environment variables.'
        )
    print('')