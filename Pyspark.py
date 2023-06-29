from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession


conf = SparkConf().setAppName("Lectura")
sc = SparkContext.getOrCreate(conf=conf)
rdd = sc.textFile("Data.csv")

spark = SparkSession.builder.getOrCreate()

def getRelatedProducts():
    header = rdd.first()
    data = rdd.filter(lambda line: line != header)
    products = data.map(lambda line: line.split(", "))

    best_products = products.filter(lambda product: float(product[3]) >= 4.8)

    #Para poner los headers en la tabla
    header_rdd = sc.parallelize([header.split(", ")])
    best_products = header_rdd.union(best_products)

    print("-------------TOP 10 PRODUCTOS MEJOR CALIFICADOS------------")
    
    df = spark.read.options(header="True", inferSchema="True").csv(best_products)
    df.show(10)
    
getRelatedProducts()