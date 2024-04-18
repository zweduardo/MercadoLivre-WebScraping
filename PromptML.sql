INSERT INTO Calc2 (Data, Description, Link, Price, AVG_PRICE, DESC_PRICE)
SELECT 
    MLOfertasdodia2.Date,
    MLOfertasdodia2.Description,
    MLOfertasdodia2.Link,
    CAST(MLOfertasdodia2.Price AS DECIMAL(10,0)),
    AVG(MLOfertasdodia2.Price) OVER (PARTITION BY MLOfertasdodia2.Description) AS AVG_PRICE,
    (MLOfertasdodia2.Price - AVG(MLOfertasdodia2.Price) OVER (PARTITION BY MLOfertasdodia2.Description)) / AVG(MLOfertasdodia2.Price) OVER (PARTITION BY MLOfertasdodia2.Description) AS DESC_PRICE
FROM
    MLOfertasdodia2

