
CREATE TABLE dimension1 (
    urunID INT PRIMARY KEY,
    urunAdi VARCHAR(50) NOT NULL
    urunGrubu VARCHAR(50) NOT NULL
);

CREATE TABLE dimension2 (
    musteriID INT PRIMARY KEY,
    musteriAdi VARCHAR(50) NOT NULL
);

CREATE TABLE dimension3 (
    zamanID INT PRIMARY KEY,
    zamanAdi VARCHAR(50) NOT NULL
    ay INT NOT NULL
    yil VARCHAR(50) NOT NULL
);

CREATE TABLE fact (
    id INT PRIMARY KEY,
    urunID INT REFERENCES dimension1(urunID),
    musteriID INT REFERENCES dimension2(musteriID),
    zamanID INT REFERENCES dimension3(zamanID),
    tutar NUMERIC NOT NULL
);
