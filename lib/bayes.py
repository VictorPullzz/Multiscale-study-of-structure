from skopt.space import Real, Integer
from skopt import gp_minimize


def optimizable(n_calls=100,
                n_random_starts=10,
                random_state=42,
                verbose=True,
                n_jobs=-1):
    '''Decorator that make any function returning single numerical value
    optimizable, i.e. perform bayesian optimization of its parameters
    if they are passed as tuples of boundaries. This will fail if
    function requiers tuples as parameters.
    '''
    def optimizable_decorator(function):
        def optimizable_wrapper(*args, **kwargs):
            map = []
            bounds = []
            for i, arg in enumerate(args):
                if isinstance(arg, tuple):
                    if len(arg) == 2:
                        if isinstance(arg[0], float) or isinstance(arg[1], float):
                            map.append(i)
                            bounds.append(Real(*arg))
                        elif isinstance(arg[0], int) and isinstance(arg[1], int):
                            map.append(i)
                            bounds.append(Integer(*arg))
            # TODO: if map (or bounds) list is empty, then just call function once
            if (len(map) == 0):
                return function(*args, **kwargs)
            def objective(params):
                new_args = list(args)
                for i, p in zip(map, params):
                    new_args[i] = p
                return function(*new_args, **kwargs)
            return gp_minimize(objective,
                               bounds,
                               n_calls=n_calls,
                               n_random_starts=n_random_starts,
                               verbose=verbose,
                               random_state=random_state,
                               n_jobs=n_jobs)
            # for kwarg in kwargs:
            #     arg = kwargs[kwarg]
            #     if isinstance(arg, tuple):
            #         if len(arg) == 2:
            #             if isinstance(arg[0], float) or isinstance(arg[1], float):
            #                 print('Real bounds detected!')
            #             elif isinstance(arg[0], int) and isinstance(arg[1], int):
            #                 print('Int bounds detected!')
        return optimizable_wrapper
    return optimizable_decorator
