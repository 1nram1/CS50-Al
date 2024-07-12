import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

import math

# def gene_num_probability(ori_gene, offer_gene):
#     """
#     Compute the probability of a parent with ori_gene genes 
#     giving or not giving (depends on the variable offer_gene)
#     a mutated gene to his(her) child
#     """
#     if offer_gene:
#         if ori_gene == 0:
#             return PROBS["mutation"]
#         elif ori_gene == 1:
#             return 0.5
#         else :
#             return 1 - PROBS["mutation"]
#     else:
#         if ori_gene == 0:
#             return 1 - PROBS["mutation"]
#         elif ori_gene == 1:
#             return 0.5
#         else :
#             return PROBS["mutation"]

# def joint_probability(people, one_gene, two_genes, have_trait):
#     """
#     Compute and return a joint probability.

#     The probability returned should be the probability that
#         * everyone in set `one_gene` has one copy of the gene, and
#         * everyone in set `two_genes` has two copies of the gene, and
#         * everyone not in `one_gene` or `two_gene` does not have the gene, and
#         * everyone in set `have_trait` has the trait, and
#         * everyone not in set` have_trait` does not have the trait.
#     """
#     names = set(people.keys())
#     conditions = {
#         name:{
#             "gene" : 1 if name in one_gene else
#                      2 if name in two_genes else 0,
#             "trait" : True if name in have_trait else False
#         }
#         for name in names
#     }
#     tot_p = 1
#     for person in names:
#         p = 1
#         p_trait_condi_on_gene = PROBS["trait"][conditions[person]["gene"]][conditions[person]["trait"]]
#         p *= p_trait_condi_on_gene
#         if people[person]["mother"] == people[person]["father"] == None:
#             p_gene = PROBS["gene"][conditions[person]["gene"]]
#             p *= p_gene
#         else:
#             gene_num = conditions[person]["gene"]
#             mum = people[person]["mother"]
#             dad = people[person]["father"]
#             mum_gene = conditions[mum]["gene"]
#             dad_gene = conditions[dad]["gene"]
#             if gene_num == 0:
#                 p *= gene_num_probability(mum_gene, False)
#                 p *= gene_num_probability(dad_gene, False)
#             elif gene_num == 1:
#                 p1 = gene_num_probability(mum_gene, True)*gene_num_probability(dad_gene, False)
#                 p2 = gene_num_probability(mum_gene, False)*gene_num_probability(dad_gene, True)
#                 p *= (p1 + p2)
#             else:
#                 p *= gene_num_probability(mum_gene, True)*gene_num_probability(dad_gene, True)
#         tot_p *= p
#     return tot_p



