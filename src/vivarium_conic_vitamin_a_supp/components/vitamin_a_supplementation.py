import numpy as np


class MagicWandSupplementationInterventionStepWise:
    """
    This magic wand component increases coverage of intervention with the ability to specify when the intervention starts and ends.
    Intervention increases by equal chunks each year by difference between baseline and target

    Required:
    target_coverage: value by intervention year end that the coverage should reach (0-1)
    intervention_year_start:
    intervention_year_end:
    affected_value: this is actual changed value in the simulation
    """

    configuration_defaults = {
        'vitamin_a_supplementation': {
            'target_coverage': 0,
            'affected_value': 'lack_of_vitamin_a_supplementation.exposure_parameters',
            'intervention_start_year': 2010,
            'intervention_end_year': 2010,
        }
    }
    
    @property
    def name(self):
        return 'vitamin_a_supplementation_magic_wand_intervention_stepwise'

    def setup(self, builder):
        self.config = builder.configuration.vitamin_a_supplementation
        
        if self.config.target_coverage == 'baseline':
            pass
        else:
            baseline_coverage = builder.data.load('population.demographic_dimensions')
            baseline_coverage['parameter'] = 'cat2'
            baseline_coverage['value'] = 1 - builder.configuration.lack_of_vitamin_a_supplementation.exposure
            
            target = self.config.target_coverage
            start_year = self.config.intervention_start_year
            end_year = self.config.intervention_end_year
            
            if target == 'baseline':
                pass
            else:
                def delta_coverage(x):
                    return (target - x) / (end_year - start_year + 1)

                baseline_coverage['value'] = baseline_coverage.value.apply(delta_coverage)
                
                self.baseline_coverage = builder.lookup.build_table(baseline_coverage)
                self.clock = builder.time.clock()
                self.intervention_start_year = start_year
                self.intervention_end_year = end_year
                
                self.intervention_effect = self.get_intervention_effect(builder)
                builder.value.register_value_modifier(self.config.affected_value, modifier=self.intervention_effect)
    
    def adjust_exposure_parameters(self, index, rates):
        return self.intervention_effect(index, rates)
    
    def get_intervention_effect(self, builder):
        clock = builder.time.clock()
        start_year = self.intervention_start_year
        end_year = self.intervention_end_year
        intervention_step_size = self.baseline_coverage
        
        def adjust_exposure(index, exposure):
            current_year = clock().year
            if current_year >= start_year and current_year <= end_year:
                step_sizes = intervention_step_size(index).value
                
                exposure -= np.maximum(0, step_sizes * (current_year - start_year + 1))
            return exposure
        
        return adjust_exposure
