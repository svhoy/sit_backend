import logging
from random import gauss
from typing import Optional

import numpy as np
from scipy.optimize import least_squares

logger = logging.getLogger("gauss_newton_optimizer")


class GaussNewtonOptimizer:
    def optimize(
        self,
        fit_function: callable,
        df_function: Optional[callable],
        initial_guess,
        max_iterations=100,
        tolerance=1e-8,
        method="gn",
        *args,
        **kwargs,
    ):
        measurements = kwargs.get("measurement")
        if method == "gn":
            result = self.gauss_newton(
                fit_function,
                df_function,
                initial_guess,
                max_iterations,
                measurements["time_round_1"],
                measurements["time_round_2"],
                measurements["time_reply_1"],
                measurements["time_reply_2"],
                measurements["real_tof"],
                tolerance,
            )
        if method == "lm":
            result_ls = least_squares(
                fit_function,
                x0=initial_guess,
                jac=df_function,
                method="lm",
                max_nfev=max_iterations,
                args=(
                    measurements["time_round_1"],
                    measurements["time_round_2"],
                    measurements["time_reply_1"],
                    measurements["time_reply_2"],
                    measurements["real_tof"],
                ),
            )
            result = result_ls.x

        return result

    def gauss_newton(
        self,
        fit_function: callable,
        df_function: Optional[callable],
        initial_guess: np.array,
        max_iterations: int,
        time_round_1: float,
        time_round_2: float,
        time_reply_1: float,
        time_reply_2: float,
        real_tof: float,
        tolerance: float,
    ) -> np.ndarray:
        x = initial_guess
        for i in range(max_iterations):
            residuen = fit_function(
                x,
                time_round_1,
                time_round_2,
                time_reply_1,
                time_reply_2,
                real_tof,
            )
            jacobian = df_function(
                x,
                time_round_1,
                time_round_2,
                time_reply_1,
                time_reply_2,
                real_tof,
            )
            delta = np.linalg.solve(
                jacobian.T @ jacobian, -jacobian.T @ residuen
            )
            x = x + delta
            if np.linalg.norm(delta) < tolerance:
                logger.debug(f"Iteration: {i}")
                break

        return x
