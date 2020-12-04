# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH, not_, DIVIDE
from openfisca_france.model.prestations.autonomie import TypesGir


class eure_et_loir_eligibilite_repas_foyer_personne_agee(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité à l'aide Repas Foyer de l'Eure-et-Loir pour les personnes âgées"
    reference = ["Titre 2 Chapitre 1-2 du règlement départementl d'Aide Sociale PA PH de l'Eure-et-Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RDAS_valide__decembre_2019.pdf"
                 ]
    documentation = """
                        Les personnes âgées peuvent bénéficier d’une prise en charge des frais de repas servis par des foyers restaurant créés par les communes, les CCAS ou les CIAS habilités à l’aide sociale. La participation financière du bénéficiaire est déterminée en fonction de ses ressources et du prix du repas.
                        Cette aide fait l’objet d’une récupération sur succession et n’est pas cumulable avec l’Allocation compensatrice pour tierce personne (ACTP), la Majoration Tierce Personne (MTP versée par la CPAM), l’Allocation personnalisée d’autonomie (APA), les prestations d’aide-ménagère servie par les caisses de retraite.
                    """

    def formula(individu, period, parameters):
        age = individu('age', period)
        inapte_travail = individu('inapte_travail', period)
        ressortissant_eee = individu('ressortissant_eee', period)
        gir = individu('gir', period)
        possede_actp = individu('actp', period)
        possede_mtp = individu('mtp', period)
        repas_foyer_parameters = parameters(
            period).departements.eure_et_loir.repas_foyer

        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)
        condition_age = ((age >= repas_foyer_parameters.age_minimal_personne_agee_apte_travail) + (
                age >= repas_foyer_parameters.age_minimal_personne_agee_inapte_travail and inapte_travail))
        condition_nationalite = ressortissant_eee + individu('titre_sejour', period) + individu('refugie',
                                                                                                period) + individu(
            'apatride', period)
        condition_gir = ((gir == TypesGir.gir_5) + (gir == TypesGir.gir_6))
        condition_ressources = individu('asi_aspa_base_ressources_individu',
                                        period) < repas_foyer_parameters.montant_aspa
        conditions_aides_apa = not_(individu('apa_domicile', period.last_month))
        condition_aides_actp = 0 if possede_actp else 1
        condition_aides_mtp = 0 if possede_mtp else 1

        return condition_residence * condition_age * condition_nationalite * condition_gir * condition_ressources * conditions_aides_apa * condition_aides_actp * condition_aides_mtp


class eure_et_loir_eligibilite_repas_foyer_personne_handicape(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir,éligibilité à l'aide Repas Foyer de l'Eure-et-Loir pour les personnes handicapées"
    reference = ["Titre 3 Chapitre 1-2 du règlement départementl d'Aide Sociale PA PH de l'Eure-et-Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RDAS_valide__decembre_2019.pdf"
                 ]
    documentation = """
                        Les personnes en situation de handicap peuvent bénéficier d’une prise en charge des frais de repas servis par des foyers restaurant créés par les communes, les CCAS ou les CIAS habilités à l’aide sociale. 
                        La participation financière du bénéficiaire est déterminée en fonction de ses ressources et du prix du repas.
                        Cette aide n’est pas cumulable avec l’Allocation compensatrice pour tierce personne (ACTP), la Majoration Tierce Personne (MTP versée par la CPAM) et les prestations d’aide-ménagère servies par les caisses de retraite
                    """

    def formula(individu, period, parameters):
        taux_incapacite = individu('taux_incapacite', period)
        restriction_substantielle_durable = individu('aah_restriction_substantielle_durable_acces_emploi', period)
        age = individu('age', period)
        ressortissant_eee = individu('ressortissant_eee', period)
        condition_nationalite = ressortissant_eee + individu('titre_sejour', period) + individu('refugie',period) + individu('apatride', period)

        repas_foyer_parameters = parameters(
            period).departements.eure_et_loir.repas_foyer

        individual_resource_names = {
            'aah',
            'salaire_imposable',
            'retraite_imposable',
            'pensions_invalidite',
            'revenus_stage_formation_pro'
        }
        ressources_famille = {'aspa'}
        ressources_annuelles = {'retraite_complementaire_artisan_commercant',
                                'retraite_complementaire_profession_liberale'
                                }
        individu_resources_month = sum(
            sum([individu(resource, period.last_month) for resource in individual_resource_names]),
            sum([individu.famille(resource, period.last_month) for resource in ressources_famille]))
        individu_resources = sum(individu_resources_month, sum(
            [individu(resource, period, options=[DIVIDE]) for resource in ressources_annuelles]))

        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)
        condition_age = repas_foyer_parameters.age_minimal_personne_handicap
        condition_nationalite = ressortissant_eee + individu('titre_sejour', period) + individu('refugie',period) + individu('apatride', period)
        condition_taux_incapacite = ((taux_incapacite >= repas_foyer_parameters.taux_incapacite_superieur)
                                     + (
                                                 taux_incapacite < repas_foyer_parameters.taux_incapacite_maximum_restriction_acces_emploi and taux_incapacite > repas_foyer_parameters.taux_incapacite_minimum_restriction_acces_emploi and restriction_substantielle_durable))
        condition_ressources = individu_resources < repas_foyer_parameters.montant_aspa

        return condition_residence * condition_age * condition_nationalite * condition_taux_incapacite * condition_ressources
