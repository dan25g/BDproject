create schema infousuarios;

create schema infopersonajes;

create domain genero as varchar not null check ( value in ('M','F','Desc','Otro'));

create domain mail as varchar not null check ( value ~* '^[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$');

create domain estadoMar as varchar not null check (value in ('Casado','Soltero','Viudo','Divorciado'));

create domain rating as int not null check (value between 1 and 5);

create domain actortipo as varchar not null check(value in('Interpreta','Presta su voz'));

create table infousuarios.usuario(
    username varchar(15) unique not null,
    nombreU varchar(20) not null,
    apellidoU varchar(20) not null,
    fechaNacU date not null,
    correoU mail,
    password varchar(20) not null,
    ciudadU varchar(10) not null,
    sexoU genero,
    paisU varchar(15) not null,

    constraint pk_user primary key (username),
    constraint val_fnac check ( fechaNacU between '1924/1/1' and '2013/12/31')
);

create table infousuarios.perfil(
    per_id serial unique not null,
    idioma varchar(10) not null,
    perCorreo mail not null,
    fk_usuario varchar(25) not null,

    constraint pk_perfil primary key (per_id),
    constraint fk_user foreign key (fk_usuario) references infousuarios.usuario(username)
    on delete cascade on update cascade
);

create table infousuarios.actividad(
    act_id serial unique not null,
    act_ingreso timestamp not null,
    act_dispositivo varchar(10) not null,
    act_fin timestamp not null,
    fk_perfil int not null,

    constraint pk_actividad primary key (act_id),
    constraint fk_perfil foreign key (fk_perfil) references infousuarios.perfil(per_id)
    on delete cascade on update cascade
);

create table infousuarios.suscripcion(
    susid serial unique not null,
    sustipo varchar(10) not null,
    susdescripcion varchar(50) not null,
    sustarifa numeric(5,4) not null,

    constraint pk_suscrip primary key (susid),
    constraint val_sutipo check ( sustipo in ('VIP', 'Gold','Premium')),
    constraint val_tarf check ( sustarifa in (9.99,19.99,29.99))
);

create table infousuarios.beneficio(
    benid serial unique not null,
    bendescripcion varchar(50) not null,

    constraint pk_beneficio primary key (benid)
);

create table infousuarios.Suscripcion_Beneficio(
    fk_ben_sus serial not null,
    fk_sus_ben serial not null,

    constraint pk_ben_sus primary key (fk_ben_sus,fk_sus_ben),
    constraint fk_ben foreign key (fk_ben_sus) references infousuarios.beneficio(benid)
    on delete cascade on update cascade,
    constraint fk_sus foreign key (fk_sus_ben) references infousuarios.suscripcion(susid)
    on delete cascade on update cascade
);

create table infousuarios.TarjetaCredito(
    tdcnumero bigint unique not null,
    tdcfecvencimiento date not null,
    tdccvv int not null,
    fk_usuario varchar(25) not null unique,

    constraint pk_tdc primary key (tdcnumero),
    constraint fk_usuario_tdc foreign key (fk_usuario) references infousuarios.usuario(username)
    on delete cascade on update cascade
);

create table infopersonajes.personaje(
    id_personaje int unique not null,
    genC genero,
    primer_nombre varchar(20) not null,
    segundo_nombre varchar(20) not null,
    primer_apellido varchar(20) not null,
    segundo_apellido varchar(20) not null,
    color_pelo varchar(15) not null,
    color_ojos varchar(15) not null,
    frase_celebre varchar(75) null,
    comic_primer_vez varchar(50) not null,

    constraint pk_personaje primary key (id_personaje)
);

create table infopersonajes.civil(
    id_personaje int unique not null,

    constraint pk_civil primary key (id_personaje),
    constraint fk_personaje foreign key (id_personaje) references infopersonajes.personaje(id_personaje)
);

create table infopersonajes.heroe(
    id_personaje int unique not null,
    nombre_superheroe varchar(20) not null,
    color_traje varchar(15) not null,
    logotipo varchar(75) not null,

    constraint pk_heroe primary key (id_personaje),
    constraint fk_personaje foreign key (id_personaje) references infopersonajes.personaje(id_personaje)
);

create table infopersonajes.villano(
    id_personaje int unique not null,
    nombre_supervillano varchar(20) not null,
    objetivo varchar(50) not null,
    archienemigo int unique ,

    constraint pk_villano primary key (id_personaje),
    constraint fk_personaje foreign key (id_personaje) references infopersonajes.personaje(id_personaje),
    constraint fk_archienemigo foreign key (archienemigo) references infopersonajes.heroe(id_personaje)
    on delete set null
);

create table infopersonajes.amistad(
    id_civil int not null,
    id_amispers int not null,

    constraint pk_amistad primary key (id_civil,id_amispers),
    constraint fk_civil foreign key (id_civil) references infopersonajes.civil(id_personaje),
    constraint fk_personaje foreign key (id_amispers) references infopersonajes.personaje(id_personaje)
    on delete cascade on update cascade

);

