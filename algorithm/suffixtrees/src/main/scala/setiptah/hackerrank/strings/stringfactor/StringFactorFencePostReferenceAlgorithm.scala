package setiptah.hackerrank.strings.stringfactor

object StringFactorFencePostReferenceAlgorithm extends StringFactorAlgorithm {
  case class Range(val startIndex: Int, val length: Int)

  def validRanges(length: Int): Seq[Range] = {
    for ( start <- 0 until length ; len <- 1 to length - start ) yield Range(start, len)
  }

  def repeatsFrom(range: Range, string: String): Int = {
    val Range(startIndex, length) = range
    val cmp = string.drop(startIndex).take(length)

    var reps = 0
    for ( i <- startIndex to (string.length - length) ) {
      if ( string.substring(i, i + length) == cmp ) {
        reps += 1
      }
    }

    reps
  }

  def score(string: String): (Int, String) = {
    val seq = for ( range <- validRanges(string.length)) yield {
      val repeats = repeatsFrom(range, string)
      println(range.startIndex, range.length, repeats)
      (range.length * repeats, string.substring(range.startIndex, range.startIndex + range.length))
    }

    seq.maxBy( _._1 )
  }
}