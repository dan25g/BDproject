
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
        where (h.personaje_id=p2.personaje_id) and ((h.personaje_id = a.fk_pers_pod)) and (p.podid = a.fk_pod_pers) and (p.ponaturaleza = 'Artificial') and (h.personaje_id=o.fk_pers_org) and (o.lider = true)
UNION ALL
select v.nombre_supervillano as nombre, p2.tipo
    from infopersonajes.poder p, infopersonajes.personaje_poder a, infopersonajes.villano v, infopersonajes.personaje p2, infopersonajes.historico_personaje o
        where (v.personaje_id=p2.personaje_id) and (v.personaje_id = a.fk_pers_pod) and (p.podid = a.fk_pod_pers) and (p.ponaturaleza = 'Artificial') and (v.personaje_id=o.fk_pers_org) and (o.lider = true);

select round(t.promedio,2)
from (select AVG(s.serepisodios) promedio
from infopersonajes.serie s) t;


select m.medionombre as nombre, s.serepisodios as episodios
    from infopersonajes.serie s, infopersonajes.medio m
        where (s.medio_id = m.medio_id)
        group by s.medio_id, m.medio_id, s.serepisodios
            having s.serepisodios >= (select AVG(s.serepisodios) promedio
                                    from infopersonajes.serie s) ;
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

select t.cmblugar as lugar ,max(contador)
from (select c.cmblugar, count(c.cmblugar) contador
    from infopersonajes.combate c
    group by c.cmblugar) t
    group by t.cmblugar
    order by max(contador) DESC
    limit 3;

select k.nombre, k.poseedor, k.tipo
from(select t.objnombre as nombre,t.nombre_superheroe as poseedor,t.tipo, t.contador
        from(select o.objnombre, h.nombre_superheroe, p.tipo, count(r.fk_obj_reg) contador
             from infopersonajes.personaje p, infopersonajes.heroe h, infopersonajes.objeto o, infopersonajes.registro_combates r
             where (p.personaje_id = h.personaje_id) and (p.personaje_id = r.id_pers_reg) and (o.obid=r.fk_obj_reg)
             group by h.nombre_superheroe, o.objnombre, p.tipo) t
    UNION all
    select t.objnombre as nombre,t.nombre_supervillano as poseedor ,t.tipo, t.contador
    from(select o.objnombre, v.nombre_supervillano, p.tipo, count(r.fk_obj_reg) contador
             from infopersonajes.personaje p, infopersonajes.villano v, infopersonajes.objeto o, infopersonajes.registro_combates r
             where (p.personaje_id = v.personaje_id) and (p.personaje_id = r.id_pers_reg) and (o.obid=r.fk_obj_reg)
             group by v.nombre_supervillano, o.objnombre, p.tipo) t) k
    order by k.contador desc limit 3

