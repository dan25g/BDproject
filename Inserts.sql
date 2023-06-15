insert into infousuarios.suscripcion (sustipo, susdescripcion, sustarifa)
values  ('VIP', 'suscripcion VIP', 9.9900),
        ('Gold', 'suscripcion GOLD', 19.9900),
        ('Premium', 'suscripcion Premium', 29.9900);

insert into infousuarios.usuario (username, nombreu, apellidou, fechanacu, correou, password, ciudadu, sexou, paisu, last_login, sub_fk_id)
values  ('byteb', 'miles', 'morales', '2012-02-29', 'byte64@gmail.com', 'pbkdf2_sha256$600000$rZsr59lWZfIlGB7XPBP01l$oa5k1GPDN//5J5jVLoeynWZPQ88pFZKIOWMmNKRfbyA=', 'New York', 'F', 'US', '2023-06-13 16:46:42.016434', 3),
        ('Peterparker16', 'Pedro', 'Villa', '2004-02-29', 'pete@gmail.com', 'pbkdf2_sha256$600000$kq4SMGUfTkVAM4F8glO8MV$TBA63L4KGSLhTf2qMQCCDOpm9w8q6XQT/CwD1sr1mb4=', 'Buenos Aires', 'Desc', 'AR', '2023-06-13 16:44:32.164870', 5),
        ('juanpepito20', 'juan', 'pepito', '1998-06-10', 'pepitobig@gmail.com', 'pbkdf2_sha256$600000$nc2qzRhoRoZmb5RUr1PDPS$MZVkB4Auim2WVTzrp7lhmHXEuGDRgpWmFo7OkQOdGpo=', 'monaco', 'M', 'MC', '2023-06-13 15:49:51.865282', 3),
        ('otherRick', 'ricardo', 'mejias', '1998-10-07', 'rickmej@gmail.com', 'pbkdf2_sha256$600000$VVRO2ikrnM5xSX9aeDm18C$FJQZ/5a6OXmPHl+z0JyM1c3VGRPsdiZIW/wa1Cpz6m8=', 'Barquisimeto', 'Otro', 'VE', '2023-06-13 16:28:57.177984', 5),
        ('Dangar', 'Daniel ', 'Garcia', '2000-05-04', 'dangar45@gmail.com', 'pbkdf2_sha256$600000$yMEmPmcFPGVd69PmihHIlB$LyXA+aNM/BR9TAijfC0PAbMh28pGCgh8oolKRnEY+uQ=', 'Caracas', 'M', 'VE', '2023-06-14 20:01:34.868001', 3),
        ('tina2006', 'tina', 'Vasta', '1992-08-12', 'tinadivasta@gmail.com', 'pbkdf2_sha256$600000$l1XhpMrOwAGtaWA2kaYJID$oB09NfC7h7qC/lzu6FCdmMBMI7jwOGOs81Gy+J1znzA=', 'Caracas', 'F', 'VE', '2023-06-14 21:13:42.420727', 4);

insert into infousuarios.perfil (per_id, idioma, percorreo, fk_usuario)
values  (1, 'Español', 'byte64@gmail.com', 'byteb'),
        (2, 'English', 'ori14@outlook.com', 'byteb'),
        (3, 'Español', 'rikijmg98@hotmail.com', 'otherRick'),
        (4, 'Italiano', 'pepitobig@gmail.com', 'juanpepito20'),
        (5, 'Frances', 'junito@yahoo.com', 'juanpepito20');

insert into infousuarios.actividad (act_id, act_ingreso, act_dispositivo, act_fin, fk_perfil)
values  (2, '2022-06-17 17:02:12.000000', 'smartphone', '2022-06-17 19:08:31.000000', 2),
        (3, '2022-09-20 12:18:33.000000', 'computadora', '2022-09-20 17:18:33.000000', 1),
        (4, '2021-05-13 19:10:31.000000', 'smartphone', '2021-05-13 23:10:49.000000', 5),
        (5, '2023-06-02 22:11:27.000000', 'smart tv', '2023-06-03 04:30:07.000000', 3),
        (6, '2019-11-18 19:12:39.000000', 'smartphone', '2019-11-18 22:19:05.000000', 1);