create table infopersonajes.nacionalidad(
    id_personaje_nac int not null,
    id_nacion int not null,
    nacion_nombre varchar(20) not null, 
    nacion_continente varchar(20) not null check(nacion_continente in('America','Europa','Africa','Asia','Oceania')),

    constraint pk_nacionalidad primary key (id_personaje_nac,id_nacion),
    constraint fk_personaje foreign key (id_personaje_nac) references infopersonajes.personaje(id_personaje)
);

create table infopersonajes.creador(
    id_personaje_cre int not null,
    id_creador int not null,
    creador_nombre varchar(20) not null, 
    creador_apellido varchar(20) not null,

    constraint pk_creador primary key (id_personaje_cre,id_creador),
    constraint fk_personaje foreign key (id_personaje_cre) references infopersonajes.personaje(id_personaje)
);

create table infopersonajes.ocupacion(
    id_personaje_ocu int not null,
    id_ocupacion int not null,
    ocupa_nombre varchar(20) not null,

    constraint pk_ocupacion primary key (id_personaje_ocu,id_ocupacion),
    constraint fk_personaje foreign key (id_personaje_ocu) references infopersonajes.personaje(id_personaje)
);

create table infopersonajes.historico_matrimonio(
    id_pers_conyug1 int not null,
    id_pers_conyug2 int not null,
    fecha_inicio date not null,
    fecha_fin date,
    estadoMarital estadoMar,

    constraint pk_matrimonio primary key (id_pers_conyug1,id_pers_conyug2,fecha_inicio),
    constraint fk_conyuge1 foreign key (id_pers_conyug1) references infopersonajes.personaje(id_personaje),
    constraint fk_conyuge2 foreign key (id_pers_conyug2) references infopersonajes.personaje(id_personaje)
);

create table infopersonajes.poder(
    podid serial unique not null,
    ponombre varchar(30) not null,
    podescripcion varchar(70) not null,
    ponaturaleza varchar(20) not null,

    constraint pk_poder primary key (podid)
);

create table infopersonajes.personaje_poder(
    fk_pod_pers int not null,
    fk_pers_pod int not null,
    hereditario boolean not null,

    constraint pk_personaje_poder primary key (fk_pod_pers,fk_pers_pod),
    constraint fk_personaje foreign key (fk_pers_pod) references infopersonajes.personaje(id_personaje),
    constraint fk_poder foreign key (fk_pod_pers) references infopersonajes.poder(podid)
);

create table infopersonajes.tipoobj (
    idtipo serial unique not null,
    tipo_nombre varchar(20) not null,
    tipo_descripcion varchar(70) not null,

    constraint pk_tipo primary key (idtipo)
);

create table infopersonajes.objeto(
    obid serial unique not null,
    objnombre varchar(20) not null,
    objmaterial varchar(20) not null,
    objdescripcion varchar(70) not null,
    objtipo int not null,

    constraint pk_objeto primary key (obid),
    constraint fk_tipo foreign key (objtipo) references infopersonajes.tipoobj(idtipo)
);

create table infopersonajes.personaje_objeto(
    fk_obj_pers int not null,
    fk_pers_obj int not null,
    hereditario boolean not null,

    constraint pk_personaje_objeto primary key (fk_obj_pers,fk_pers_obj),
    constraint fk_personaje foreign key (fk_pers_obj) references infopersonajes.personaje(id_personaje),
    constraint fk_objeto foreign key (fk_obj_pers) references infopersonajes.objeto(obid)
);

create table infopersonajes.combate(
    cmbid serial unique not null,
    cmblugar varchar(20) not null,

    constraint pk_combate primary key (cmbid)
);

create table infopersonajes.registro_combates (
    fk_cmb_reg int not null,
    fk_obj_reg int not null,
    id_pers_reg int not null,
    id_pod_reg int not null,
    cmbfecha date not null,

    constraint pk_registro_combate primary key (fk_cmb_reg,fk_obj_reg,id_pers_reg,id_pod_reg,cmbfecha),
    constraint fk_personaje foreign key (id_pers_reg) references infopersonajes.personaje(id_personaje),
    constraint fk_combate foreign key (fk_cmb_reg) references infopersonajes.combate(cmbid),
    constraint fk_objeto foreign key (fk_obj_reg) references infopersonajes.objeto(obid),
    constraint fk_poder foreign key (id_pod_reg) references infopersonajes.poder(podid)
);

create table infopersonajes.organizacion(
    id_organizacion serial unique not null,
    org_nombre varchar(40) not null,
    eslogan varchar (100) not null,
    tipo_organizacion varchar(7) not null check (tipo_organizacion in ('Malvada','Civil','Heroica')),
    comic_primer_vez varchar(30) not null,
    objetivo_principal varchar(70) not null,
    lugar_creacion varchar(20) not null,

    constraint pk_organizacion primary key (id_organizacion)
);

