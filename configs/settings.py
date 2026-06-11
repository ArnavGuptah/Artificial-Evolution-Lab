# ── World ──────────────────────────────────────────────────────────────────────
WORLD_WIDTH          = 1600
WORLD_HEIGHT         = 1200
FPS                  = 30
BG_COLOR             = (12, 12, 22)

# ── Population ─────────────────────────────────────────────────────────────────
INITIAL_ORGANISMS    = 40
MAX_ORGANISMS        = 300
INITIAL_FOOD         = 40
MAX_AGE              = 3000

# ── Food ───────────────────────────────────────────────────────────────────────
FOOD_SPAWN_RATE      = 0.4
FOOD_ENERGY          = 45
FOOD_RADIUS          = 4
FOOD_COLOR           = (60, 200, 90)

# ── Energy ─────────────────────────────────────────────────────────────────────
STARTING_ENERGY      = 100.0
MOVE_ENERGY_BASE     = 0.015
IDLE_ENERGY_BASE     = 0.01
REPRODUCTION_COST    = 25.0
REPRODUCTION_THRESH  = 70.0

# ── Evolution ──────────────────────────────────────────────────────────────────
MUTATION_RATE        = 0.7
MUTATION_STRENGTH    = 0.36
CROSSOVER_RATE       = 0.5
ELITISM_COUNT        = 5

#── Quantum Mutation ──────────────────────────────────────────────────────────────────
QUANTUM_ENTROPY = 0.4
USE_QUANTUM_MUTATION = True