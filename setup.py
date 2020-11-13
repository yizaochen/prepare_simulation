from setuptools import setup, find_packages

setup(name='simulation', 
      version='0.1',
      packages=find_packages(),
      url='https://github.com/yizaochen/prepare_simulation.git',
      author='Yizao Chen',
      author_email='yizaochen@gmail.com',
      license='MIT',
      install_requires=[
          'jupyterlab',
          'MDAnalysis'
      ]
      )
