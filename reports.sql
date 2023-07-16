
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
    order by k.contador desc limit 3;

select p.primer_nombre as nombre, p.primer_apellido as apellido, c.creador_nombre as nombrec , c.creador_apellido as apellidoc
    from(select p.primer_nombre, p.primer_apellido, p.personaje_id
        from infopersonajes.personaje p
        where ((p.primer_nombre like 'A%') and (p.primer_apellido like 'A%'))
        OR ((p.primer_nombre like 'B%') and (p.primer_apellido like 'B%'))
        OR ((p.primer_nombre like 'C%') and (p.primer_apellido like 'C%'))
        OR ((p.primer_nombre like 'D%') and (p.primer_apellido like 'D%'))
        OR ((p.primer_nombre like 'E%') and (p.primer_apellido like 'E%'))
        OR ((p.primer_nombre like 'F%') and (p.primer_apellido like 'F%'))
        OR ((p.primer_nombre like 'G%') and (p.primer_apellido like 'G%'))
        OR ((p.primer_nombre like 'H%') and (p.primer_apellido like 'H%'))
        OR ((p.primer_nombre like 'I%') and (p.primer_apellido like 'I%'))
        OR ((p.primer_nombre like 'J%') and (p.primer_apellido like 'J%'))
        OR ((p.primer_nombre like 'K%') and (p.primer_apellido like 'K%'))
        OR ((p.primer_nombre like 'L%') and (p.primer_apellido like 'L%'))
        OR ((p.primer_nombre like 'M%') and (p.primer_apellido like 'M%'))
        OR ((p.primer_nombre like 'N%') and (p.primer_apellido like 'N%'))
        OR ((p.primer_nombre like 'O%') and (p.primer_apellido like 'O%'))
        OR ((p.primer_nombre like 'P%') and (p.primer_apellido like 'P%'))
        OR ((p.primer_nombre like 'Q%') and (p.primer_apellido like 'Q%'))
        OR ((p.primer_nombre like 'R%') and (p.primer_apellido like 'R%'))
        OR ((p.primer_nombre like 'S%') and (p.primer_apellido like 'S%'))
        OR ((p.primer_nombre like 'T%') and (p.primer_apellido like 'T%'))
        OR ((p.primer_nombre like 'U%') and (p.primer_apellido like 'U%'))
        OR ((p.primer_nombre like 'V%') and (p.primer_apellido like 'V%'))
        OR ((p.primer_nombre like 'W%') and (p.primer_apellido like 'W%'))
        OR ((p.primer_nombre like 'X%') and (p.primer_apellido like 'X%'))
        OR ((p.primer_nombre like 'Y%') and (p.primer_apellido like 'Y%'))
        OR ((p.primer_nombre like 'Z%') and (p.primer_apellido like 'Z%')))p, infopersonajes.creador c
    where (p.personaje_id = c.id_personaje_cre);

    select p.ponombre as nombre,p.ponaturaleza as naturaleza,p.podescripcion as descripcion, v.nombre_supervillano as usuario
        from infopersonajes.villano v, infopersonajes.poder p, infopersonajes.personaje_poder q
        where (p.podid = q.fk_pod_pers) and (v.personaje_id=q.fk_pers_pod) and (q.hereditario = true) and (p.ponombre like 'Super%');

    select o.id_organizacion, count(s.org_id) contador1
        from infopersonajes.organizacion o, infopersonajes.sede s
        where (o.id_organizacion=s.org_id)
        group by s.org_id, o.id_organizacion
        order by contador1 desc;

    select p.personaje_id, count(h.fk_pers_org) contador2
        from infopersonajes.personaje p, infopersonajes.historico_personaje h
        where (p.personaje_id=h.fk_pers_org)
        group by h.fk_pers_org, p.personaje_id
        order by contador2 desc;

    select o.org_nombre as org, p.primer_nombre as nombrelider, p.primer_apellido as apellidolider, org.contador1 as sedes, pers.contador2 as orgs
        from (select o.id_organizacion, count(s.org_id) contador1
        from infopersonajes.organizacion o, infopersonajes.sede s
        where (o.id_organizacion=s.org_id)
        group by s.org_id, o.id_organizacion
        order by contador1 desc) org, (select p.personaje_id, count(h.fk_pers_org) contador2
        from infopersonajes.personaje p, infopersonajes.historico_personaje h
        where (p.personaje_id=h.fk_pers_org)
        group by h.fk_pers_org, p.personaje_id
        order by contador2 desc) pers, infopersonajes.personaje p, infopersonajes.organizacion o, infopersonajes.historico_personaje h
        where (p.personaje_id=pers.personaje_id) and (org.id_organizacion=o.id_organizacion) and (h.fk_org_pers=org.id_organizacion) and (h.fk_pers_org=pers.personaje_id) and (h.lider=true) and (pers.contador2>=2) and (org.contador1>2);

select m.medionombre as nombre,p.pelduracion as duracion,p.pelcosteprod as coste,p.pelganancias as ganancias, m.medfecestreno as estreno
from infopersonajes.pelicula p, infopersonajes.medio m
where (p.medio_id = m.medio_id) and (p.pelduracion>150)
group by p.medio_id, m.medio_id
having p.pelganancias >= (select avg(p2.pelganancias)
        from infopersonajes.pelicula p2
        where p2.medtipo ='animada')
order by p.pelcosteprod desc;

    select avg(p2.pelganancias)
        from infopersonajes.pelicula p2
        where p2.medtipo ='animada';