from setuptools import setup

setup(
    name='Laser-Lithography',
    version='0.0.1',    
    description='Python package that controls the DS102 series motor controller.',
    url='https://gitlab.com/cnu-physics-capstone-design/laser-lithography',
    author='Seungyeop Lee',
    author_email='lsy020206@outlook.kr',
    license='GNU GPL V3',
    install_requires=['numpy', 'pyserial', 'tkinter'],
)