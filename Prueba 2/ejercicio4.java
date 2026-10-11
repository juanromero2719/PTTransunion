import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

class Ejercicio4 {

    private static final int CANTIDAD_DE_HILOS = 3;
    private static final int INCREMENTOS_POR_HILO = 100_000;

    public static void main(String[] args) throws InterruptedException {
        compararResultado("Contador original sin sincronizacion", new ContadorSinSincronizacion());
        compararResultado("Solucion 1: metodos synchronized", new ContadorSincronizado());
        compararResultado("Solucion 2: AtomicInteger", new ContadorAtomico());
    }

    private static void compararResultado(String descripcion, Contador contador) throws InterruptedException {
        incrementarDesdeVariosHilos(contador);
        int valorEsperado = CANTIDAD_DE_HILOS * INCREMENTOS_POR_HILO;
        System.out.printf("%-40s esperado=%d obtenido=%d%n", descripcion, valorEsperado, contador.getValor());
    }

    private static void incrementarDesdeVariosHilos(Contador contador) throws InterruptedException {
        List<Thread> hilos = new ArrayList<>();
        for (int numeroDeHilo = 0; numeroDeHilo < CANTIDAD_DE_HILOS; numeroDeHilo++) {
            Thread hilo = new Thread(() -> incrementarRepetidamente(contador));
            hilos.add(hilo);
            hilo.start();
        }
        for (Thread hilo : hilos) {
            hilo.join();
        }
    }

    private static void incrementarRepetidamente(Contador contador) {
        for (int incremento = 0; incremento < INCREMENTOS_POR_HILO; incremento++) {
            contador.incrementar();
        }
    }
}

interface Contador {

    void incrementar();

    int getValor();
}

class ContadorSinSincronizacion implements Contador {

    private int valor = 0;

    @Override
    public void incrementar() {
        valor++;
    }

    @Override
    public int getValor() {
        return valor;
    }
}

class ContadorSincronizado implements Contador {

    private int valor = 0;

    @Override
    public synchronized void incrementar() {
        valor++;
    }

    @Override
    public synchronized int getValor() {
        return valor;
    }
}

class ContadorAtomico implements Contador {

    private final AtomicInteger valor = new AtomicInteger(0);

    @Override
    public void incrementar() {
        valor.incrementAndGet();
    }

    @Override
    public int getValor() {
        return valor.get();
    }
}
