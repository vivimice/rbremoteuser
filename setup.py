from setuptools import setup

setup(name='rbremoteuser',
      version='0.3',
      description='ReviewBoard RemoteUser Auth Backend',
      author='vivimice',
      author_email='vivimice@gmail.com',
      packages=['rbremoteuser'],
      entry_points={
            'reviewboard.auth_backends' : [
                  'remoteuser = rbremoteuser:RemoteUserBackend',
            ],
      },
      install_requires=['reviewboard >= 2.0'])