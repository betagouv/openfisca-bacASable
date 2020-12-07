from openfisca_france.model.base import Variable, Individu, MONTH

class titre_sejour(Variable):
    value_type = bool
    label ="Bénéficiaire d'un titre de séjour"
    entity = Individu
    definition_period = MONTH
    default_value = False

class actp(Variable):
    value_type = bool
    label ="Bénéficiaire de l'Allocation compensatrice pour tierce personne"
    entity = Individu
    definition_period = MONTH
    default_value = False

class station_debout_penible(Variable):
    value_type = bool
    label = "La station debout est pénible pour cet individu"
    entity = Individu
    definition_period = MONTH
    default_value = False

class refugie(Variable):
    value_type = bool
    label = "La personne est réfugié"
    entity = Individu
    definition_period = MONTH
    default_value = False

class apatride(Variable):
    value_type = bool
    label = "La personne est apatride"
    entity = Individu
    definition_period = MONTH
    default_value = False