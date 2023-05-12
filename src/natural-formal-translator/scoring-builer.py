from ..common.templates import ScoringBuilder


class LLMScoringBuilder(ScoringBuilder):
    """
                Returns a function which evaluates a user's preferences for an option.
    """

    def build_scoring_model(self, struct_user_state[dict], struct_option_states: list[dict]):  
        ks = struct_user_state.keys()
