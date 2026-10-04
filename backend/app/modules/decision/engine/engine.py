from app.modules.decision.engine.schemas import (
    OptionInput,
    OptionScore,
    RankedOption,
)


class DecisionEngine:

    def calculate_option_scores(
        self,
        options: list[OptionInput],
    ) -> list[OptionScore]:

        if not options:
            raise ValueError(
                "No decision options provided."
            )

        # Collect metric values across all options
        metric_values: dict[str, list[float]] = {}

        for option in options:

            if not option.metrics:
                raise ValueError(
                    f"Decision option {option.option_id} "
                    "has no metrics."
                )

            for metric in option.metrics:

                metric_values.setdefault(
                    metric.metric_name,
                    []
                ).append(metric.value)

        results: list[OptionScore] = []

        for option in options:

            total_weight = sum(
                metric.weight
                for metric in option.metrics
            )

            if total_weight <= 0:
                raise ValueError(
                    f"Total metric weight for option "
                    f"{option.option_id} must be greater than zero."
                )

            total_score = 0.0

            for metric in option.metrics:

                values = metric_values[
                    metric.metric_name
                ]

                minimum = min(values)
                maximum = max(values)

                # Same value for every option
                if maximum == minimum:

                    normalized = 1.0

                elif metric.direction == "maximize":

                    normalized = (
                        metric.value - minimum
                    ) / (
                        maximum - minimum
                    )

                elif metric.direction == "minimize":

                    normalized = (
                        maximum - metric.value
                    ) / (
                        maximum - minimum
                    )

                else:
                    raise ValueError(
                        f"Invalid metric direction: "
                        f"{metric.direction}"
                    )

                total_score += (
                    normalized * metric.weight
                )

            final_score = self.calculate_final_score(
                weighted_score=total_score,
                total_weight=total_weight,
            )
            results.append(
                OptionScore(
                    option_id=option.option_id,
                    score=final_score,
                )
            )

        return results

    def calculate_final_score(
            self,
            weighted_score: float,
            total_weight:float,
    ) -> float:

        if total_weight <=0:
            raise ValueError(
                "Total Weight must be greater than zero."
            )
        score = weighted_score/total_weight

        return max(0.0, min(1.0 , score))

    def rank_options(
            self,
            scores: list[OptionScore],
    ) -> list[RankedOption]:

        if not scores:
            raise ValueError(
                "No option scores provided."
            )

        sorted_scores = sorted(
            scores,
            key=lambda option: option.score,
            reverse=True


        )

        ranked_option = []

        for rank,option in enumerate(
            sorted_scores,
            start=1,
        ):
            ranked_option.append(
                RankedOption(
                    option_id=option.option_id,
                    score=option.score,
                    rank=rank,
                )
            )

        return ranked_option

    def select_best_option(
        self,
        ranked_options: list[RankedOption],
    ) -> RankedOption:

        if not ranked_options:
            raise ValueError(
                "No ranked options provided."
            )

        best_option = ranked_options[0]

        return RankedOption(
            option_id=best_option.option_id,
            score=best_option.score,
            rank=best_option.rank,
        )