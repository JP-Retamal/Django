DROP SEQUENCE SEC_PAGO;

CREATE SEQUENCE  SEC_PAGO
MINVALUE 1 
MAXVALUE 99999 
INCREMENT BY 1 
START WITH 1 
CACHE 20 NOORDER  
NOCYCLE  NOKEEP  
NOSCALE  GLOBAL ;

DROP TRIGGER PAGO_AUTOINCREMENTS;

CREATE OR REPLACE TRIGGER PAGO_AUTOINCREMENTS 
    BEFORE INSERT ON PAGO 
    FOR EACH ROW

    BEGIN
        SELECT SEC_PAGO.NEXTVAL
        INTO   :new.ID_PAGO
        FROM   dual;
    END;
    
DROP PROCEDURE SP_AGREGAR_PAGO;

CREATE OR REPLACE PROCEDURE SP_AGREGAR_PAGO(
    v_descrpcion VARCHAR2, v_monto NUMBER, v_fecha_pago DATE, v_kilos NUMBER, v_usuario VARCHAR2, v_especie NUMBER,
    v_variedad NUMBER, v_idVventaLocal NUMBER,  v_idStock NUMBER, v_salida out NUMBER
    )
IS

    --lista: 
    --salida= 0 "no se realizo el registro".
    --salida= 1 "Registro exitoso".
    Conteo Number(1);            
BEGIN
    INSERT INTO PAGO VALUES (SEC_PAGO.NEXTVAL, v_descrpcion, v_monto, v_fecha_pago, v_kilos, v_usuario,
    v_especie, v_variedad, v_idVventaLocal);
    
    UPDATE STOCK_SOBRANTE SET KILO = KILO-v_kilos WHERE id_stock=v_idStock;
    
    SELECT COUNT(*) as conteo_cr INTO Conteo FROM STOCK_SOBRANTE WHERE KILO=0;   
    IF Conteo = 1
            THEN 
                UPDATE VENTA_LOCAL SET ID_ESTADO = 2  WHERE id_venta_local=v_idvventalocal ;
    END IF;
    v_salida:=1;
    
EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    v_salida:=0;
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;


Set SERVEROUTPUT ON; -- para ver salida del DBMS_OUTPUT
declare 
salida number(1);
Begin
SP_AGREGAR_PAGO('agregar  datos acorde a las columnas', salida);
DBMS_OUTPUT.PUT_LINE(salida);
end;