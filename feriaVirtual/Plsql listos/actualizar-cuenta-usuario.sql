-- Buscar usuario comerciante

SELECT us.id_usuario, us.run_usuario, us.nombre, us.ap_paterno,
            us.ap_materno, TO_CHAR(us.fecha_nac,'DD/MM/YYYY') as "FECHA",
            us.email, us.direccion, us.num_celular, com.ID_COMUNA, com.DES_COMUNA,
            pro.ID_PROVINCIA, pro.DES_PROVINCIA, reg.ID_REGION, reg.DES_REGION
        FROM USUARIO us
        JOIN ESTADO_USUARIO esu ON us.ID_ESTADO = esu.ID_ESTADO
        LEFT JOIN COMUNA com ON us.ID_COMUNA = com.ID_COMUNA
        JOIN PROVINCIA pro ON com.ID_PROVINCIA = pro.ID_PROVINCIA
        JOIN REGION reg ON pro.ID_REGION = reg.ID_REGION
        where us.EMAIL = 'comerciante@gmail.com';

create or replace procedure SP_BUSCAR_USUARIO(email in Varchar2,usuario out SYS_REFCURSOR)
AS
    v_email VARCHAR2(150 BYTE) := email;
    BEGIN
        open usuario for 
        SELECT us.id_usuario, us.run_usuario, us.nombre, us.ap_paterno,
            us.ap_materno, TO_CHAR(us.fecha_nac,'DD/MM/YYYY') as "FECHA",
            us.email, us.direccion, us.num_celular, com.ID_COMUNA, com.DES_COMUNA,
            pro.ID_PROVINCIA, pro.DES_PROVINCIA, reg.ID_REGION, reg.DES_REGION
        FROM USUARIO us
        JOIN ESTADO_USUARIO esu ON us.ID_ESTADO = esu.ID_ESTADO
        LEFT JOIN COMUNA com ON us.ID_COMUNA = com.ID_COMUNA
        JOIN PROVINCIA pro ON com.ID_PROVINCIA = pro.ID_PROVINCIA
        JOIN REGION reg ON pro.ID_REGION = reg.ID_REGION
        where us.EMAIL = v_email;
END;

-- procedimiento actualizar usuario
CREATE OR REPLACE PROCEDURE SP_MODIFICAR_USUARIO(
    email in VARCHAR2, celular in NUMBER, direccion in VARCHAR2, comuna in NUMBER,
    code out NUMBER
    )
AS
    v_email VARCHAR2(250 CHAR):=email;
    v_direccion VARCHAR2(150 CHAR):=direccion; 
    v_celular NUMBER(9,0):=celular; 
    v_comuna NUMBER(3,0):=comuna;
    --lista: 
    --code 0 no se realizo el registro
    --code 1 Actualizacion exitosa
BEGIN
    UPDATE usuario SET  direccion = v_direccion, num_celular = v_celular, id_comuna = v_comuna WHERE email = v_email;
    code:=1;
EXCEPTION
    WHEN OTHERS THEN
        code:=0;
        DBMS_OUTPUT.PUT_LINE(SQLERRM);
END SP_MODIFICAR_USUARIO;
