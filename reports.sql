
--select h.nombre_superheroe as SuperHeroe
    --from infopersonajes.personaje p, infopersonajes.heroe h, infopersonajes.villano v
    --where --p.id_personaje = (select h.id_personaje
                               -- from infopersonajes.personaje_poder a, infopersonajes.poder p2
                                --where (p2.ponaturaleza = 'Artificial') and (a.fk_pod_pers = p2.podid) and (h.id_personaje=a.fk_pers_pod)
                               -- ) or
                                --p.id_personaje = (select v.id_personaje
                               -- from infopersonajes.personaje_poder a, infopersonajes.poder p2,infopersonajes.villano v
                                --where (p2.ponaturaleza = 'Artificial') and (a.fk_pod_pers = p2.podid) and (v.id_personaje=a.fk_pers_pod)
                               -- group by (p2.ponaturaleza = 'Artificial') and (v.id_personaje=a.fk_pers_pod)
                               -- )
                               --
select h.nombre_superheroe, p2."tipoPers"
      from infopersonajes.poder p, infopersonajes.personaje_poder a, infopersonajes.heroe h, infopersonajes.personaje p2
        where (h.id_personaje=p2.id_personaje) and ((h.id_personaje = a.fk_pers_pod)) and (p.podid = a.fk_pod_pers) and (p.ponaturaleza = 'Artificial')
UNION ALL
select v.nombre_supervillano, p2."tipoPers"
    from infopersonajes.poder p, infopersonajes.personaje_poder a, infopersonajes.villano v, infopersonajes.personaje p2
        where (v.id_personaje=p2.id_personaje) and (v.id_personaje = a.fk_pers_pod) and (p.podid = a.fk_pod_pers) and (p.ponaturaleza = 'Artificial');

select AVG(s.serepisodios)
from infopersonajes.serie s;

select s.medio_id, s.serepisodios
    from infopersonajes.serie s
        group by s.medio_id, s.serepisodios
        having s.serepisodios > avg(s.serepisodios);

