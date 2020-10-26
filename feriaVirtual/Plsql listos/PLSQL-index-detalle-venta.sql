--LISTADOS PARA INDEX
--Listar saldos calidad baja
SELECT dl.id_detalle_local, st.id_stock, vl.id_venta_local, dl.precio,
    st.kilo, es.des_especie, va.des_variedad, im.imagen, ca.detalle, esv.des_estado
FROM detalle_local dl 
INNER JOIN calidad ca on ca.id_calidad = dl.id_calidad
INNER JOIN venta_local vl on vl.id_venta_local = dl.id_venta_local
INNER JOIN estado_venta esv on esv.id_estado = vl.id_estado
INNER JOIN stock_sobrante st on st.id_stock = dl.id_stock
INNER JOIN variedad va on va.id_variedad = st.id_variedad
INNER JOIN imagen im on im.id_imagen = va.id_imagen
INNER JOIN especie es on es.id_especie = va.id_especie
WHERE ca.id_calidad = 1 and vl.id_estado = 1;

--plsql listar saldos calidad baja & filtro estado activo.
CREATE OR REPLACE PROCEDURE SP_CALIDAD_BAJA(BAJA out SYS_REFCURSOR)
IS
BEGIN
OPEN BAJA FOR SELECT dl.id_detalle_local, st.id_stock, vl.id_venta_local, dl.precio,
    st.kilo, es.des_especie, va.des_variedad, im.imagen, ca.detalle, esv.des_estado
FROM detalle_local dl 
INNER JOIN calidad ca on ca.id_calidad = dl.id_calidad
INNER JOIN venta_local vl on vl.id_venta_local = dl.id_venta_local
INNER JOIN estado_venta esv on esv.id_estado = vl.id_estado
INNER JOIN stock_sobrante st on st.id_stock = dl.id_stock
INNER JOIN variedad va on va.id_variedad = st.id_variedad
INNER JOIN imagen im on im.id_imagen = va.id_imagen
INNER JOIN especie es on es.id_especie = va.id_especie
WHERE ca.id_calidad = 1 and vl.id_estado = 1;
EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;

---------------------------------------------

--Lista de calidad media y Alta & filtro estado activo.

SELECT dl.id_detalle_local, st.id_stock, vl.id_venta_local, dl.precio,
    st.kilo, es.des_especie, va.des_variedad, im.imagen, ca.detalle, esv.des_estado
FROM detalle_local dl 
INNER JOIN calidad ca on ca.id_calidad = dl.id_calidad
INNER JOIN venta_local vl on vl.id_venta_local = dl.id_venta_local
INNER JOIN estado_venta esv on esv.id_estado = vl.id_estado
INNER JOIN stock_sobrante st on st.id_stock = dl.id_stock
INNER JOIN variedad va on va.id_variedad = st.id_variedad
INNER JOIN imagen im on im.id_imagen = va.id_imagen
INNER JOIN especie es on es.id_especie = va.id_especie
WHERE ca.id_calidad != 1 and vl.id_estado = 1;

--plsql listar calidad media y alta & filtro estado activo.
CREATE OR REPLACE PROCEDURE SP_CALIDAD_MEDIA_ALTA(MEDIA_ALTA out SYS_REFCURSOR)
IS
BEGIN
OPEN MEDIA_ALTA FOR SELECT dl.id_detalle_local, st.id_stock, vl.id_venta_local, dl.precio,
    st.kilo, es.des_especie, va.des_variedad, im.imagen, ca.detalle, esv.des_estado
FROM detalle_local dl 
INNER JOIN calidad ca on ca.id_calidad = dl.id_calidad
INNER JOIN venta_local vl on vl.id_venta_local = dl.id_venta_local
INNER JOIN estado_venta esv on esv.id_estado = vl.id_estado
INNER JOIN stock_sobrante st on st.id_stock = dl.id_stock
INNER JOIN variedad va on va.id_variedad = st.id_variedad
INNER JOIN imagen im on im.id_imagen = va.id_imagen
INNER JOIN especie es on es.id_especie = va.id_especie
WHERE ca.id_calidad != 1 and vl.id_estado = 1;
EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;
-------------------------------------------------------------------------------------------------------------------------

-- traer detalle & filtro estado activo.
SELECT dl.id_detalle_local, st.id_stock, vl.id_venta_local, dl.precio,
    st.kilo, es.des_especie, va.des_variedad, im.imagen, TO_CHAR(st.fecha_cosecha, 'dd/mm/YYYY')as "Fecha de cosecha",
    ca.detalle, esv.des_estado, dl.descripcion, es.id_especie, va.id_variedad
FROM detalle_local dl 
INNER JOIN stock_sobrante st on st.id_stock = dl.id_stock 
INNER JOIN venta_local vl on vl.id_venta_local = dl.id_venta_local 
INNER JOIN variedad va on va.id_variedad = st.id_variedad 
INNER JOIN especie es on es.id_especie = va.id_especie
INNER JOIN imagen im on im.id_imagen = va.id_imagen
INNER JOIN calidad ca on ca.id_calidad = dl.id_calidad
INNER JOIN estado_venta esv on esv.id_estado = vl.id_estado
WHERE dl.id_detalle_local = 1 and esv.id_estado = 1;

CREATE OR REPLACE PROCEDURE SP_BUSCAR_DETALLE_VLOCAL(v_id_detalle NUMBER, BD_VLOCAL out SYS_REFCURSOR)
IS
--declaracion de variable local & filtro estado activo.
BEGIN
--sentencias
OPEN BD_VLOCAL FOR SELECT dl.id_detalle_local, st.id_stock, vl.id_venta_local, dl.precio,
    st.kilo, es.des_especie, va.des_variedad, im.imagen, TO_CHAR(st.fecha_cosecha, 'dd/mm/YYYY')as "Fecha de cosecha",
    ca.detalle, esv.des_estado, dl.descripcion, es.id_especie, va.id_variedad
FROM detalle_local dl 
INNER JOIN stock_sobrante st on st.id_stock = dl.id_stock 
INNER JOIN venta_local vl on vl.id_venta_local = dl.id_venta_local 
INNER JOIN variedad va on va.id_variedad = st.id_variedad 
INNER JOIN especie es on es.id_especie = va.id_especie
INNER JOIN imagen im on im.id_imagen = va.id_imagen
INNER JOIN calidad ca on ca.id_calidad = dl.id_calidad
INNER JOIN estado_venta esv on esv.id_estado = vl.id_estado
WHERE dl.id_detalle_local = v_id_detalle and esv.id_estado = 1;
EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END SP_BUSCAR_DETALLE_VLOCAL;

----------
















