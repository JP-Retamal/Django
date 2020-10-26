--Plsql listar detalle de pedidos 
SELECT * FROM orden_compra oc
INNER JOIN solicitud sol ON oc.id_solicitud=sol.id_solicitud
WHERE sol.id_estado=2
;
    
    
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

----------------------------------------------------------
--este no
SELECT
    oc.id_orden, oc.id_solicitud, oc.total, oc.id_estado as "seguimiento",
    TO_CHAR(sol.fecha_creacion) as "Fecha Creacion", es.des_especie, ds.variedad, ds.kilos, 
    img.imagen
FROM  orden_compra oc INNER JOIN solicitud sol ON oc.id_solicitud=sol.id_solicitud
INNER JOIN detalle_solicitud DS ON ds.id_solicitud=sol.id_solicitud
INNER JOIN especie es ON es.id_especie=ds.id_especie
INNER JOIN variedad va ON va.id_especie=es.id_especie
INNER JOIN imagen img ON img.id_imagen=va.id_imagen
WHERE sol.id_estado=2 and va.des_variedad=ds.variedad;

DROP PROCEDURE SP_BUSCAR_DETALLE_PEDIDO;

--plsql listar saldos calidad baja & filtro estado activo.
CREATE OR REPLACE PROCEDURE SP_BUSCAR_DETALLE_PEDIDO(v_id_orden NUMBER, BD_PEDIDO out SYS_REFCURSOR)
IS
--declaracion de variable local & filtro estado activo.
BEGIN
--sentencias
OPEN BD_PEDIDO FOR SELECT
    oc.id_orden, oc.id_solicitud, oc.total, oc.id_estado as "seguimiento",
    TO_CHAR(sol.fecha_creacion) as "Fecha Creacion", es.des_especie, ds.variedad, ds.kilos, 
    img.imagen
FROM  orden_compra oc INNER JOIN solicitud sol ON oc.id_solicitud=sol.id_solicitud
INNER JOIN detalle_solicitud DS ON ds.id_solicitud=sol.id_solicitud
INNER JOIN especie es ON es.id_especie=ds.id_especie
INNER JOIN variedad va ON va.id_especie=es.id_especie
INNER JOIN imagen img ON img.id_imagen=va.id_imagen
WHERE sol.id_estado=2 and va.des_variedad=ds.variedad;
EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END SP_BUSCAR_DETALLE_PEDIDO;
-----------------------------------------------------------------
SELECT
    oc.id_orden, oc.id_solicitud, oc.total, oc.id_estado as "seguimiento",
    TO_CHAR(sol.fecha_creacion, 'dd/mm/YYYY') as "Fecha Creacion", es.des_especie, ds.variedad, ds.kilos, 
    img.imagen
FROM  orden_compra oc INNER JOIN solicitud sol ON oc.id_solicitud=sol.id_solicitud
INNER JOIN detalle_solicitud DS ON ds.id_solicitud=sol.id_solicitud
INNER JOIN especie es ON es.id_especie=ds.id_especie
INNER JOIN variedad va ON va.id_especie=es.id_especie
INNER JOIN imagen img ON img.id_imagen=va.id_imagen
WHERE sol.id_estado=2 and oc.id_orden=1 and va.des_variedad=ds.variedad;

CREATE OR REPLACE PROCEDURE SP_BUSCAR_DETALLE_PEDIDO(id_detalle Number, DETALLEPEDIDOS out SYS_REFCURSOR)
IS
BEGIN
OPEN DETALLEPEDIDOS FOR SELECT
    oc.id_orden, oc.id_solicitud, oc.total, oc.id_estado as "seguimiento",
    TO_CHAR(sol.fecha_creacion, 'dd/mm/YYYY') as "Fecha Creacion", es.des_especie, ds.variedad, ds.kilos, 
    img.imagen
FROM  orden_compra oc INNER JOIN solicitud sol ON oc.id_solicitud=sol.id_solicitud
INNER JOIN detalle_solicitud DS ON ds.id_solicitud=sol.id_solicitud
INNER JOIN especie es ON es.id_especie=ds.id_especie
INNER JOIN variedad va ON va.id_especie=es.id_especie
INNER JOIN imagen img ON img.id_imagen=va.id_imagen
WHERE sol.id_estado=2 and oc.id_orden=id_detalle and va.des_variedad=ds.variedad;
EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;