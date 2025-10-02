import random
import matplotlib.pyplot as plt

random.seed(42)


NUM_INDIVIDUOS = 10
GERACOES = 4

SCALE_FACTOR = 0.5

class Vector():
    def __init__(self, diametro_roda, potencia_motor, capacidade_bateria):
        self.diametro_roda = diametro_roda
        self.potencia_motor = potencia_motor
        self.capacidade_bateria = capacidade_bateria
        
        self.autonomia = capacidade_bateria / (potencia_motor * diametro_roda)
        self.tempo_aceleracao = (capacidade_bateria + diametro_roda) / potencia_motor
    
    # configurando operacoes
    def __add__(self, outro):
        return Vector(
            self.diametro_roda + outro.diametro_roda,
            self.potencia_motor + outro.potencia_motor,
            self.capacidade_bateria + outro.capacidade_bateria
        )
    
    def __sub__(self, outro):
        return Vector(
            self.diametro_roda - outro.diametro_roda,
            self.potencia_motor - outro.potencia_motor,
            self.capacidade_bateria - outro.capacidade_bateria
        )
    
    def __mul__(self, escalar: int | float):
        return Vector(
            self.diametro_roda * escalar,
            self.potencia_motor * escalar,
            self.capacidade_bateria * escalar
        )
        
    def __rmul__(self, escalar):
        self.__mul__(escalar)
        
        
    # configurando operacoes de comparacao
    # def __lt__(self, outro):
       
        
def gerar_individuos(n=10):
    individuos = []
    for _ in range(n):
        diametro_roda = random.uniform(10, 30)  # exemplo: entre 10 e 30
        potencia_motor = random.uniform(50, 200)  # exemplo: entre 50 e 200
        capacidade_bateria = random.uniform(100, 500)  # exemplo: entre 100 e 500
        individuo = Vector(diametro_roda, potencia_motor, capacidade_bateria)
        individuos.append(individuo)
    return individuos

def domina(dominates: Vector, dominated: Vector):
    condicao1 = (dominates.autonomia >= dominated.autonomia and dominates.tempo_aceleracao <= dominated.tempo_aceleracao)
    condicao2 = (dominates.autonomia > dominated.autonomia or dominates.tempo_aceleracao < dominated.tempo_aceleracao)
    return condicao1 and condicao2

def crossover(pop, parent, trial) -> Vector | tuple[Vector, Vector]:
    if random.random() < 0.05:
        capacidade = random.uniform(100, 500)
    elif(random.random() < 0.5):
        capacidade = parent.capacidade_bateria
    else:
        capacidade = trial.capacidade_bateria
    
    if random.random() < 0.05:
        potencia = random.uniform(50, 200)
    elif(random.random() < 0.5):
        potencia = parent.potencia_motor
    else:
        potencia = trial.potencia_motor
    
    if random.random() < 0.05:
        diametro = random.uniform(10, 30)
    elif(random.random() < 0.5):
        diametro = parent.diametro_roda
    else:
        diametro = trial.diametro_roda
        
    new_vector = Vector(diametro, potencia, capacidade)
    
    if domina(new_vector, parent):
        return new_vector
    elif domina(parent, new_vector):
        return parent
    else:
        return (new_vector, parent)

def prune(population, vector_tuple):
    # crowding distance sorting
    pass

def mutacao(pop: list[Vector], scale_factor: int | float):
    for parent_vector, i in enumerate(pop):
        target_vector, random_vector1, random_vector2 = random.sample([ind for ind in pop if ind is not parent_vector], 3)
        trial_vector = target_vector + scale_factor * (random_vector1 - random_vector2)
        new_vector = crossover(pop, parent_vector, trial_vector)
        
        if isinstance(new_vector, Vector):
            pop[i] = new_vector
        elif isinstance(new_vector, tuple):
            prune(pop, new_vector)