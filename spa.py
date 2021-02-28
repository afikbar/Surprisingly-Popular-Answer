

from collections import defaultdict
from typing import Dict, List, Union


class Vote():
    def __init__(self, answer: Union[int, str], confidence: int, meta_judgment: int) -> None:
        """Represents a respondant vote to a question.

        Args:
            answer (int | str): Chosen answer.
            confidence (int): The confidence the respondant has in his answer. Between 1 (guess) and 5 (very high)
            meta_judgment (float): The estimated percentage of other participants who agreed with their answer. between 0 to 1.
        """
        self.answer = answer
        self.confidence = confidence
        self.meta_judgment = meta_judgment

    def __repr__(self) -> str:
        return str(self.__dict__)

    @property
    def normalized_confidence(self) -> float:
        return self.confidence / 5


class AggregatedAnswer():
    def __init__(self, total_respondants: int) -> None:
        """Aggregated Respondants answer.

        Args:
            total_respondants (int): Total amount of respondants in the study.
        """
        self._total_respondants = total_respondants
        self.respondants = 0
        self.meta_judgment = 0
        self.weighted_respondants = 0

    def update(self, vote: Vote) -> 'AggregatedAnswer':
        """Updates the aggregation with a new respondant (inplace).
        Args:
            vote (Vote): Vote to update the aggregation with.

        Returns:
            AggregatedAnswer: The updated AggregatedAnswer.
        """
        self.respondants += 1
        self.weighted_respondants += vote.normalized_confidence
        self.meta_judgment = self.meta_judgment + \
            ((vote.meta_judgment - self.meta_judgment) / self.respondants)
        return self

    def difference(self) -> float:
        """Calculates the difference between the observed popularity and the expected popularity (mean metacognitive judgments).

        Returns:
            float: Difference between observed popularity and expected one.
        """
        return self.ratio - self.mean_meta

    @property
    def ratio(self) -> float:
        return self.respondants / self._total_respondants

    @property
    def mean_meta(self) -> float:
        if self._mean_meta is not None:
            return self._mean_meta
        raise Exception("Mean meta is not set. run calc_mean_meta before!")

    def calc_mean_meta(self, others_agg_answer: List['AggregatedAnswer']) -> float:
        """Calculate the mean metacognitive judgments, weighted by the proportion of participants who gave each answer.
        This method should be called before calling `self.difference()`.
        The mean metacognitive judgments is accessible through `self.mean_meta`.

        Args:
            others_agg_answer (List['AggregatedAnswer']): Other answers AggregatedAnswer object.

        Returns:
            float: The mean metacognitive judgments.
        """
        if not others_agg_answer:
            self._mean_meta = 0
            return 0
        others_meta_comp = [agg.ratio * (1 - agg.meta_judgment)
                            for agg in others_agg_answer]
        self._mean_meta = self.ratio * self.meta_judgment + \
            (sum(others_meta_comp) / len(others_meta_comp))
        return self._mean_meta


def aggregate_answers(votes: List[Vote], verbose=False) -> Dict[Union[str, int], AggregatedAnswer]:

    n = len(votes)
    agg_answers = defaultdict(lambda: AggregatedAnswer(total_respondants=n))
    for vote in votes:
        agg_answers[vote.answer].update(vote)

    if verbose:
        print(
            f"Aggregates answers are: {', '.join(sorted(map(str, agg_answers.keys())))}.")

    return agg_answers


def surprisingly_popular(votes: List[Vote], verbose=False) -> Union[int, str]:
    """Calculates the Suprisingly Popular answer given a list of answers.
    The SPA is the answer which maximizes the difference between the observed popularity, 
    and the `expected` popularity (a weighted mean of metacognitive judgments).

    Args:
        votes (List[Votes]): List of respondant votes to a single question.

    Returns:
        int | str: The Surprisingly Popular answer.
    """

    agg_answers = aggregate_answers(votes, verbose)

    # Calculate Mean Meta Judgment:
    expected = {ans: agg.calc_mean_meta([agg_answers[k] for k in agg_answers if k != ans])
                for ans, agg in agg_answers.items()}

    if verbose:
        for ans, agg in agg_answers.items():
            print(
                f"{agg.ratio} Voted for '{ans}'. Mean-Meta is '{expected[ans]:.3f}'.")
    spa = max(agg_answers, key=lambda ans: agg_answers[ans].difference())
    return spa


def weighted_confidence(votes: List[Vote], verbose=False) -> Union[int, str]:
    agg_answers = aggregate_answers(votes, verbose)
    weighted_confidence = max(
        agg_answers, key=lambda ans: agg_answers[ans].weighted_respondants)

    return weighted_confidence


def plurality(votes: List[Vote], verbose=False) -> Union[int, str]:

    agg_answers = aggregate_answers(votes, verbose)
    plurality = max(agg_answers, key=lambda ans: agg_answers[ans].ratio)

    return plurality
