from evolution_simulation import EvolutionSimulation
from simulation import Simulation


def main() -> None:
    s: EvolutionSimulation = EvolutionSimulation()
    # s: Simulation = Simulation()
    s.run()


main()
