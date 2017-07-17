package setiptah.hackerrank.strings.stringfactor

/**
  * Created by ktreleav on 7/3/2017.
  */

trait StringFactorAlgorithm {
  /**
    * The function L(s,S) = |s| * the number of occurrences of s as a contiguous substring of S.
    *
    */

  def score(string: String): (Int, String)
}