insert into infousuarios.beneficio (benid, bendescripcion)
values  (1, '10% de descuento en productos Funko Pop'),
        (2, '10% de descuento en entrada en cines seleccionados'),
        (3, 'susscripcion a marvel newsletter'),
        (4, 'cajas con material promocional de marvel'),
        (5, '10% de descuento en tienda seleccionadas de Marvel');

insert into infousuarios.suscripcion_beneficio (fk_ben_sus, fk_sus_ben)
values  (2, 3),
        (1, 4),
        (3, 5),
        (4, 3),
        (5, 5);

insert into infousuarios.tarjetacredito (tdcnumero, tdcfecvencimiento, tdccvv, fk_usuario_id)
values  (4273242134457977, '2030-05-01', 991, 'juanpepito20'),
        (4594251013627404, '2023-12-01', 593, 'otherRick'),
        (5536705474667447, '2027-01-01', 883, 'Peterparker16'),
        (377462596165784, '2027-12-01', 6909, 'byteb'),
        (5167126502675664, '2024-01-13', 800, 'Dangar'),
        (4767431223456090, '2027-05-01', 541, 'tina2006');

insert into infopersonajes.personaje (id_personaje, genc, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, color_pelo, color_ojos, frase_celebre, comic_primer_vez, estadoMarital)
values  (1, 'M', 'Wade', 'Winston', 'Wilson', null, 'Calvo', 'Marrones', null, 'New Mutants #98', 'Divorciado'),
        (2, 'M', 'Peter', 'Benjanmin', 'Parker', null, 'Castaño', 'Avellana', null, 'Amazing Fantasy #15', 'Casado'),
        (3, 'M', 'Anthony', 'Edward', 'Stark', null, 'Negro', 'Azules', null, 'Tales of Suspense #39', 'Divorciado'),
        (4, 'M', 'James', 'Buchanan', 'Barnes', null, 'Marron', 'Marrones', null, 'Capitan America #1', 'Soltero'),
        (5, 'F', 'Daisy', 'Louise', 'Johnson', null, 'Negro', 'Marrones', null, 'Secret War #2', 'Soltero'),
        (6, 'F', 'Mary', 'Jane', 'Watson', null, 'Rojo', 'Verdes', null, 'Amazing Spider-Man #42', 'Casado'),
        (7, 'F', 'Virginia', null, 'Potts', null, 'Rojo claro', 'Azules', null, 'Tales of Suspense #45', 'Divorciado'),
        (8, 'F', 'Mercedes', null, 'Wilson', null, 'Rojo', 'Ambar', null, 'Deadpool 3 #26', 'Divorciado'),
        (9, 'M', 'Leopold', 'James', 'Fitz', null, 'Castaño Oscuro', 'Marrones', null, 'Agents of Shield: The Chase', 'Casado'),
        (10, 'F', 'Jemma', 'Anne', 'Simmons', null, 'Rojo Oscuro', 'Ambar', null, 'Agents of Shield: The Chase', 'Casado'),
        (11, 'M', 'Norman', 'Virgil', 'Osborne', null, 'Castaño', 'Verdes', null, 'Amazing Spider-Man #14', 'Viudo'),
        (12, 'M', 'Zhang', null, 'Tong', null, 'Negro', 'Verdes', null, 'Tales of Suspense #50', 'Soltero'),
        (13, 'M', 'Nathaniel', null, 'Essex', null, 'Negro', 'Rojos', null, 'Uncanny X-Men #221', 'Viudo'),
        (14, 'M', 'Grant', 'Douglas', 'Ward', null, 'Negro', 'Negros', null, 'Agents of Shield: The Chase', 'Soltero'),
        (15, 'M', 'Helmut', null, 'Zemo', null, 'Rubio', 'Azules', null, 'Capitan America #25', 'Soltero'),
        (17, 'M', 'Thor', null, 'Odinsson', null, 'Rubio', 'azules', null, 'Thor #1', 'Viudo'),
        (18, 'M', 'Steve', null, 'Rogers', null, 'Rubio', 'azules', null, 'Cap #1', 'Soltero');

