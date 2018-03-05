match (b:Batch)-[co:COMPOSED_OF]->(r:Refactoring)-->(c:Commit)
where b.type = 'element-based'
with b, co, r

optional match (r)-[:CHANGED]->(eb:Element)-->(sb:Smell)
with b, co, r, collect(sb.type) as smells_before

optional match (r)-[:PRODUCED]->(eb:Element)-->(sb:Smell)
return
    b as batch,
    co as composed_of,
    r as refactoring,
    smells_before,
    collect(sb.type) as smells_after

order by b.hash_id, co.order;