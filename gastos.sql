-- CREATE TABLE egresos (id_egreso INTEGER PRIMARY KEY, monto REAL, categoria TEXT);

-- INSERT INTO egresos (monto, categoria) VALUES (1200, "Carro");

-- SELECT nombre_cuenta FROM cuentas ORDER BY id_cuenta ASC LIMIT 5;

-- DROP TABLE egresos;

-- DROP TABLE ingresos;

-- DROP TABLE puente_movimientos;

-- DROP TABLE cuentas;

-- CREATE TABLE cuentas (id_cuenta INTEGER PRIMARY KEY NOT NULL, id_usuario INTEGER NOT NULL, nombre_cuenta TEXT NOT NULL, FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)); 

-- CREATE TABLE egresos (id_egreso INTEGER PRIMARY KEY NOT NULL, id_usuario INTEGER NOT NULL, id_cuenta INTEGER NOT NULL, id_categoria_egr INTEGER NOT NULL, monto REAL NOT NULL, moneda TEXT NOT NULL, mes TEXT NOT NULL, FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario), FOREIGN KEY (id_cuenta) REFERENCES cuentas(id_cuenta), FOREIGN KEY (id_categoria_egr) REFERENCES categoria_egresos(id_categoria_egr));

-- CREATE TABLE ingresos (id_ingreso INTEGER PRIMARY KEY NOT NULL, id_usuario INTEGER NOT NULL, id_cuenta INTEGER NOT NULL, id_categoria_ing INTEGER NOT NULL, monto REAL NOT NULL, moneda TEXT NOT NULL, mes TEXT NOT NULL, FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario), FOREIGN KEY (id_cuenta) REFERENCES cuentas(id_cuenta), FOREIGN KEY (id_categoria_ing) REFERENCES categoria_ingresos(id_categoria_ing));

-- INSERT INTO cuentas (id_usuario, nombre_cuenta) VALUES (1, "cuenta de prueba");

-- INSERT INTO egresos (id_usuario, id_cuenta, id_categoria_egr, monto, moneda, mes) VALUES (1,1,7,100,"NIO","FEBRERO");

-- SELECT monto, mes, categoria_e FROM egresos, categoria_egresos WHERE id_usuario = 1 AND egresos.id_categoria_egr = categoria_egresos.id_categoria_egr ORDER BY id_egreso DESC;

-- INSERT INTO ingresos (id_usuario, id_cuenta, id_categoria_ing, monto, moneda, mes) VALUES (1,1,1,500,"NIO","FEBRERO");

-- SELECT monto, mes, categoria_i FROM ingresos, categoria_ingresos WHERE id_usuario = 1 AND ingresos.id_categoria_ing = categoria_ingresos.id_categoria_ing ORDER BY id_ingreso DESC;

-- SELECT id_categoria_egr, sum(monto) FROM egresos WHERE id_usuario = 1  GROUP BY id_categoria_egr;

-- SELECT sum(monto), categoria_e FROM egresos, categoria_egresos WHERE id_usuario = 1 AND egresos.id_categoria_egr = categoria_egresos.id_categoria_egr GROUP BY categoria_e;

SELECT sum(monto), categoria_i FROM ingresos, categoria_ingresos WHERE id_usuario = 1 AND ingresos.id_categoria_ing = categoria_ingresos.id_categoria_ing GROUP BY categoria_i;