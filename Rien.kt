// Génère data/rien.json : une liste d'excuses pour ne rien faire.
import java.io.File

fun main() {
    val sujets = listOf("Le compilateur", "Mon chat", "Le cloud", "Le stagiaire", "Mercure")
    val raisons = listOf("est en rétrograde", "a mangé le cache", "attend une mise à jour", "ne répond plus", "fait une pause")
    val excuses = sujets.flatMap { s -> raisons.map { r -> "$s $r." } }.shuffled().take(12)
    val json = excuses.joinToString(",\n    ", "{\n  \"excuses\": [\n    ", "\n  ]\n}") { "\"$it\"" }
    File("data").mkdirs()
    File("data/rien.json").writeText(json)
    println("${excuses.size} excuses générées par Kotlin.")
}
