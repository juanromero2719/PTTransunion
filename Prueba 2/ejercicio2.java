import java.util.List;

class Ejercicio2 {

    public static void main(String[] args) {
        PruebasEvaluadorDeSubsidio pruebas = new PruebasEvaluadorDeSubsidio();
        pruebas.ejecutarTodas();
    }
}

record Integrante(String nombre, int edad, boolean tieneSubsidio) {

    private static final int EDAD_MAYORIA_DE_EDAD = 18;
    private static final int EDAD_LIMITE_MENOR_PARA_BONO = 12;

    boolean esMayorDeEdad() {
        return edad >= EDAD_MAYORIA_DE_EDAD;
    }

    boolean esMenorParaBono() {
        return edad < EDAD_LIMITE_MENOR_PARA_BONO;
    }
}

record Hogar(List<Integrante> integrantes, double ingresoMensualTotal) {

    Hogar {
        integrantes = integrantes == null ? List.of() : List.copyOf(integrantes);
    }

    int cantidadDeIntegrantes() {
        return integrantes.size();
    }

    boolean tieneAlMenosUnMayorDeEdad() {
        return integrantes.stream().anyMatch(Integrante::esMayorDeEdad);
    }

    boolean tieneIntegranteConSubsidioActivo() {
        return integrantes.stream().anyMatch(Integrante::tieneSubsidio);
    }

    long contarMenoresParaBono() {
        return integrantes.stream().filter(Integrante::esMenorParaBono).count();
    }
}

record ResultadoEvaluacion(boolean elegible, double montoFinal, String motivo) {

    static ResultadoEvaluacion aprobado(double montoFinal, String motivo) {
        return new ResultadoEvaluacion(true, montoFinal, motivo);
    }

    static ResultadoEvaluacion rechazado(String motivo) {
        return new ResultadoEvaluacion(false, 0.0, motivo);
    }
}

class EvaluadorDeSubsidio {

    private static final double SMMLV = 1_300_000;
    private static final double MAXIMO_SALARIOS_MINIMOS_PERMITIDOS = 4;
    private static final double INGRESO_MAXIMO_PERMITIDO = SMMLV * MAXIMO_SALARIOS_MINIMOS_PERMITIDOS;
    private static final int MINIMO_INTEGRANTES = 1;
    private static final int MAXIMO_INTEGRANTES = 8;
    private static final int MINIMO_MENORES_PARA_BONO = 3;
    private static final double PORCENTAJE_BONO_POR_MENORES = 0.15;

    public ResultadoEvaluacion evaluarSubsidio(Hogar hogar, double subsidioBase) {
        validarParametros(hogar, subsidioBase);

        if (!tieneCantidadDeIntegrantesPermitida(hogar)) {
            return ResultadoEvaluacion.rechazado(
                    "El hogar debe tener entre " + MINIMO_INTEGRANTES + " y " + MAXIMO_INTEGRANTES + " integrantes");
        }
        if (superaIngresoMaximoPermitido(hogar)) {
            return ResultadoEvaluacion.rechazado(
                    "El ingreso mensual supera " + (int) MAXIMO_SALARIOS_MINIMOS_PERMITIDOS + " SMMLV");
        }
        if (!hogar.tieneAlMenosUnMayorDeEdad()) {
            return ResultadoEvaluacion.rechazado("El hogar no tiene integrantes mayores de edad");
        }
        if (hogar.tieneIntegranteConSubsidioActivo()) {
            return ResultadoEvaluacion.rechazado("Al menos un integrante tiene subsidio previo activo");
        }

        if (aplicaBonoPorMenores(hogar)) {
            double montoConBono = subsidioBase * (1 + PORCENTAJE_BONO_POR_MENORES);
            return ResultadoEvaluacion.aprobado(montoConBono, "Hogar elegible con bono adicional por 3 o mas menores de 12");
        }
        return ResultadoEvaluacion.aprobado(subsidioBase, "Hogar elegible");
    }

    private void validarParametros(Hogar hogar, double subsidioBase) {
        if (hogar == null) {
            throw new IllegalArgumentException("El hogar es obligatorio");
        }
        if (subsidioBase <= 0) {
            throw new IllegalArgumentException("El subsidio base debe ser mayor a cero");
        }
    }

    private boolean tieneCantidadDeIntegrantesPermitida(Hogar hogar) {
        int cantidad = hogar.cantidadDeIntegrantes();
        return cantidad >= MINIMO_INTEGRANTES && cantidad <= MAXIMO_INTEGRANTES;
    }

    private boolean superaIngresoMaximoPermitido(Hogar hogar) {
        return hogar.ingresoMensualTotal() > INGRESO_MAXIMO_PERMITIDO;
    }

    private boolean aplicaBonoPorMenores(Hogar hogar) {
        return hogar.contarMenoresParaBono() >= MINIMO_MENORES_PARA_BONO;
    }
}

class PruebasEvaluadorDeSubsidio {

    private static final double SUBSIDIO_BASE = 10_000_000;
    private static final double TOLERANCIA_MONETARIA = 0.001;

    private final EvaluadorDeSubsidio evaluador = new EvaluadorDeSubsidio();
    private int pruebasExitosas = 0;
    private int pruebasFallidas = 0;

