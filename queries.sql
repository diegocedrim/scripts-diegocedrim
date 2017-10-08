-- cria uma tabela temporária com todas as refatorações feitas em aglomerações simples:
-- feitas em elementos que, somando, tem mais de 1 smell
create table refactorings_in_agglomerations as (
select ref_id from (
	select ref_id, sum(smells_count) smells_all_resources from
		(select
			r.id ref_id,
			rsc.id resource_id,
			(select count(*) from anomaly where resource_id = rsc.id) smells_count
		from
			refactoring r
			inner join refactored_resource rr on (rr.refactoring_id = r.id)
			inner join resource rsc on (rsc.id = rr.resource_id)
		where
			rr.is_before = 1
			and r.valid = 1) refs_smells
	group by
		ref_id
) refs_all_smells
where
	smells_all_resources >= 2
)

--atualiza com os dados das aglomeracoes simples
update refactoring set in_agglomeration = 1 where id in (select ref_id from refactorings_in_agglomerations);

--consulta estatisticas de aglomeracao e ref por tipo
select
	rt.name,
	(select count(*) from refactoring where valid = 1 and type_id = rt.id and in_agglomeration is not null) count,
	(select count(*) from refactoring where valid = 1 and re_refactored = 1 and type_id = rt.id and in_agglomeration is not null) re_refactored,
	(select count(*) from refactoring where valid = 1 and in_agglomeration = 1 and type_id = rt.id and in_agglomeration is not null) in_agglomeration,
	(select count(*) from refactoring where valid = 1 and re_refactored = 1 and in_agglomeration = 1 and type_id = rt.id and in_agglomeration is not null) in_agglomeration_and_re_refactored
from
	refactoring_type rt
where
	rt.id in (select type_id from refactoring);


--tocam ou nao em uma aglomeracao
SELECT in_agglomeration, count(*) FROM ref_base.refactoring group by in_agglomeration;



SELECT
	r.id ref_id,
	r.parameters,
	r.type_id,
	rt.name ref_type,
	p.name project,
	vt.hash original_commit,
	vt.hash final_commit,
	vt.description commit_text,
	vt.order version_order,
	r.class_id_bavota,
	rc.classification

FROM
	refactoring r
	inner join version vt on (vt.id = r.version_to)
	inner join version vf on (vf.id = r.version_frpm)
	inner join refactoring_type rt on (rt.id = r.type_id)
	inner join project p on (p.id = r.project_id)
	inner join refactoring_classification rc on (rc.id = r.class_id_bavota)
where
	r.valid = 1
order by
	r.project_id, vt.order
limit 0, 1000000;

LOAD DATA INFILE '/Users/diego/PycharmProjects/scripts_cedrim/data/re-refactored.csv' INTO TABLE re_refactoring
  FIELDS TERMINATED BY ';';


 SELECT
	r.id ref_id,
	r.parameters,
	r.type_id,
	rt.name ref_type,
	p.name project,
	vt.hash final_commit,
	vt.description commit_text,
	vt.order version_order,
	r.class_id_bavota,
	rc.classification

FROM
	refactoring r
	inner join version vt on (vt.id = r.version_to)
	inner join refactoring_type rt on (rt.id = r.type_id)
	inner join project p on (p.id = r.project_id)
	inner join refactoring_classification rc on (rc.id = r.class_id_bavota)
where
	r.valid = 1
	and vt.description REGEXP '.*#[0-9]+.*'
	and r.project_id not in (367, 368, 369)
limit 0, 1000000;

