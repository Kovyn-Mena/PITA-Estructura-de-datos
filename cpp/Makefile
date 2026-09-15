CXX = g++
CXXFLAGS = -std=c++17 -Wall
SRC = src/main.cpp src/gestion.cpp src/nomina.cpp src/persistencia.cpp src/interfaz.cpp src/generador.cpp
OUT = pita

all:
	$(CXX) $(CXXFLAGS) $(SRC) -o $(OUT)

run: all
	./$(OUT)

clean:
	rm -f $(OUT)
