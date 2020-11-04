--secuencias--

create sequence sec_detalle_sol
start with 4
increment by 1
maxvalue 99999
minvalue 1;

drop sequence sec_detalle_sol;

create sequence SEC_SOLICITUD_2
start with 2
increment by 1
maxvalue 99999
minvalue 1;

CREATE TABLE pruebadetalle (
    id     NUMBER(8) NOT NULL PRIMARY KEY,
    especie  VARCHAR2(30) NOT NULL,
    variedad  VARCHAR2(30) NOT NULL,
    cantidad  NUMBER(1) NOT NULL
);

--------------------------------------------------------

--ingresar solicitud--

create or replace procedure sp_ingresar_solicitud(
v_fecha date
) is
begin

INSERT INTO solicitud(id_solicitud,fecha_entrega,fecha_creacion,id_usuario,id_estado)
values (sec_solicitud_2.nextval,v_fecha,sysdate,1,1);
COMMIT;
end;



----------------------------------------------

--agregar detalle-----

create or replace procedure sp_agregar_fruta(
v_especie varchar2,
v_variedad varchar2,
v_cantidad number
) as
v_id NUMBER;
v_sec number;
begin


SELECT id_solicitud into v_sec FROM solicitud WHERE ROWNUM <= 1 order by id_solicitud desc;


select ID_ESPECIE into v_id
from especie
where des_especie=v_especie;


INSERT INTO DETALLE_SOLICITUD (ID_PEDIDO, KILOS, VARIEDAD, ID_SOLICITUD, ID_ESPECIE) VALUES (sec_detalle_sol.nextval, v_cantidad, v_variedad, v_sec, v_id);

COMMIT;
end;

-------------------------------------------------------------

--listar especie--
SELECT id_especie, des_especie
FROM especie ;


create or replace procedure sp_listar_especie(especie out SYS_REFCURSOR)
is
begin
    open especie for SELECT
        id_especie, des_especie
    FROM especie;
end;

commit;
---------------------------------------------------------

--listar variedad--

create or replace procedure sp_listar_variedad(variedad out SYS_REFCURSOR,
v_nombre_especie varchar2)
as
v_id number;
begin
    select ID_ESPECIE into v_id
    from especie
    where des_especie=v_nombre_especie;

    open variedad for SELECT
        *
    FROM variedad WHERE id_especie=v_id;
end;

-------------------------------------
SELECT
    *
FROM variedad where id_especie=1;

create or replace procedure sp_listar_variedad_por_especies(subcategorias out SYS_REFCURSOR,
categoria_id NUMBER)
as

begin
   
    open subcategorias for SELECT * FROM variedad WHERE id_especie=categoria_id;
end;

