-- crear procidimiento Listar Historial compra
create or replace procedure SP_LISTAR_HISTORIAL_COMPRA(email in varchar2,registros out SYS_REFCURSOR)
AS
    v_email VARCHAR2(150 BYTE) := email;
    BEGIN
        open registros for 
            Select 
                VENTA_LOCAL.ID_VENTA_LOCAL as "ID",
                PAGO.DESCRIPCION as "DESCRIPCION",
                TO_CHAR(PAGO.FECHA_PAGO,'DD/MM/YYYY') as "FECHA",
                PAGO.MONTO as "TOTAL",
                ESTADO_VENTA.DES_ESTADO as "ESTADO"
            FROM VENTA_LOCAL 
            JOIN ESTADO_VENTA ON VENTA_LOCAL.ID_ESTADO = ESTADO_VENTA.ID_ESTADO
            LEFT JOIN PAGO ON  VENTA_LOCAL.ID_VENTA_LOCAL = PAGO.ID_VENTA_LOCAL
            WHERE Pago.Usuario = v_email;
    EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;


-- crear procidimiento detalle Historial compra
create or replace procedure SP_LISTAR_DETALLE_HISTORIAL_COMPRA(id_venta in Number,detalle_hc out SYS_REFCURSOR)
AS
    vid_venta NUMBER(8,0) := id_venta;
    BEGIN
        open detalle_hc for 
            Select 
                DETALLE_LOCAL.ID_DETALLE_LOCAL,
                IMAGEN.IMAGEN,
                PAGO.DESCRIPCION as "DES_P",
                TO_CHAR(PAGO.FECHA_PAGO,'DD/MM/YYYY') as "FECHA_P",
                PAGO.KILOS,
                PAGO.MONTO,
                DETALLE_LOCAL.DESCRIPCION as "Desc_Det",
                TO_CHAR(STOCK_SOBRANTE.FECHA_COSECHA,'DD/MM/YYYY') as "FECHA_C",
                ESTADO_VENTA.DES_ESTADO as "ESTADO"
            FROM VENTA_LOCAL 
            JOIN ESTADO_VENTA ON VENTA_LOCAL.ID_ESTADO = ESTADO_VENTA.ID_ESTADO
            LEFT JOIN PAGO ON  VENTA_LOCAL.ID_VENTA_LOCAL = PAGO.ID_VENTA_LOCAL
            JOIN DETALLE_LOCAL ON VENTA_LOCAL.ID_VENTA_LOCAL = DETALLE_LOCAL.ID_VENTA_LOCAL
            JOIN ESPECIE ON ESPECIE.ID_ESPECIE = PAGO.ESPECIE
            JOIN VARIEDAD ON VARIEDAD.ID_VARIEDAD = PAGO.VARIEDAD
            JOIN IMAGEN ON IMAGEN.ID_IMAGEN = VARIEDAD.ID_IMAGEN
            INNER JOIN STOCK_SOBRANTE on STOCK_SOBRANTE.ID_STOCK = DETALLE_LOCAL.ID_STOCK
            WHERE VENTA_LOCAL.ID_VENTA_LOCAL = vid_venta;
    EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
    END;


    
    