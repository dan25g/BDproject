
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
select h.nombre_superheroe as nombre, p2.tipo
      from infopersonajes.poder p, infopersonajes.personaje_poder a, infopersonajes.heroe h, infopersonajes.personaje p2, infopersonajes.historico_personaje o
        where (h.id_personaje=p2.id_personaje) and ((h.id_personaje = a.fk_pers_pod)) and (p.podid = a.fk_pod_pers) and (p.ponaturaleza = 'Artificial') and (h.id_personaje=o.fk_pers_org) and (o.lider = true)
UNION ALL
select v.nombre_supervillano as nombre, p2.tipo
    from infopersonajes.poder p, infopersonajes.personaje_poder a, infopersonajes.villano v, infopersonajes.personaje p2, infopersonajes.historico_personaje o
        where (v.id_personaje=p2.id_personaje) and (v.id_personaje = a.fk_pers_pod) and (p.podid = a.fk_pod_pers) and (p.ponaturaleza = 'Artificial') and (v.id_personaje=o.fk_pers_org) and (o.lider = true);

select AVG(s.serepisodios)
from infopersonajes.serie s;

select m.medionombre, s.serepisodios
    from infopersonajes.serie s, infopersonajes.medio m
        where (s.medio_id = m.medio_id)
        group by s.medio_id, m.medio_id, s.serepisodios
            having s.serepisodios >= (select AVG(s.serepisodios)
                                    from infopersonajes.serie s);
        --and (s.medio_id = m.medio_id);

select c.cmblugar
    from infopersonajes.combate c
    group by  c.cmblugar
    having count(c.cmblugar)= avg((select count(c1.cmblugar)
                                    from infopersonajes.combate c1
                                    group by c1.cmblugar));

select p.medio_id,p.pelcosteprod
from infopersonajes.pelicula p
group by p.medio_id
having p.pelcosteprod = (select avg(p2.pelganancias)
                         from infopersonajes.pelicula p2);

select c.cmblugar, count(c.cmblugar) contador
    from infopersonajes.combate c
    group by c.cmblugar;

select t.cmblugar ,max(contador)
from (select c.cmblugar, count(c.cmblugar) contador
    from infopersonajes.combate c
    group by c.cmblugar) t
    group by t.cmblugar
    order by max(contador) DESC

