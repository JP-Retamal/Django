--Plsql listar detalle de pedidos 
SELECT * FROM orden_compra oc
INNER JOIN solicitud sol ON oc.id_solicitud=sol.id_solicitud
WHERE sol.id_estado=2
;
--enviar id de solicitud  
    
CREATE OR REPLACE PROCEDURE SP_BUSCAR_PEDIDO(BD_PEDIDO out SYS_REFCURSOR)
IS
--declaracion de variable local & filtro estado activo.
BEGIN
--sentencias
OPEN BD_PEDIDO FOR SELECT * FROM orden_compra oc
INNER JOIN solicitud sol ON oc.id_solicitud=sol.id_solicitud
WHERE sol.id_estado=2;
EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END SP_BUSCAR_PEDIDO;
---------------------------------------------------------

SELECT ps.id_pub_solicitud, ps.nombre_especie, ps.variedad,ps.kilos,TO_CHAR(ps.fecha_creacion, 'dd/mm/YYY') as "fecha creacion)",
TO_CHAR(ps.fecha_creacion, 'DD/MM/YYYY') as "fecha publicacion", ps.id_pedido, ps.id_solicitud, img.imagen
FROM publicacion_solicitud ps
INNER JOIN imagen img ON img.id_imagen=ps.id_imagen
where ps.id_solicitud=1 and ps.id_estado_publicacion_solicitud=1;

CREATE OR REPLACE PROCEDURE SP_BUSCAR_DETALLE_PEDIDO(id_detalle Number, DETALLEPEDIDOS out SYS_REFCURSOR)
IS
BEGIN
OPEN DETALLEPEDIDOS FOR SELECT ps.id_pub_solicitud, ps.nombre_especie, ps.variedad,ps.kilos,TO_CHAR(ps.fecha_creacion, 'dd/mm/YYY') as "fecha creacion)",
TO_CHAR(ps.fecha_creacion, 'DD/MM/YYYY') as "fecha publicacion", ps.id_pedido, ps.id_solicitud, img.imagen
FROM publicacion_solicitud ps
INNER JOIN imagen img ON img.id_imagen=ps.id_imagen
where ps.id_solicitud=id_detalle and ps.id_estado_publicacion_solicitud=1;
EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;

commit;