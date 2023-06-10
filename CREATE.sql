create schema infousuarios;

create schema infopersonajes;

create domain genero as varchar not null check ( value in ('M','F','Desc','Otro'));

create domain mail as varchar not null check ( value ~* '^[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$');

create table infousuarios.usuario(
    idU varchar(15) unique not null,
    nombreU varchar(20) not null,
    apellidoU varchar(20) not null,
    fechaNacU date not null,
    correoU mail,
    contrasennaU varchar(20) not null,
    ciudadU varchar(10) not null,
    sexoU genero,
    paisU varchar(15) not null,

    constraint pk_user primary key (idU),
    constraint val_fnac check ( fechaNacU between '1924/1/1' and '2013/12/31')
);

create table infousuarios.perfil(
    per_id serial unique not null,
    idioma varchar(10) not null,
    perCorreo mail not null,
    fk_usuario varchar(25) not null,

    constraint pk_perfil primary key (per_id),
    constraint fk_user foreign key (fk_usuario) references infousuarios.usuario(idU)
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
    tdcnumero serial unique not null,
    tdcfecvencimiento date not null,
    tdccvv int not null,
    fk_usuario varchar(25) not null,

    constraint pk_tdc primary key (tdcnumero),
    constraint fk_usuario_tdc foreign key (fk_usuario) references infousuarios.usuario(idU)
    on delete cascade on update cascade
);

create table infopersonajes.civil(
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

    constraint pk_civil primary key (id_personaje)
);

create table infopersonajes.heroe(
    id_personaje int unique not null,
    genC genero,
    primer_nombre varchar(20) not null,
    segundo_nombre varchar(20) not null,
    primer_apellido varchar(20) not null,
    segundo_apellido varchar(20) not null,
    color_pelo varchar(15) not null,
    color_ojos varchar(15) not null,
    frase_celebre varchar(75),
    nombre_superheroe varchar(20) not null,
    color_traje varchar(15) not null,
    logotipo varchar(75) not null,
    comic_primer_vez varchar(50) not null,

    constraint pk_heroe primary key (id_personaje)
);

create table infopersonajes.villano(
    id_personaje int unique not null,
    genC genero,
    primer_nombre varchar(20) not null,
    segundo_nombre varchar(20) not null,
    primer_apellido varchar(20) not null,
    segundo_apellido varchar(20) not null,
    color_pelo varchar(15) not null,
    color_ojos varchar(15) not null,
    frase_celebre varchar(75),
    nombre_supervillano varchar(20) not null,
    objetivo varchar(50) not null,
    comic_primer_vez varchar(50) not null,
    archienemigo int,

    constraint pk_civil primary key (id_personaje)
    constraint fk_archienemigo foreign key (archienemigo) references infopersonajes.heroe(id_personaje)
    on delete set null
);

create table infopersonajes.amistad(
    id_civil int,
    id_amispers int,

    constraint pk_amistad primary key (id_civil,id_amispers),
    constraint fk_civil foreign key (id_civil) references infopersonajes.civil(id_personaje),
    constraint fk_personaje foreign key (id_amispers) references infopersonajes.id_personaje,
    on delete cascade on update cascade

);