def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    all_probability = []
    all_situation = dict()
    for person in people.keys():
        if person in one_gene:
            all_situation[person] = "one"
        elif person in two_genes:
            all_situation[person] = "two"
        else:
            all_situation[person] = "zero"
    for person in people.keys():
        this_probability = 1
        mother = people[person]['mother']
        if all_situation[person] == "one":
            #看有无父母信息
            if mother :
                mother_gene = all_situation[mother]
                father_gene = all_situation[people[person]['father']]
                if mother_gene == "one" and father_gene == "one":
                    this_probability = 2 * ((0.5 * (1 - PROBS["mutation"]) + 0.5 * PROBS["mutation"]) * (0.5 * PROBS["mutation"] + 0.5 * (1 - PROBS["mutation"])))
                elif (mother_gene == "one" and father_gene == "two") or (mother_gene == "two" and father_gene == "one"):
                    this_probability = (0.5 * (1 - PROBS["mutation"]) + 0.5 * PROBS["mutation"]) * PROBS["mutation"] + (1 - PROBS["mutation"]) * (0.5 * (1 - PROBS["mutation"]) + 0.5 * PROBS["mutation"])
                elif (mother_gene == "one" and father_gene == "zero") or (mother_gene == "zero" and father_gene == "one"):
                    this_probability = (0.5 * (1 - PROBS["mutation"]) + 0.5 * PROBS["mutation"]) * (1 - PROBS["mutation"]) + PROBS["mutation"] *(0.5 * (1 - PROBS["mutation"]) + 0.5 * PROBS["mutation"])
                elif mother_gene == "two" and father_gene == "two":
                    this_probability = (1 - PROBS["mutation"])  * PROBS["mutation"] * 2
                elif (mother_gene == "two" and father_gene == "zero") or (mother_gene == "zero" and father_gene == "two"):
                    this_probability = (1 - PROBS["mutation"])  * (1 - PROBS["mutation"]) + PROBS["mutation"] * PROBS["mutation"]
                elif mother_gene == "zero" and father_gene == "zero":
                    this_probability = PROBS["mutation"] * (1 - PROBS["mutation"]) * 2    
            else:
                this_probability *= PROBS["gene"][1]
            if person in have_trait:
                this_probability *= PROBS["trait"][1][True]
            else :
                this_probability *= PROBS["trait"][1][False]
        elif all_situation[person] == "two":
            #看有无父母信息
            if mother :
                mother_gene = all_situation[mother]
                father_gene = all_situation[people[person]['father']]
                if mother_gene == "one" and father_gene == "one":
                    this_probability = ((1 - PROBS["mutation"]) * 0.5 + 0.5 * PROBS["mutation"]) ** 2
                elif (mother_gene == "one" and father_gene == "two") or (mother_gene == "two" and father_gene == "one"):
                    this_probability = ((1 - PROBS["mutation"]) * 0.5 + 0.5 * PROBS["mutation"]) * ((1 - PROBS["mutation"]))
                elif (mother_gene == "one" and father_gene == "zero") or (mother_gene == "zero" and father_gene == "one"):
                    this_probability = ((1 - PROBS["mutation"]) * 0.5 + 0.5 * PROBS["mutation"]) * (PROBS["mutation"])
                elif mother_gene == "two" and father_gene == "two":
                    this_probability = (1 - PROBS["mutation"]) * (1 - PROBS["mutation"])
                elif (mother_gene == "two" and father_gene == "zero") or (mother_gene == "zero" and father_gene == "two"):
                    this_probability = (1 - PROBS["mutation"]) * PROBS["mutation"]
                elif mother_gene == "zero" and father_gene == "zero":
                    this_probability = PROBS["mutation"] * PROBS["mutation"]
            else:
                this_probability *= PROBS["gene"][2]
            if person in have_trait:
                this_probability *= PROBS["trait"][2][True]
            else :
                this_probability *= PROBS["trait"][2][False]
        else:
            if mother :
                mother_gene = all_situation[mother]
                father_gene = all_situation[people[person]['father']]
                if mother_gene == "one" and father_gene == "one":
                    this_probability = (0.5 * PROBS["mutation"] + 0.5 * (1 - PROBS["mutation"])) * 2
                elif (mother_gene == "one" and father_gene == "two") or (mother_gene == "two" and father_gene == "one"):
                    this_probability = (0.5 * PROBS["mutation"] + 0.5 * (1 - PROBS["mutation"])) * PROBS["mutation"]
                elif (mother_gene == "one" and father_gene == "zero") or (mother_gene == "zero" and father_gene == "one"):
                    this_probability = (0.5 * PROBS["mutation"] + 0.5 * (1 - PROBS["mutation"])) * (1 - PROBS["mutation"])
                elif mother_gene == "two" and father_gene == "two":
                    this_probability = PROBS["mutation"] * PROBS["mutation"]
                elif (mother_gene == "two" and father_gene == "zero") or (mother_gene == "zero" and father_gene == "two"):
                    this_probability = (1 - PROBS["mutation"]) * PROBS["mutation"]
                elif mother_gene == "zero" and father_gene == "zero":
                    this_probability = (1 - PROBS["mutation"]) * (1 - PROBS["mutation"])
            else:
                this_probability *= PROBS["gene"][0]
            if person in have_trait:
                this_probability *= PROBS["trait"][0][True]
            else :
                this_probability *= PROBS["trait"][0][False]
        all_probability.append(this_probability)
    return math.prod(all_probability)
    


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    people_list = probabilities.keys()
    for person in people_list:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else :
            probabilities[person]["gene"][0] += p
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else :
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    people_list = probabilities.keys()
    for person in people_list:
        sum_value = sum(probabilities[person]["gene"].values())
        probabilities[person]["gene"][2] /= sum_value
        probabilities[person]["gene"][1] /= sum_value
        probabilities[person]["gene"][0] /= sum_value

        # probabilities[person]["gene"] = {key : value / sum_value for key, value in old_dict}
        # old_dict_trait = probabilities[person]["trait"]
        sum_value_trait = sum(probabilities[person]["trait"].values())
        # probabilities[person]["trait"] = {key : value / sum_value_trait for key, value in old_dict_trait}
        probabilities[person]["trait"][True] /= sum_value_trait
        probabilities[person]["trait"][False] /= sum_value_trait
        


if __name__ == "__main__":
    main()
