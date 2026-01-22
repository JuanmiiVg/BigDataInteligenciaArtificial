from pymongo import MongoClient

mongo_client = MongoClient('mongodb://admin:password@mongodb:27017/?authSource=admin')
db = mongo_client['consumo_db']

print('Documentos en consumos_mensuales:', db['consumos_mensuales'].count_documents({}))
print('Documentos en anomalias_detectadas:', db['anomalias_detectadas'].count_documents({}))
print('Documentos en consumos_horarios:', db['consumos_horarios'].count_documents({}))

print('\nPrimero en consumos_mensuales:')
doc = db['consumos_mensuales'].find_one()
if doc:
    print(f"  _id: {doc['_id']}")
    print(f"  consumo_total: {doc.get('consumo_total')}")
    print(f"  anomalias_detectadas: {doc.get('anomalias_detectadas')}")
else:
    print("  (vacío)")
