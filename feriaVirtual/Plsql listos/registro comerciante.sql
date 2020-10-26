----INSERT PARA FORMULARIO DE REGISTRO COMERCIANTES

--LISTAR REGIONES
SELECT r.des_region, p.des_provincia,c.id_comuna, c.des_comuna
from region r INNER JOIN provincia p on p.id_region = r.id_region
INNER JOIN comuna c on c.id_provincia = p.id_provincia;
-------------------------------------
--plsql para listar por region y sus provincias y comunas
CREATE OR REPLACE PROCEDURE SP_LISTAR_REGIONES(REGION out SYS_REFCURSOR)
IS
BEGIN
OPEN REGION FOR SELECT r.des_region, p.des_provincia, c.id_comuna, c.des_comuna
from region r INNER JOIN provincia p on p.id_region = r.id_region
INNER JOIN comuna c on c.id_provincia = p.id_provincia;
END;

--Secuencia para el usuario
DROP SEQUENCE SEC_USUARIO;

CREATE SEQUENCE  SEC_USUARIO
MINVALUE 1 
MAXVALUE 99999 
INCREMENT BY 1 
START WITH 5 
CACHE 20 NOORDER  
NOCYCLE  NOKEEP  
NOSCALE  GLOBAL ;

--Trigger que trabaja con la secuencia, busca el sigiente n°
DROP TRIGGER USUARIO_AUTOINCREMENTS;

CREATE OR REPLACE TRIGGER USUARIO_AUTOINCREMENTS 
    BEFORE INSERT ON usuario 
    FOR EACH ROW

    BEGIN
        SELECT SEC_USUARIO.NEXTVAL
        INTO   :new.ID_USUARIO
        FROM   dual;
    END;
--plsql para el registro de comerciantes.

DROP PROCEDURE SP_AGREGAR_COMERCIANTE;

CREATE OR REPLACE PROCEDURE SP_AGREGAR_COMERCIANTE(
    v_run VARCHAR2, v_nombre VARCHAR2, v_paterno VARCHAR2,
    v_materno VARCHAR2, v_f_nac VARCHAR2, v_email VARCHAR2,
    v_direccion VARCHAR2, v_celular NUMBER, v_clave VARCHAR2,
    v_id_comuna NUMBER, v_salida out NUMBER
    )
IS
    v_id_estado NUMBER:=1;
    v_id_rol NUMBER:=3;
    v_id_empresa NUMBER:=null;
    v_id_pais NUMBER:=1;
    
    --lista: 
    --salida= 0 "no se realizo el registro".
    --salida= 1 "Registro exitoso".
                        
BEGIN
    INSERT INTO USUARIO VALUES (SEC_USUARIO.NEXTVAL, v_run, v_nombre, v_paterno, v_materno, v_f_nac, v_email, v_direccion, v_celular, v_clave,
    v_id_estado, v_id_comuna, v_id_rol, v_id_empresa, v_id_pais);
    v_salida:=1;
EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    v_salida:=0;
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;

--------------------------------------------------------------------------------------------------------------------------------------------------
-- PLSQL validar rut.
SELECT * FROM usuario
WHERE run_usuario = '111111-1'; 

CREATE OR REPLACE PROCEDURE SP_BUSCA_RUT(RUT in Varchar2, v_salidaR out NUMBER)
AS
    Conteo Number(1);
    v_rut VARCHAR2(30 char) := RUT;   
    --lista:
    --conteo= 1 "Rut usuario ya existe en los registros". code =1 v_salida
    --code=2 "Rut no existe en los registros".
    --code=3 "Problemas al consultar a la BD".
    BEGIN
        Conteo := 0;
        Select COUNT(*) as conteo_rut INTO Conteo from USUARIO WHERE RUN_USUARIO = v_rut;
        IF Conteo = 1
          THEN v_salidaR :=1;
        ELSE v_salidaR :=2;
        END IF;
    EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    v_salidaR := 3;
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;
    
-- Ejecucion en Oracle
Set SERVEROUTPUT ON; -- para ver salida del DBMS_OUTPUT
declare 
salida number(1);
Begin
SP_BUSCA_RUT('11111111-1', salida);
DBMS_OUTPUT.PUT_LINE(salida);
end;
-- PLSQL validar rut.
SELECT * FROM usuario
WHERE run_usuario = '111111-1'; 

--------------------------------------------------------------------------------------------------------------------------------------------------
--PLSQL Valida correo.
CREATE OR REPLACE PROCEDURE SP_BUSCA_EMAIL(CORREO in Varchar2, v_salidaC out NUMBER)
AS
    Conteo Number(1);
    v_emal VARCHAR2(30 char) := CORREO;   
    --lista:
    --conteo= 1 "Rut usuario ya existe en los registros". code =1 v_salida
    --code=2 "Rut no existe en los registros".
    --code=3 "Problemas al consultar a la BD".
    BEGIN
        Conteo := 0;
        Select COUNT(*) as conteo_email INTO Conteo from USUARIO WHERE EMAIL = v_emal;
        IF Conteo = 1
          THEN v_salidaC :=1;
        ELSE v_salidaC :=2;
        END IF;
    EXCEPTION --control de excepciones
    WHEN OTHERS THEN
    v_salidaC := 3;
    DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;
    
Set SERVEROUTPUT ON; -- para ver salida del DBMS_OUTPUT
declare 
salida number(1);
Begin
SP_BUSCA_EMAIL('admin@admin.cl', salida);
DBMS_OUTPUT.PUT_LINE(salida);
end;
-- PLSQL validar email.
SELECT * FROM usuario
WHERE EMAIL = 'admin@admin.cl';   