insert into infopersonajes.civil (id_personaje)
values  (6),
        (7),
        (8),
        (9),
        (10);

insert into infopersonajes.heroe (id_personaje, nombre_superheroe, color_traje, logotipo)
values  (1, 'Deadpool', 'Rojo y Negro', 'un circulo rojo y negro'),
        (2, 'Spider-Man', 'Rojo y Azul', 'Una araña'),
        (3, 'Iron-Man', 'Rojo y Dorado', 'Un Casco de hierro'),
        (4, 'Soldado del Invierno', 'Negro y Plata', 'Una estrella roja'),
        (5, 'Quake', 'Negro', 'Un simbolo sismico');

insert into infopersonajes.villano (id_personaje, nombre_supervillano, objetivo, archienemigo)
values  (11, 'Duende Verde', 'Matar a Spider-Man', 2),
        (12, 'El Mandarin', 'Dominar el mundo criminal', 3),
        (13, 'Mr Siniestro', 'Dominar el mundo y crear una raza superior', 1),
        (14, 'Desconocido', 'Reconstruir Hydra con el a la cabeza', 5),
        (15, 'Baron Zemo', 'Revivir Hydra', 4);

insert into infopersonajes.amistad (id_civil, id_amispers)
values  (9, 5),
        (10, 5),
        (7, 3),
        (6, 7);

insert into infopersonajes.nacionalidad (id_personaje_nac, id_nacion, nacion_nombre, nacion_continente)
values  (1, 1, 'Canada', 'America'),
        (3, 2, 'Estados Unidos', 'America'),
        (2, 2, 'Estados Unidos', 'America'),
        (4, 2, 'Estados Unidos', 'America'),
        (9, 3, 'Escocia', 'Europa');

insert into infopersonajes.creador (id_personaje_cre, id_creador, creador_nombre, creador_apellido)
values  (1, 1, 'Fabian', 'Nicieza'),
        (4, 2, 'Joe', 'Simon'),
        (6, 3, 'Stan', 'Lee'),
        (8, 4, 'Joe', 'Kelly'),
        (13, 5, 'Chris', 'Claremont');

insert into infopersonajes.ocupacion (id_personaje_ocu, id_ocupacion, ocupa_nombre)
values  (1, 1, 'Mercenario'),
        (2, 2, 'Fotografo'),
        (3, 3, 'Cientifico'),
        (4, 1, 'Mercenario'),
        (11, 4, 'Empresario');

insert into infopersonajes.historico_matrimonio (id_pers_conyug1, id_pers_conyug2, fecha_inicio, fecha_fin)
values  (1, 8, '2005-10-15', '2006-08-09'),
        (2, 6, '2004-03-23', null),
        (3, 7, '2008-12-01', '2015-09-09'),
        (10, 9, '2018-05-30', null);

insert into infopersonajes.poder (podid, ponombre, podescripcion, ponaturaleza)
values  ('Regeneracion', 'Regenera partes del cuerpo rapidamente', 'Mutante'),
        ('Telepatia', 'Leer mentes y otras habilidades', 'Mutante'),
        ('Poderes Aracnidos ', 'Poderes similares a los de las arañas', 'Mutante'),
        ('Vibraciones', 'Permite mandar vibraciones moleculares a donde se quiera', 'Inhumano'),
        ('Manipulacion de Chi', 'Permite vivir mucho mas tiempo y mejorar tus habilidades fisicas', 'Mistico'),
        ('Habilidades Fisicas Aumentas', 'Permite mejores habilidades fisicas', 'Supersoldado'),
        ('Supertraje', 'Mejora las habilidades y permite volar', 'Tecnologico');

