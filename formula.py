from classiq import RegisterUserInput, construct_grover_model

register_size = RegisterUserInput(size=1)

qmod = construct_grover_model(
    num_reps=1,
    expression="(" + formula + ")",
    definitions=[
        ("x1", register_size),
        ("x2", register_size),
        ("x3", register_size),
    ],
)