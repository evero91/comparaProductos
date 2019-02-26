import os
import sys
import csv

argumentos = sys.argv
archivo1 = str(argumentos[1])
archivo2 = str(argumentos[2])
archivoResultado = str(argumentos[3])

directorioArchivos = "/Users/sistemas/Documents/Ever/shoemat/"

with open(directorioArchivos + archivo1, 'r') as file:
	reader = csv.reader(file)
	listaProductos = sorted(list(reader))

with open(directorioArchivos + archivo2, 'r') as fileServer:
	reader = csv.reader(fileServer)
	listaServerProductos = sorted(list(reader))

productos = []
serverProductos = []

for producto in listaProductos:
	productos.append(str(producto[0]))

for serverProducto in listaServerProductos:
	serverProductos.append(str(serverProducto[0]))

productosExistentes = []
productosSobrantes = []
productosFaltantes = []

# Buscar productos de lista en los productos servidor para obtener existentes y sobrantes del servidor
for serverProducto in serverProductos:
	productoEncontrado = False

	for producto in productos:
		if str(producto).strip().upper() == str(serverProducto).strip().upper():
			productosExistentes.append(producto)
			productoEncontrado = True
			break

	if not productoEncontrado:
		productosSobrantes.append(serverProducto)

# Buscar productos de lista en los productos existentes para obtener faltantes
for producto in productos:
	productoExiste = False
	# print("-- BUSCANDO ----- " + str(producto))

	for productosExistente in productosExistentes:
		# print("" + str(productosExistente).strip().upper() +" == " + str(producto).strip().upper() + ": " + str((str(productosExistente).strip().upper() == str(producto).strip().upper())))

		if str(productosExistente).strip().upper() == str(producto).strip().upper():
			productoExiste = True
			# print("-- BREAK! -----")
			break

	if not productoExiste:
		productosFaltantes.append(producto)
		# print("-- FALTA ----- " + str(producto))


if os.path.exists(directorioArchivos + archivoResultado):
	os.remove(directorioArchivos + archivoResultado)

with open(directorioArchivos + archivoResultado, 'w+') as fileResultado:
	for productosFaltante in productosFaltantes:
		fileResultado.write("INSERT INTO oportunidades_clasificaciones(idOportunidadClasificacion, descripcion, idOportunidadClasificacionPadre, borrar, idEmpresa, fechaModificacion) VALUES(UUID(), '%s', '580d6657-3f39-4c1e-b070-fb50d3b772c0', 0, 1, now());\n" % str(productosFaltante))

	for  productosSobrante in productosSobrantes:
		fileResultado.write("DELETE FROM oportunidades_clasificaciones WHERE descripcion = '%s';\n" % str(productosSobrante))

print('Productos Existentes')
print(productosExistentes)
print()

print('Productos Faltantes')
print(productosFaltantes)
print()

print('Productos Sobrantes')
print(productosSobrantes)
print()
