import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

class Ejercicio1 {

    public static void main(String[] args) {
        AgrupadorDeAnagramas agrupador = new AgrupadorDeAnagramas();

        List<String> palabrasDeEjemplo = List.of("comer", "recto", "merco", "treco", "python", "java", "avaj");
        System.out.println("Entrada: " + palabrasDeEjemplo);
        System.out.println("Grupos:  " + agrupador.agruparAnagramas(palabrasDeEjemplo));

        List<String> listaVacia = List.of();
        System.out.println("Entrada: " + listaVacia);
        System.out.println("Grupos:  " + agrupador.agruparAnagramas(listaVacia));
    }
}

class AgrupadorDeAnagramas {

    public List<List<String>> agruparAnagramas(List<String> palabras) {
        if (palabras == null || palabras.isEmpty()) {
            return Collections.emptyList();
        }

        Map<String, List<String>> palabrasPorFirma = new LinkedHashMap<>();
        for (String palabra : palabras) {
            String firma = obtenerFirmaDeLetrasOrdenadas(palabra);
            palabrasPorFirma.computeIfAbsent(firma, firmaNueva -> new ArrayList<>()).add(palabra);
        }

        return new ArrayList<>(palabrasPorFirma.values());
    }

    private String obtenerFirmaDeLetrasOrdenadas(String palabra) {
        char[] letras = palabra.toLowerCase(Locale.ROOT).toCharArray();
        Arrays.sort(letras);
        return new String(letras);
    }
}
