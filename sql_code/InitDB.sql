CREATE SCHEMA IF NOT EXISTS frog_cafe;

CREATE TABLE frog_cafe.Roles (
    Id SERIAL PRIMARY KEY,
    Name TEXT NOT NULL
);

CREATE TABLE frog_cafe.Users (
    Id SERIAL PRIMARY KEY,
    Name TEXT NOT NULL,
    Pass TEXT NOT NULL,
    Role_id INT REFERENCES frog_cafe.Roles(Id)
);

CREATE TABLE frog_cafe.Toads (
    Id SERIAL PRIMARY KEY,
    Pic TEXT NOT NULL,
    Is_taken BOOLEAN DEFAULT FALSE
);

CREATE TABLE frog_cafe.Order_statuses (
    Id SERIAL PRIMARY KEY,
    Name TEXT NOT NULL
);

CREATE TABLE frog_cafe.Orders (
    Id SERIAL PRIMARY KEY,
    User_id INT REFERENCES frog_cafe.Users(Id),
    Toad_id INT REFERENCES frog_cafe.Toads(Id),
    Status_id INT REFERENCES frog_cafe.Order_statuses(Id),
    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE frog_cafe.Menu (
    Id SERIAL PRIMARY KEY,
    Dish_name TEXT NOT NULL,
    Image TEXT,
    Is_available BOOLEAN DEFAULT TRUE,
    Description TEXT
);

CREATE TABLE frog_cafe.Cart (
    Id SERIAL PRIMARY KEY,
    Order_id INT REFERENCES frog_cafe.Orders(Id),
    Menu_item INT REFERENCES frog_cafe.Menu(Id)
);
