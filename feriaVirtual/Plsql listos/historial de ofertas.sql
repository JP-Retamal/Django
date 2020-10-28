-- crear procidimiento Listar Historial ofertas

select op.id_oferta as "N° Oferta", us.nombre||' '||us.ap_paterno as Nombre, op.id_orden as "N° Orden", TO_CHAR(op.fecha_oferta, 'dd/mm/YYYY') as "Fecha oferta"
FROM oferta_productor  op
INNER JOIN usuario us ON us.id_usuario=op.id_usuario
WHERE us.email='productor@gmail.com';

create or replace procedure SP_LISTAR_HISTORIAL_OFERTA(correo in VARCHAR2, Registros out SYS_REFCURSOR)
AS
    BEGIN
        open Registros for select op.id_oferta  as "N° Oferta", us.nombre||' '||us.ap_paterno as Nombre, op.id_orden as "N° Orden", TO_CHAR(op.fecha_oferta, 'dd/mm/YYYY') as "Fecha oferta"
        FROM oferta_productor  op
        INNER JOIN usuario us ON us.id_usuario=op.id_usuario
        WHERE us.email=correo;
    EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;


-- detalle de historial de ofertas
SELECT op.id_oferta, op.id_orden, op.id_usuario, op.fecha_oferta, do.kilo, do.precio, do.fecha_cosecha, es.des_especie,
        do.variedad, img.imagen
FROM oferta_productor op
JOIN detalle_oferta do ON do.id_oferta=op.id_oferta
JOIN especie es ON es.id_especie=do.id_especie
JOIN variedad va ON va.id_especie=es.id_especie and va.id_especie=do.id_especie
JOIN imagen img ON img.id_imagen=va.id_imagen
where do.variedad=va.des_variedad and op.id_oferta=1;


create or replace procedure SP_LISTAR_DETALLE_HISTORIAL_OFERTA(oferta in Number,detalle_ho out SYS_REFCURSOR)
AS
    BEGIN
        open detalle_ho for SELECT op.id_oferta, op.id_orden, op.id_usuario, TO_CHAR(op.fecha_oferta, 'DD/MM/yyyy') AS "Fecha Oferta",
        do.kilo, do.precio, TO_CHAR(do.fecha_cosecha, 'dd/mm/YYYY') as "Fercha Cosecha", es.des_especie,
        do.variedad, img.imagen
        FROM oferta_productor op
        JOIN detalle_oferta do ON do.id_oferta=op.id_oferta
        JOIN especie es ON es.id_especie=do.id_especie
        JOIN variedad va ON va.id_especie=es.id_especie and va.id_especie=do.id_especie
        JOIN imagen img ON img.id_imagen=va.id_imagen
        where do.variedad=va.des_variedad and op.id_oferta=oferta;
    EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;





       





