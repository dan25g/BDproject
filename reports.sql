select u.username, u.nombreu, u.apellidou, s.sustipo
    from infousuarios.usuario u inner join infousuarios.suscripcion s on s.susid = u.sub_fk_id

