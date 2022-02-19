

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

from collections import Counter


class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)
        
class AssocOne(Association):
    one = dict()

    def __init__(self, e1, assoc, e2):
        if assoc not in AssocOne.one:
            AssocOne.one[assoc] = dict()
        assert e2 not in AssocOne.one[assoc] or AssocOne.one[assoc][e2].entity1 == e1
        AssocOne.one[assoc][e2] = self

        Association.__init__(self, e1, assoc, e2)
#   Exemplo:
#   a = Association('socrates','professor','filosofia')

class AssocNum(Association):
    def __init__(self, e1, assoc, e2):
        assert isinstance(e2, (int, float))
        Association.__init__(self, e1, assoc, e2)


#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None, rel_type=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2)
                and (rel_type == None or type(d.relation) is rel_type) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    ######################################################### EXERCÍCIOS GUIÃO #########################################################

    def list_associations(self):
        return list(set( d.relation.name for d in self.declarations if type(d.relation) is Association ))

    def list_objects(self):
        return list(set( d.relation.entity1 for d in self.declarations if type(d.relation) is Member ))

    def list_users(self):
        return list(set( d.user for d in self.declarations ))

    def list_types(self):
        lst1 = list(set(  d.relation.entity1 for d in self.declarations if type(d.relation) is Subtype ))
        lst2 = list(set(  d.relation.entity2 for d in self.declarations if type(d.relation) in [Member, Subtype] ))
        return list(set( lst1 + lst2 ))

    def list_local_associations(self, entity):
        return list(set( d.relation.name for d in self.declarations if type(d.relation) is Association and d.relation.entity1 == entity ))

    def list_relations_by_user(self, user):
        return list(set( d.relation.name for d in self.declarations if d.user == user ))

    def associations_by_user(self, user):
        return len(list(set( d.relation.name for d in self.declarations if d.user == user and type(d.relation) is Association)))

    def list_local_associations_by_user(self, entity):
        return list(set( (d.relation.name, d.user) for d in self.declarations if type(d.relation) is Association and d.relation.entity1 == entity ))

    def predecessor(self, A, B):

        relations = [d.relation.entity1 for d in self.declarations if type(d.relation) in [Member, Subtype] and d.relation.entity2 == A]

        for entity in relations:
            if entity == B:
                return True

        for entity in relations:
            if self.predecessor(entity, B):
                return True

        return False
        
    def predecessor_path(self, predecessor, entidade):

        relations = [d.relation.entity1 for d in self.declarations if type(d.relation) in [Member, Subtype] and d.relation.entity2 == predecessor]
        lst = None

        for entity in relations:
            if entity == entidade:
                return [predecessor, entidade]

        for entity in relations:
            lst = self.predecessor_path(entity, entidade)

            if lst:
                lst = [predecessor] + lst

        return lst

    def query(self,entity,association=None):

        relations = [d.relation.entity2 for d in self.declarations if type(d.relation) in [Member, Subtype] and d.relation.entity1 == entity]
        declarations = [d for d in self.declarations if type(d.relation) == Association and d.relation.entity1 == entity] if association is None \
            else [d for d in self.declarations if type(d.relation) == Association and d.relation.name == association and d.relation.entity1 == entity]
        for super in relations:
            if self.query(super,association) is not None:
                declarations += self.query(super,association)
        return declarations


    def query2(self,entity,association=None):

        relations = [d.relation.entity2 for d in self.declarations if type(d.relation) in [Member, Subtype] and d.relation.entity1 == entity]
        declarations = [d for d in self.declarations if d.relation.entity1 == entity] if association is None \
            else [d for d in self.declarations if d.relation.name == association and d.relation.entity1 == entity]
        for super in relations:
            if self.query(super,association) is not None:
                declarations += self.query(super,association)
        return declarations

    def query_cancel(self, entity,  associacao):
        
        pds = [self.query_cancel(d.relation.entity2, associacao) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1==entity]

        local = self.query_local(e1=entity, rel=associacao, rel_type=Association)

        pds_query = [d for sublist in pds for d in sublist if d.relation.name not in [l.relation.name for l in local]]

        return pds_query + local
    
    
    # Daqui para baixo, não me apeteceu fazer mais :) portanto, o código que se segue é do grande rei Rui (Rui-FMF no gitbub)
    # Obrigado Rui <3
    
    def query_down(self, entity, assoc_name=None, first=True):
        desc = [self.query_down(d.relation.entity1, assoc_name, first=False) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity2 == entity]

        desc_query = [ d for sublist in desc for d in sublist]

        if first:
            return desc_query

        local = self.query_local(e1=entity, rel=assoc_name)

        return desc_query + local

    def query_induce(self, entity, assoc_name):
        desc = self.query_down(entity, assoc_name)

        for val, _ in Counter([d.relation.entity2 for d in desc]).most_common(1):
            return val
        
        return None

    def query_local_assoc(self, entity, assoc_name):
        local = self.query_local(e1=entity, rel=assoc_name)

        for l in local:
            if isinstance(l.relation, AssocNum):
                values = [d.relation.entity2 for d in local]
                return sum(values)/len(local)
            if isinstance(l.relation, AssocOne):
                val, count = Counter([d.relation.entity2 for d in local]).most_common(1)[0]
                return val, count/len(local)
            if isinstance(l.relation, Association):
                mc = []
                freq = 0
                for val, count in Counter([d.relation.entity2 for d in local]).most_common():
                    mc.append((val, count/len(local)))
                    freq += count/len(local)
                    if freq > 0.75:
                        return mc

    def query_assoc_value(self, E, A):
        local = self.query_local(e1=E, rel=A)

        local_values = [l.relation.entity2 for l in local]

        if len(set(local_values)) == 1:
            return local_values[0]
        
        predecessor = [a for a in self.query(entity=E, association=A) if a not in local]

        predecessor_values = [i.relation.entity2 for i in predecessor]

        def perc(lista, value):
            if lista == []:
                return 0

            return len([l for l in lista if l.relation.entity2 == value])/len(lista)
        
        return max(local_values + predecessor_values, key=lambda v: (perc(local, v)+perc(predecessor, v))/2)
    
# Funcao auxiliar para converter para cadeias de caracteres
# listas cujos elementos sejam convertiveis para
# cadeias de caracteres
def my_list2string(list):
   if list == []:
       return "[]"
   s = "[ " + str(list[0])
   for i in range(1,len(list)):
       s += ", " + str(list[i])
   return s + " ]"
    