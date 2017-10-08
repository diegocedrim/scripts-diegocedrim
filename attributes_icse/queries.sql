-- classifica o impacto de cada refatoracao nos atributos
select
	impacts.*,
	case
		when neutral = total then 1 #Não altera nenhum atributo
		when positive = total then 2 #Melhora todos os atributos
		when positive > 0 and neutral = (total - positive) then 3 #Melhora algum atributo e mantém outros
		when negative > 0 and neutral = (total - negative) then 4 #Piora algum atributo e mantém outros
		when negative = total then 5 #Piora todos os atributos
		when positive > (negative + neutral) then 7 #Melhora a maioria
		when negative > (positive + neutral) then 8 #Piora a maioria
		when positive > negative and positive > neutral then 9 # Mais melhora que qualquer coisa
		when negative > positive and negative > neutral then 10 # Mais piora que qualquer coisa
		when negative = positive then 11 # Piora e melhora a mesma quantidade de atributos
		when negative > 0 then 12 #piora pelo menos um
		when positive > 0 then 13 #melhora pelo menos um
	end as impact_id
from
	(select
		ra.refactoring_id,
		ra.positive,
		ra.negative,
		ra.neutral,
		ra.positive + ra.negative + ra.neutral total
	from
		refs_overall_impact_attrs ra
	where
		ra.type = '1-metrics') as impacts;