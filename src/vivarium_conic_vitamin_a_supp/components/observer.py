from collections import Counter

import pandas as pd

from vivarium_public_health.metrics.utilities import QueryString, get_output_template, get_age_bins, get_group_counts


class SupplementedDaysObserver:

    configuration_defaults = {
        'metrics': {
            'supplemented_days': {
                'by_age': False,
                'by_year': False,
                'by_sex': False
            }
        }
    }

    def __init__(self):
        self.measure_name = 'supplemented_days'

    @property
    def name(self, ):
        return 'supplemented_days_observer'

    def setup(self, builder):
        self.config = builder.configuration.metrics.supplemented_days
        self.step_size = builder.time.step_size()
        self.age_bins = get_age_bins(builder)

        self.lack_of_vitamin_a_supplementation = builder.value.get_value("lack_of_vitamin_a_supplementation.exposure")
        self.supplemented_days = Counter()

        columns_required = ['tracked', 'alive']
        if self.config.by_age:
            columns_required += ['age']
        if self.config.by_sex:
            columns_required += ['sex']
        self.population_view = builder.population.get_view(columns_required)

        builder.event.register_listener('collect_metrics', self.on_collect_metrics)
        builder.value.register_value_modifier('metrics', self.metrics)

    def on_collect_metrics(self, event):
        pop = self.population_view.get(event.index)
        current_lack_of_supplementation_exposure = self.lack_of_vitamin_a_supplementation(pop.index)

        # cat 1 represents the exposure to lack of vitamin a supplementation
        # therefore cat 2 is "being supplemented"
        current_supplemented_pop = pop.loc[current_lack_of_supplementation_exposure == 'cat2']

        config = self.config.to_dict().copy()
        base_filter = QueryString(f'alive == "alive" and tracked')
        base_key = get_output_template(**config).substitute(measure=self.measure_name, year=event.time.year)
        current_supplemented_count = get_group_counts(current_supplemented_pop, base_filter, base_key,
                                              config, self.age_bins)
        current_supplemented_count = {k: v * self.step_size().days for k, v in current_supplemented_count.items()}
        self.supplemented_days.update(current_supplemented_count)

    def metrics(self, index: pd.Index, metrics: dict):
        metrics.update(self.supplemented_days)
        return metrics
