package setiptah.hackerrank.strings.stringfactor

/**
  * Created by ktreleav on 7/17/2017.
  */
object StringFactorUtil {
  def repeats(word: String, string: String): Int = {
    def sub(k: Int) = string.substring(k, k + word.length)

    ((0 to string.length - word.length)
      .map( sub )
      .filter( _ == word )
      .length)
  }

  def score(word: String, string: String): Int = {
    word.length * repeats(word, string)
  }

  def substrings(string: String): Seq[String] = for (
    i <- 0 until string.length;
    j <- (i+1) to string.length) yield {
    string.substring(i,j)
  }
}
