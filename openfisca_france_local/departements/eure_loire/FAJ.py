# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH


class eure_et_loir_revenus_nets_du_travail(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant des revenus nets du travail"

    def formula(individu, period):
        # Il faudra ajouter des revenus ici
        return individu('salaire_net', period)


class eure_et_loir_eligibilite_FAJ(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité au Fond d'Aide aux Jeunes"

    def formula(individu, period, parameters):
        reside_eure_et_loir = individu.menage('eure_et_loir_eligibilite_residence', period)
        a_entre_18_25_ans = 18 <= individu('age', period) <= 25
        rsa = parameters(period).prestations.minima_sociaux.rsa
        revenue_inferieur_RSA = individu('eure_et_loir_revenus_nets_du_travail', period) < rsa.montant_de_base_du_rsa

        return reside_eure_et_loir * a_entre_18_25_ans * revenue_inferieur_RSA
