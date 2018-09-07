from __future__ import print_function
from ase.test import NotAvailable
from ase.build import bulk
from ase.calculators.calculator import get_calculator


required = {'abinit': dict(ecut=200, toldfe=0.0001, chksymbreak=0),
            'aims': dict(sc_accuracy_rho=5.e-3),
            'elk': dict(tasks=0, rgkmax=5.0),
            'gpaw': dict(mode='pw'),
            'cp2k': dict(auto_write=True, uks=True, max_scf=1, cutoff=400)}


def run(name):
    Calculator = get_calculator(name)
    par = required.get(name, {})
    calc = Calculator(label=name, xc='LDA', kpts=(1, 1, 1), **par)
    al = bulk('AlO', crystalstructure='rocksalt', a=4.5)
    al.calc = calc
    e = al.get_potential_energy()
    calc.set(xc='PBE', kpts=(2, 2, 2))
    epbe = al.get_potential_energy()
    print(e, epbe)
    calc = Calculator(name)
    print(calc.parameters, calc.results, calc.atoms)
    assert not calc.calculation_required(al, ['energy'])
    al = calc.get_atoms()
    print(al.get_potential_energy())
    label = 'dir/' + name + '-2'
    calc = Calculator(label=label, atoms=al, xc='LDA', kpts=1.0, **par)
    print(al.get_potential_energy())
    print(Calculator.read_atoms(label).get_potential_energy())


names = ['openmx']
for name in names:
    try:
        run(name)
    except NotAvailable:
        pass