insert into infopersonajes.personaje_poder (fk_pod_pers, fk_pers_pod, hereditario)
values  (1, 1, true),
        (2, 13, true),
        (3, 2, true),
        (4, 5, false),
        (5, 12, false);

insert into infopersonajes.tipoobj (tipo_nombre, tipo_descripcion)
values  ('Cosmico', 'Artefactos de origen cosmico o espacial'),
        ('Mistico', 'Artefactos de origen mistico'),
        ('Arma', 'Artefactos que pueden ser usados principalmente como arma'),
        ('Mejora', 'Artefactos que mejoran las aptitudes'),
        ('Traje', 'Artefactos que pueden vestirse');

insert into infopersonajes.objeto (obid, objnombre, objmaterial, objdescripcion, objtipo)
values  ('Traje Mark 15', 'Vibranium', 'Traje mecanico de vibranium', 5),
        ('Manoplas antiVibra', 'Vibranium', 'Manoplas que protegen las manos de las vibraciones y las canalizan', 4),
        ('Brazo Bionico', 'Vibranium', 'Brazo prostetico de vibranium', 4),
        ('Anillos del Poder', 'Desconocido', 'Anillos de póder psionico con efestos varios', 1),
        ('Aerodeslizador', 'Acero', 'Aerodeslizador con muchas implementacione', 3),
        ('Espada Zemo', 'Adamantio', 'Espada heredada por la familia Zemo', 3),
        ('Katanas', 'Acero', 'Espada de acero japonesa', 3);

insert into infopersonajes.personaje_objeto (fk_obj_pers, fk_pers_obj, hereditario)
values  (1, 3, true),
        (2, 5, false),
        (3, 4, false),
        (4, 12, true),
        (5, 15, true);

insert into infopersonajes.combate (cmblugar)
values  ('New York'),
        ('Antartida'),
        ('Latveria'),
        ('Portland'),
        ('Lao Tze');

insert into infopersonajes.registro_combates (fk_cmb_reg, fk_obj_reg, id_pers_reg, id_pod_reg, cmbfecha)
values  (1, 6, 2, 3, '2001-06-13'),
        (2, 3, 4, 6, '2014-06-02'),
        (3, 7, 1, 1, '2020-07-07'),
        (4, 2, 5, 4, '2015-10-02'),
        (5, 1, 3, 7, '2012-06-08');

insert into infopersonajes.organizacion (org_nombre, eslogan, tipo_organizacion, comic_primer_vez, objetivo_principal, lugar_creacion)
values  ('HYDRA', 'si cortas una cabeza dos mas reemplazan su lugar', 'Malvada', 'Strange Tales #135', 'conquistar el mundo', 'Desconocido'),
        ('SHIELD', 'Proteger y Cuidar', 'Heroica', 'Strange Tales #135', 'proteger al mundo ', 'Langley'),
        ('X-Force', 'Fuerza y Deber', 'Heroica', 'Uncanny X-Men #493', 'Equipo de asesinos mutantes dispuestos a obras negras', 'Alcatraz'),
        ('Thunderbolts', 'Union por los demas', 'Heroica', 'Incredible Hulk #449', 'Equipo de Exvillanos que decidieron rehacer su vida como heroes', 'Castillo Zemo'),
        ('Diez Anillos', 'Unidos por el mundo', 'Malvada', 'Ironheart #2', 'Conquistar el mundo', 'Cambodia');

insert into infopersonajes.sede (sede_nombre, sede_ubicacion, tipo_edificacion, id_org)
values  ('Dragon Celestial', 'Movil', 'voladora', 5),
        ('Ravencroft Institute', 'Carolina del Norte', 'Superficial', 4),
        ('The Pointe', 'Oceano Atlantico', 'voladora', 3),
        ('El Faro', 'Portland', 'Subterranea', 2),
        ('Ravenous Base', 'Desconocido', 'Subterranea', 1);

