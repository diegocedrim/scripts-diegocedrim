-- consulta pra gerar o arquivo que lista todos os elementos pra se detectar as batches
select
	p.name project_name,
	r.name element,
	v.order,
	v.author_email,
	ref.id ref_id,
	rt.name type,
	v.id as commit_id,
	v.hash as commit_hash,
	r.id as resource_id
from
	refactored_resource rr
	inner join resource r on (r.id = rr.resource_id)
	inner join version v on (v.id = r.version_id)
	inner join refactoring ref on (ref.id = rr.refactoring_id)
	inner join project p on (v.project_id = p.id)
	inner join refactoring_type rt on (ref.type_id = rt.id)
where
	ref.valid = 1
	and rr.is_before = 1
order by
	p.name, r.name, v.order asc
limit 100000000


--consulta pra pegar os commits em que os devs trabalharam
select
	p.name as project_name,
	v.id as version_id,
	v.author_email,
	v.order
from
	version v
	inner join project p on (p.id = v.project_id)
order by
	p.name, v.order
limit 100000000



-- classificar os batches usando os smells
update batch b set classification = 1
where (select count(*) from anomaly where resource_id = b.initial_resource) >
	  (select count(*) from anomaly where resource_id = b.final_resource);

update batch b set classification = 2
where (select count(*) from anomaly where resource_id = b.initial_resource) <
	  (select count(*) from anomaly where resource_id = b.final_resource);

update batch b set classification = 3
where (select count(*) from anomaly where resource_id = b.initial_resource) =
	  (select count(*) from anomaly where resource_id = b.final_resource);