create table infopersonajes.sede(
    id_sede serial unique not null,
    sede_nombre varchar(20) not null,
    sede_ubicacion varchar (20) not null,
    tipo_edificacion varchar(10) not null check (tipo_edificacion in ('Subterranea','voladora','Superficial')),
    id_org int not null,

    constraint pk_sede primary key (id_sede),
    constraint fk_org foreign key (id_org) references infopersonajes.organizacion(id_organizacion)
);

create table infopersonajes.historico_personaje(
    fk_pers_org int not null,
    fk_org_pers int not null,
    fundador boolean not null,
    lider boolean not null,
    fecha_union date not null,
    fecha_salida date,

    constraint pk_historico primary key (fk_pers_org,fk_org_pers,fecha_union),
    constraint fk_personaje foreign key (fk_pers_org) references infopersonajes.personaje(id_personaje),
    constraint fk_organizacion foreign key (fk_org_pers) references infopersonajes.organizacion(id_organizacion)
);

create table infopersonajes.medio(
    medio_id serial unique not null,
    medfecestreno date not null,
    medcomcreacion varchar(20) not null,
    medcomproduc varchar (40) not null,
    medrating rating,
    medsinopsis varchar(120) not null,

    constraint pk_medio primary key (medio_id)
);

create table infopersonajes.pelicula(
    medio_id int unique not null,
    medtipo varchar(10) not null check(medtipo in('animada','liveaction','stopmotion')),
    peldirector varchar(40) not null,
    pelduracion int not null,
    pelcosteprod numeric(5,4) not null,
    pelganancias numeric(5,4) not null,

    constraint pk_pelicula primary key (medio_id),
    constraint check_ganancia check (pelcosteprod<=pelganancias),
    constraint fk_medio foreign key (medio_id) references infopersonajes.medio(medio_id)
);

create table infopersonajes.serie(
    medio_id int unique not null,
    medtipo varchar(10) not null check(medtipo in('animada','liveaction','stopmotion')),
    sercreador varchar(40) not null,
    serepisodios int not null,
    sercanal varchar(20) not null,

    constraint pk_serie primary key (medio_id),
    constraint fk_medio foreign key (medio_id) references infopersonajes.medio(medio_id)
);

create table infopersonajes.jueplataforma(
    id_plataforma serial unique not null,
    plataforma varchar(20) not null,

    constraint pk_plataforma primary key (id_plataforma)
);

create table infopersonajes.juego(
    medio_id int unique not null,
    medtipo varchar(14) not null check(medtipo in('accion','aventura','estrategia','rpg','mundo abierto','simulacion')),
    juegocompania varchar(20) not null,
    fk_plataforma int not null,

    constraint pk_juego primary key (medio_id),
    constraint fk_plataforma foreign key (fk_plataforma) references infopersonajes.jueplataforma(id_plataforma),
    constraint fk_medio foreign key (medio_id) references infopersonajes.medio(medio_id)
);

create table infopersonajes.organizacion_medio(
    fk_med_org int not null,
    fk_org_med int not null,
    estado varchar(20) not null,

    constraint pk_orgmed primary key (fk_med_org,fk_org_med),
    constraint fk_organizacion foreign key (fk_org_med) references infopersonajes.organizacion(id_organizacion),
    constraint fk_medio foreign key (fk_med_org) references infopersonajes.medio(medio_id)
);

create table infopersonajes.personaje_medio(
    fk_med_pers int not null,
    fk_pers_med int not null,
    actor_tipo actortipo,
    actor_nombre varchar(40) not null,
    personaje_tipo varchar(30) not null check (personaje_tipo in('Antagonista','Protagonista','Secundario')),

    constraint pk_persmed primary key (fk_med_pers,fk_pers_med),
    constraint fk_personaje foreign key (fk_pers_med) references infopersonajes.personaje(id_personaje),
    constraint fk_medio foreign key (fk_med_pers) references infopersonajes.medio(medio_id)
);

create table infousuarios.perfil_medio(
    fk_perf_med int not null,
    fk_med_perf int not null,
    calificacion rating,
    fecha_vista timestamp not null,

    constraint pk_perfmed primary key (fk_perf_med,fk_med_perf),
    constraint fk_perfil foreign key (fk_perf_med) references infousuarios.perfil(per_id),
    constraint fk_medio foreign key (fk_med_perf) references infopersonajes.medio(medio_id)
);

create function Mensaje_Perdida() returns trigger as
$$
    BEGIN
        raise notice 'ADVERTENCIA: La pelicula da perdida, revise los datos inserados';
    END
$$
language plpgsql;

create trigger DaPerdida before insert or update on infopersonajes.pelicula
    for each row
    when ( old.pelcosteprod>old.pelganancias )
    execute function Mensaje_Perdida();