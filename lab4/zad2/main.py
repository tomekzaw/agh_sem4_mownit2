from zad2 import *

"""
for density in [0.1, 0.2, 0.4]:
    for neighbourhood_name, neighbourhood in {
        '8-': {
            (-1,-1): -1, (0,-1): -1, (1,-1): -1,
            (-1, 0): -1,             (1, 0): -1,
            (-1, 1): -1, (0, 1): -1, (1, 1): -1
        },
        '8+': {
            (-1,-1): +1, (0,-1): +1, (1,-1): +1,
            (-1, 0): +1,             (1, 0): +1,
            (-1, 1): +1, (0, 1): +1, (1, 1): +1
        }
    }.items():
        run(
            name='512_{}_{}'.format(density, neighbourhood_name),
            width=512,
            height=512,
            density=density,    
            neighbourhood=neighbourhood,
            max_iterations=int(1.5e6),
            temperature=lambda i: 0.99996**i,
            scale=5.0
        )
"""

run(
    name='200_1,-4',
    width=200,
    height=200,
    density=0.5,    
    neighbourhood={
        (0,-3): 1,    
        (0,-2): 1,    
        (0,-1): 1, 
    (-1,0): -4, (1,0): -4,
        (0, 1): 1,
        (0, 2): 1,
        (0, 3): 1
    },
    max_iterations=int(2e6),
    temperature=lambda i: 0.99999**i,
    scale=5.0
)

"""
run(
    name='200_8-,16+',
    width=200,
    height=200,
    density=0.5,    
    neighbourhood={
        (-2,-2): +1, (-1,-2): +1, (0,-2): +1, (1,-2): +1, (2,-2): +1,
        (-2,-1): +1, (-1,-1): -1, (0,-1): -1, (1,-1): -1, (2,-1): +1,
        (-2, 0): +1, (-1, 0): -1,             (1, 0): -1, (2, 0): +1,
        (-2, 1): +1, (-1, 1): -1, (0, 1): -1, (1, 1): -1, (2, 1): +1,
        (-2, 2): +1, (-1, 2): +1, (0, 2): +1, (1, 2): +1, (2, 2): +1,
    },
    max_iterations=int(1e6),
    temperature=lambda i: 0.99999**i,
    scale=5.0
)
"""

"""
run(
    name='200_diag',
    width=200,
    height=200,
    density=0.4,    
    neighbourhood={
        (-2,-2): -1,
        (-1,-1): -1,
        ( 1, 1): -1,
        ( 2, 2): -1,
    },
    max_iterations=int(1.5e6),
    temperature=lambda i: 0.99999**i,
    scale=5.0
)
"""

"""
run(
    name='200_16-',
    width=200,
    height=200,
    density=0.5,    
    neighbourhood={
        (-2,-2):-1, (-1,-2):-1, ( 0,-2):-1, ( 1,-2):-1, ( 2,-2):-1,
        (-2,-1):-1,                                     ( 2,-1):-1,
        (-2, 0):-1,                                     ( 2, 0):-1,
        (-2, 1):-1,                                     ( 2, 1):-1,
        (-2, 2):-1, (-1, 2):-1, ( 0, 2):-1, ( 1, 2):-1, ( 2, 2):-1,
    },
    max_iterations=int(1e6),
    temperature=lambda i: 0.99999**i,
    scale=5.0
)
"""

"""
run(
    name='200_16+',
    width=200,
    height=200,
    density=0.5,    
    neighbourhood={
        (-2,-2): 1, (-1,-2): 1, ( 0,-2): 1, ( 1,-2): 1, ( 2,-2): 1,
        (-2,-1): 1,                                     ( 2,-1): 1,
        (-2, 0): 1,                                     ( 2, 0): 1,
        (-2, 1): 1,                                     ( 2, 1): 1,
        (-2, 2): 1, (-1, 2): 1, ( 0, 2): 1, ( 1, 2): 1, ( 2, 2): 1,
    },
    max_iterations=int(1e6),
    temperature=lambda i: 0.99999**i,
    scale=5.0
)
"""

"""
run(
    name='200_s',
    width=200,
    height=200,
    density=0.5,    
    neighbourhood={
                                (0,-2):-1, (1,-2):-1, (2,-2):-1,
                                (0,-1):-1, (1,-1): 2,
                    (-1, 1): 2, (0, 1):-1,
        (-2, 2):-1, (-1, 2):-1, (0, 2):-1,
    },
    max_iterations=int(1.5e6),
    temperature=lambda i: 0.99999**i,
    scale=5.0
)
"""

"""
run(
    name='200_x_3e5_0.9999',
    width=200,
    height=200,
    density=0.5,    
    neighbourhood={
        (-2,-2): -1, (-1,-2): +1, (0,-2): +1, (1,-2): +1, (2,-2): -1,
        (-2,-1): +1, (-1,-1): -1, (0,-1): +1, (1,-1): -1, (2,-1): +1,
        (-2, 0): +1, (-1, 0): +1,             (1, 0): +1, (2, 0): +1,
        (-2, 1): +1, (-1, 1): -1, (0, 1): +1, (1, 1): -1, (2, 1): +1,
        (-2, 2): -1, (-1, 2): +1, (0, 2): +1, (1, 2): +1, (2, 2): +1,
    },
    max_iterations=int(3e5),
    temperature=lambda i: 0.9999**i,
    scale=5.0
)
"""

"""
run(
    name='200_-',
    width=200,
    height=200,
    density=0.2,    
    neighbourhood={
        (-2,-2): 1, (-1,-2): 1, (0,-2): 1, (1,-2): 1, (2,-2): 1,
        (-2,-1): 1, (-1,-1): 1, (0,-1): 1, (1,-1): 1, (2,-1): 1,
        (-2, 0):-9, (-1, 0):-9,            (1, 0):-9, (2, 0):-9,
        (-2, 1): 1, (-1, 1): 1, (0, 1): 1, (1, 1): 1, (2, 1): 1,
        (-2, 2): 1, (-1, 2): 1, (0, 2): 1, (1, 2): 1, (2, 2): 1,
    },
    max_iterations=int(1e6),
    temperature=lambda i: 0.99999**i,
    scale=5.0
)
"""