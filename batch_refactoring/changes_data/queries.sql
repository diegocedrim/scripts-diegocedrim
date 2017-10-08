select * from (
    select
        p.name project, repo_file_path_reduced, count(*) refs_count
    from
        refactoring r
        inner join refactored_resource rr on (rr.refactoring_id = r.id)
        inner join resource rsc on (rsc.id = rr.resource_id)
        inner join resource_java_file rjf on (rjf.resource_id = rsc.id)
        inner join project p on (p.id = r.project_id)
    where
        r.valid = 1
        and rr.is_before = 1
    group by
        p.name, repo_file_path_reduced) a
order by
 refs_count desc limit 0,10000000;


 match (el:Element)
  match (r:Refactoring)-[:CHANGED]->(a:Element {name:el.name})
  where a.hash_id <> el.hash_id
  return el.name, count(r)
  limit 10;