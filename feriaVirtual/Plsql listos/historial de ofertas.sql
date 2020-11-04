-- crear procidimiento Listar Historial ofertas

select op.id_oferta as "N° Oferta",es.des_especie||' '||do.variedad as Descripcion
,us.nombre||' '||us.ap_paterno as Nombre,
TO_CHAR(op.fecha_oferta, 'dd/mm/YYYY') as "Fecha oferta"
FROM oferta_productor  op
INNER JOIN usuario us ON us.id_usuario=op.id_usuario
JOIN detalle_oferta do ON op.id_oferta=do.id_oferta
join especie es ON es.id_especie=do.id_especie
WHERE us.email='productor@gmail.com';

create or replace procedure SP_LISTAR_HISTORIAL_OFERTA(correo in VARCHAR2, Registros out SYS_REFCURSOR)
AS
    BEGIN
        open Registros for select op.id_oferta as "N° Oferta",es.des_especie||' '||do.variedad as Descripcion
        ,us.nombre||' '||us.ap_paterno as Nombre,
        TO_CHAR(op.fecha_oferta, 'dd/mm/YYYY') as "Fecha oferta"
        FROM oferta_productor  op
        INNER JOIN usuario us ON us.id_usuario=op.id_usuario
        JOIN detalle_oferta do ON op.id_oferta=do.id_oferta
        join especie es ON es.id_especie=do.id_especie
        WHERE us.email=correo;
    EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;


-- detalle de historial de ofertas
SELECT do.kilo, do.precio, ofp.fecha_oferta,do.fecha_cosecha, es.des_especie, do.variedad, img.imagen
FROM detalle_oferta do
JOIN oferta_productor ofp ON do.id_oferta=ofp.id_oferta
JOIN especie es ON do.id_especie=es.id_especie
JOIN variedad va ON va.des_variedad=do.variedad
JOIN imagen img ON img.id_imagen=va.id_imagen
where do.id_oferta=1;


create or replace procedure SP_LISTAR_DETALLE_HISTORIAL_OFERTA(oferta in Number,detalle_ho out SYS_REFCURSOR)
AS
    BEGIN
        open detalle_ho for SELECT do.kilo, do.precio, TO_CHAR(ofp.fecha_oferta, 'dd/mm/YYYY'),TO_CHAR(do.fecha_cosecha, 'dd/mm/YYYY'), es.des_especie, do.variedad, img.imagen
        FROM detalle_oferta do
        JOIN oferta_productor ofp ON do.id_oferta=ofp.id_oferta
        JOIN especie es ON do.id_especie=es.id_especie
        JOIN variedad va ON va.des_variedad=do.variedad
        JOIN imagen img ON img.id_imagen=va.id_imagen
        where do.id_oferta=oferta;
    EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;





       





