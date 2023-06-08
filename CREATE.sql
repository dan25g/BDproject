create schema infousuarios;

create schema infopersonajes;

create table infousuarios.usuario(
    idU varchar(20),
    nombreU varchar(20),

    constraint pk_user primary key (idU)
);