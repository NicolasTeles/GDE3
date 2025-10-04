import random
import matplotlib.pyplot as plt
import time



random.seed(42)

NUM_INDIVIDUOS = 3000
GERACOES = 1200

SCALE_FACTOR = 0.5

class Vector():
    def __init__(self, diametro_roda, potencia_motor, capacidade_bateria):
        self.diametro_roda = diametro_roda
        self.potencia_motor = potencia_motor
        self.capacidade_bateria = capacidade_bateria
        
        self.autonomia = capacidade_bateria / (potencia_motor * diametro_roda)
        self.tempo_aceleracao = (capacidade_bateria + diametro_roda) / potencia_motor
        
        self.crowding_distance = None
    
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
        return self.__mul__(escalar)
    
    # sobrescrever comparacao ==
    def __eq__(self, outro):
        return (
            self.diametro_roda == outro.diametro_roda and
            self.potencia_motor == outro.potencia_motor and
            self.capacidade_bateria == outro.capacidade_bateria and
            self.autonomia == outro.autonomia and
            self.tempo_aceleracao == outro.tempo_aceleracao
        )
    
    # sobrescrever comparacao > para comparar crowding distance
    def __gt__(self, outro):
        return self.crowding_distance > outro.crowding_distance
     
    def __repr__(self):
        return f"Vector({self.autonomia}, {self.tempo_aceleracao})"
        
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

def crossover(parent, trial) -> Vector | tuple[Vector, Vector]:
    if(random.random() < 0.5):
        capacidade = parent.capacidade_bateria
    else:
        capacidade = trial.capacidade_bateria
    
    if(random.random() < 0.5):
        potencia = parent.potencia_motor
    else:
        potencia = trial.potencia_motor
    
    if(random.random() < 0.5):
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

def prune(old_population):
    pop = []
    tuples_list = []
    
    for i, ind in enumerate(old_population):
        if isinstance(ind, Vector):
           pop.append(ind)
        elif isinstance(ind, tuple):
            tuples_list.append((i, ind))
            for vec in ind:
                pop.append(vec)
    
    for vector in pop:
        vector.crowding_distance = 0    
    
    # para autonomia
        
    pop.sort(key=lambda sol: sol.autonomia, reverse=True)
    pop[0].crowding_distance, pop[-1].crowding_distance = float('inf'), float('inf')
    
    max, min = pop[0], pop[-1]            
    
    indexes = [pop.index(v) for _idx ,vector_tuple in tuples_list for v in vector_tuple]
    
    for i in indexes:
        if i > 0 and i < len(old_population)-1:
            pop[i].crowding_distance += (pop[i-1].autonomia - pop[i+1].autonomia) / (max.autonomia - min.autonomia)
        
    # para aceleracao
    
    pop.sort(key=lambda sol: sol.tempo_aceleracao)
    pop[0].crowding_distance, pop[-1].crowding_distance = float('inf'), float('inf')
    
    max, min = pop[-1], pop[0]
    
    indexes = [pop.index(v) for _idx, vector_tuple in tuples_list for v in vector_tuple]
    
    for i in indexes:
        if i > 0 and i < len(old_population)-1:
            pop[i].crowding_distance += (pop[i+1].tempo_aceleracao - pop[i-1].tempo_aceleracao) / (max.tempo_aceleracao - min.tempo_aceleracao)
    
    for _idx, vec_tuple in tuples_list:
        for i in indexes:
            if pop[i] == vec_tuple[0]:
                vec_tuple[0].crowding_distance = pop[i].crowding_distance
            if pop[i] == vec_tuple[1]:
                vec_tuple[1].crowding_distance = pop[i].crowding_distance
        
    for idx, vec_tuple in tuples_list:
        if vec_tuple[0] > vec_tuple[1]:
            old_population[idx] = vec_tuple[0]
        else:
            old_population[idx] = vec_tuple[1]

def invalidos(vectors):
    for vector in vectors:
        if vector is None:
            return True
        if not (10 <= vector.diametro_roda <= 30):
            return True
        if not (50 <= vector.potencia_motor <= 200):
            return True
        if not (100 <= vector.capacidade_bateria <= 500):
            return True
    return False
    

def mutar_geracao(pop: list[Vector], scale_factor: int | float):
    for i, parent_vector in enumerate(pop):
        target_vector, random_vector1, random_vector2, trial_vector = None, None, None, None
        while invalidos([trial_vector, ]):
            target_vector, random_vector1, random_vector2 = [v[0] if isinstance(v, tuple) else 
                                                            v for v in random.sample([ind for ind in pop if ind is not parent_vector], 3)]
            trial_vector = target_vector + ( scale_factor * (random_vector1 - random_vector2) )
            
        new_vector = crossover(parent_vector, trial_vector)
        
        pop[i] = new_vector
        
    prune(pop)
            
def plot(pop, filename: str):
    autonomias = [ind.autonomia for ind in pop]
    tempos = [ind.tempo_aceleracao for ind in pop]

    autonomia_range = max(autonomias) - min(autonomias) if len(autonomias) > 1 else 1
    tempo_range = max(tempos) - min(tempos) if len(tempos) > 1 else 1
    fig_width = max(6, autonomia_range)
    fig_height = max(4, tempo_range)

    plt.figure(figsize=(fig_width, fig_height))
    plt.scatter(autonomias, tempos, color='blue', label='Indivíduos')
    plt.xlabel('Autonomia')
    plt.ylabel('Tempo de Aceleração')
    plt.title('Indivíduos: Autonomia vs Tempo de Aceleração')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename+".png")

start = time.process_time()
    
populacao_inicial = gerar_individuos(NUM_INDIVIDUOS)
for i, ind in enumerate(populacao_inicial):
    print(f"Indivíduo {i+1}: diametro_roda={ind.diametro_roda:.2f}, potencia_motor={ind.potencia_motor:.2f}, capacidade_bateria={ind.capacidade_bateria:.2f}")

population = populacao_inicial[:]

for i in range(GERACOES):
    mutar_geracao(population, 0.5)
    print(f"\nFIM DA GERAÇÃO {i+1}\n")

end = time.process_time()

print(f"CPU time: {end - start:.6f} seconds")

plot(populacao_inicial, "populacao inicial")
plot(population, "nova populacao")