insert into infopersonajes.historico_personaje (fk_pers_org, fk_org_pers, fundador, lider, fecha_union, fecha_salida)
values  (1, 3, false, false, '2012-06-06', null),
        (2, 2, false, false, '2016-07-09', null),
        (3, 2, false, false, '2011-01-12', null),
        (4, 1, false, false, '1950-09-23', '2011-07-28'),
        (12, 5, true, true, '1870-11-09', null);

insert into infopersonajes.medio (medfecestreno, medcomcreacion, medcomproduc, medrating, medsinopsis, medionombre)
values  ('2015-12-09', 'Laura Bosque', 'Fabian Wolsh', 4, 'La vida de la hacker Skye se ve revolucionada en el momento que se encuentra con al Agencia Shield', 'Agents of Shield'),
        ('2016-03-18', 'Karla Lions', 'Mariangel Fabian', 5, 'Despues de otro incidente internacional, en el que se ven envueltos los Vengadores,la presion politica pone un marcha una reforma con el tema de los superheroes', 'Capitan America Civil War'),
        ('2021-02-23', 'Julian Moura', 'Harry Gomez', 3, 'Juego donde Deadpool pelea contra Mister Sinister', 'Deadpool'),
        ('2010-08-15', 'Javier Cadenas', 'Gabriel Fabianski', 3, 'El descarado y brillante Tony Stark se enfrenta a una competencia, mientras lidia con sus demonios internos y averigua sobre un nuevo enemigo', 'Iron Man 2'),
        ('2002-05-15', 'Daniel Wesex', 'Daniel Wesex', 4, 'Luego de sufir la picadura de una araña Peter Parker, tendra que afrontar sus nuevos poderes', 'Spider-Man');

insert into infopersonajes.pelicula (medio_id, medtipo, peldirector, pelduracion, pelcosteprod, pelganancias)
values  (1, 'liveaction', 'Sam Raimi', 121, 139.00, 825.00),
        (5, 'liveaction', 'Jon Favreau', 130, 200.00, 623.90),
        (4, 'liveaction', 'Anthony Russo', 148, 250.00, 1153.00);

insert into infopersonajes.serie (medio_id, medtipo, sercreador, serepisodios, sercanal)
values  (2, 'liveaction', 'Laura Bosque', 300, 'Sony');

insert into infopersonajes.jueplataforma (plataforma)
values  ('Wii'),
        ('PS4'),
        ('Xbox series S'),
        ('Switch'),
        ('PS5');

insert into infopersonajes.juego (medio_id, medtipo, juegocompania, fk_plataforma)
values  (3, 'accion', 'Ubisoft', 2);

insert into infopersonajes.organizacion_medio (fk_med_org, fk_org_med, estado)
values  (1, 2, 'Desconocido'),
        (2, 1, 'Activa'),
        (3, 3, 'Inactiva'),
        (4, 1, 'Disuelta'),
        (5, 5, 'Activa');

insert into infopersonajes.personaje_medio (fk_med_pers, fk_pers_med, actor_tipo, actor_nombre, personaje_tipo)
values  (4, 4, 'Interpreta', 'Sebastian Stan', 'Protagonista'),
        (1, 2, 'Interpreta', 'Tobey Macguire', 'Protagonista'),
        (2, 9, 'Interpreta', 'Iain de Caestecker', 'Secundario'),
        (5, 7, 'Interpreta', 'Gwyneth Paltrow', 'Secundario'),
        (3, 13, 'Presta su voz', 'Keith Ferguson', 'Antagonista');

insert into infousuarios.perfil_medio (fk_perf_med, fk_med_perf, calificacion, fecha_vista)
values  (2, 2, 4, '2022-09-16 15:31:47.000000'),
        (4, 3, 2, '2018-08-23 18:09:06.000000'),
        (1, 2, 3, '2022-09-21 20:33:16.000000'),
        (3, 4, 4, '2019-05-19 08:34:24.000000'),
        (5, 3, 5, '2020-06-14 15:35:11.000000');

select u.username, u.nombreu, u.apellidou, s.sustipo
    from infousuarios.usuario u inner join infousuarios.suscripcion s on s.susid = u.sub_fk_id