    void ejecutarTodas() {
        deberiaAprobarHogarElegibleSinBono();
        deberiaAprobarHogarElegibleConBonoPorMenores();
        deberiaRechazarHogarPorIngresoAlto();
        deberiaRechazarHogarPorIntegranteConSubsidioActivo();
        deberiaRechazarHogarSinMayoresDeEdad();
        deberiaRechazarHogarSinIntegrantes();
        deberiaRechazarHogarConMasDeOchoIntegrantes();

        System.out.printf("%nResultado: %d exitosas, %d fallidas%n", pruebasExitosas, pruebasFallidas);
    }

    private void deberiaAprobarHogarElegibleSinBono() {
        Hogar hogar = new Hogar(List.of(
                new Integrante("Ana", 35, false),
                new Integrante("Luis", 37, false),
                new Integrante("Sofia", 8, false)
        ), 3_000_000);

        ResultadoEvaluacion resultado = evaluador.evaluarSubsidio(hogar, SUBSIDIO_BASE);

        verificar("Hogar elegible sin bono",
                resultado.elegible() && sonMontosIguales(resultado.montoFinal(), SUBSIDIO_BASE), resultado);
    }

    private void deberiaAprobarHogarElegibleConBonoPorMenores() {
        Hogar hogar = new Hogar(List.of(
                new Integrante("Marta", 40, false),
                new Integrante("Pedro", 10, false),
                new Integrante("Juana", 7, false),
                new Integrante("Tomas", 3, false)
        ), 4_000_000);

        ResultadoEvaluacion resultado = evaluador.evaluarSubsidio(hogar, SUBSIDIO_BASE);

        verificar("Hogar elegible con bono por menores",
                resultado.elegible() && sonMontosIguales(resultado.montoFinal(), 11_500_000), resultado);
    }

    private void deberiaRechazarHogarPorIngresoAlto() {
        Hogar hogar = new Hogar(List.of(
                new Integrante("Carlos", 45, false),
                new Integrante("Elena", 42, false)
        ), 5_200_001);

        ResultadoEvaluacion resultado = evaluador.evaluarSubsidio(hogar, SUBSIDIO_BASE);

        verificar("Hogar rechazado por ingreso alto", esRechazoConMontoCero(resultado), resultado);
    }

    private void deberiaRechazarHogarPorIntegranteConSubsidioActivo() {
        Hogar hogar = new Hogar(List.of(
                new Integrante("Rosa", 50, false),
                new Integrante("Andres", 22, true)
        ), 2_000_000);

        ResultadoEvaluacion resultado = evaluador.evaluarSubsidio(hogar, SUBSIDIO_BASE);

        verificar("Hogar rechazado por integrante con subsidio activo", esRechazoConMontoCero(resultado), resultado);
    }

    private void deberiaRechazarHogarSinMayoresDeEdad() {
        Hogar hogar = new Hogar(List.of(
                new Integrante("Mateo", 17, false),
                new Integrante("Valentina", 15, false)
        ), 1_500_000);

        ResultadoEvaluacion resultado = evaluador.evaluarSubsidio(hogar, SUBSIDIO_BASE);

        verificar("Hogar rechazado por no tener mayores de edad", esRechazoConMontoCero(resultado), resultado);
    }

    private void deberiaRechazarHogarSinIntegrantes() {
        Hogar hogar = new Hogar(List.of(), 1_000_000);

        ResultadoEvaluacion resultado = evaluador.evaluarSubsidio(hogar, SUBSIDIO_BASE);

        verificar("Hogar rechazado por no tener integrantes", esRechazoConMontoCero(resultado), resultado);
    }

    private void deberiaRechazarHogarConMasDeOchoIntegrantes() {
        Hogar hogar = new Hogar(List.of(
                new Integrante("Integrante 1", 60, false),
                new Integrante("Integrante 2", 58, false),
                new Integrante("Integrante 3", 30, false),
                new Integrante("Integrante 4", 28, false),
                new Integrante("Integrante 5", 25, false),
                new Integrante("Integrante 6", 20, false),
                new Integrante("Integrante 7", 10, false),
                new Integrante("Integrante 8", 6, false),
                new Integrante("Integrante 9", 2, false)
        ), 4_500_000);

        ResultadoEvaluacion resultado = evaluador.evaluarSubsidio(hogar, SUBSIDIO_BASE);

        verificar("Hogar rechazado por tener mas de 8 integrantes", esRechazoConMontoCero(resultado), resultado);
    }

    private boolean esRechazoConMontoCero(ResultadoEvaluacion resultado) {
        return !resultado.elegible() && sonMontosIguales(resultado.montoFinal(), 0.0);
    }

    private boolean sonMontosIguales(double montoObtenido, double montoEsperado) {
        return Math.abs(montoObtenido - montoEsperado) < TOLERANCIA_MONETARIA;
    }

    private void verificar(String nombrePrueba, boolean condicionCumplida, ResultadoEvaluacion resultado) {
        if (condicionCumplida) {
            pruebasExitosas++;
            System.out.printf("[OK]    %s -> %s%n", nombrePrueba, resultado);
        } else {
            pruebasFallidas++;
            System.out.printf("[FALLO] %s -> %s%n", nombrePrueba, resultado);
        }
    }
}
