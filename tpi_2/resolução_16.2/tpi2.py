#encoding: utf8

# nome: João António Assis Reis
# nMec: 98474

from semantic_network import *
from bayes_net import *

import math

class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)
        
    # ex1

    def source_confidence(self,user):
        # initialize variables
        correct = 0
        wrong = 0
        
        # all entities and declaraded relations of AssocOne relations
        entities_relations_assocOne =  list(set( (d.relation.entity1, d.relation.name) for d in self.declarations if type(d.relation) is AssocOne ))
        
        for entity, relation in entities_relations_assocOne:
            # all declarations of AssocOne relations that contains the entity as first argument
            assocOne_dcl_by_entity_relation = list(set( d for d in self.declarations if d.relation.entity1 == entity and d.relation.name == relation))
            
            # analyse just the declarations that the introduced user interact
            if any([ d.user == user for d in assocOne_dcl_by_entity_relation ]):
                
                entity2_count = {}  # { entity2: count }
                
                for d in assocOne_dcl_by_entity_relation:
                    e2 = d.relation.entity2
                    if e2 in entity2_count.keys():
                        entity2_count[e2] += 1
                    else:
                        entity2_count.update( { e2 : 1 } )
                    
                # descending sort of entity2_count by value
                entity2_count = dict(sorted(entity2_count.items(), key=lambda x: x[1], reverse=True))
                
                most_common_value = entity2_count[list(entity2_count.keys())[0]]

                list_most_common_entity2 = [ e for e,c in entity2_count.items() if c == most_common_value ] 
                
                # if any query is not None, it means that the user's declaration is correct    
                if any([ self.query_local(user, entity, relation, entity2) != [] for entity2 in list_most_common_entity2]):
                    correct += 1
                else:
                    wrong += 1

        return self.Conf1(correct, wrong)
    
    def Conf1(self, correct, wrong):
        return ( 1 - math.pow(0.75, correct) ) * math.pow(0.75, wrong)
    
    
    # ex2
    
    def query_with_confidence(self,entity,assoc):
        # all parents of entity
        relations = [self.query_with_confidence(d.relation.entity2, assoc) for d in self.declarations if type(d.relation) in [Member, Subtype] and d.relation.entity1 == entity]
        
        # all entities2 of all declaritions with the introduced entity and association
        entities = [d.relation.entity2 for d in self.declarations if type(d.relation) == AssocOne and d.relation.name == assoc and d.relation.entity1 == entity]
        
        # Conf2(n, t), where n = total number of declarations with each entity2 - entities.count(e2) -, and t = total number of declarations - len(entities)
        local_results = { e2 : self.Conf2( entities.count(e2) , len(entities) ) for e2 in set(entities)}
        inherited_results = {}
        
        # for each parent, update inherited_results
        for parent in relations:
            for ent, num in parent.items():
                if ent in inherited_results.keys():
                    inherited_results[ent] += num
                else:
                    inherited_results[ent] = num
                        
        # average the confidence results (i.e. divide by number of parents)
        for ent, num in inherited_results.items():
            inherited_results[ent] = num / len(relations)

        if inherited_results:
            
            if not local_results:
                # if there are no local results, the inherited results should be returned with a discount of 10%
                return { e2 : inherited_results[e2]*0.9  for e2 in inherited_results.keys() }
        
            else:
                # in all other cases, the final confidence values are computed by weighted average, 
                # with 0.9 for the local confidences and 0.1 for the inherited confidences.
                for e2 in inherited_results.keys():
                    if e2 in local_results.keys():
                        local_results[e2] = inherited_results[e2]*0.1 + local_results[e2]*0.9
                        
                    else:
                        local_results[e2] =  inherited_results[e2]*0.1

                for e2 in local_results.keys():
                    if e2 not in inherited_results:
                        local_results[e2] = local_results[e2]*0.9
                        
                return local_results
            
        else:
            # if there are no inherited results, the local results should be returne
            return local_results

    def Conf2(self, n, T):
        return n/(2*T) + (1 - n/(2*T)) * (1 - math.pow(0.95, n)) * math.pow(0.95, T-n)



class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)
        
        
    # ex3

    def individual_probabilities(self):
        # initialize probabilities dictionary
        prob_dic = {}
        
        # for each variable of network
        for var in self.dependencies.keys():
            # list of all others variables of network
            all_other_vars = list(self.dependencies.keys())
            all_other_vars.remove(var)
            
            prob_all_conjuctions = [ self.jointProb( [(var,True)] + conjunction ) for conjunction in self.all_conjunctions(all_other_vars) ]
            
            # calculate prob for each var
            prob_dic[var] = sum( prob_all_conjuctions )
                        
        return prob_dic    
    
    def all_conjunctions(self, lst):
        return [ [(lst[0], bol)] + conj for conj in self.all_conjunctions(lst[1:]) for bol in [True, False]] if len(lst) != 1 else [ [(lst[0], True)], [(lst[0], False)] ]
    
